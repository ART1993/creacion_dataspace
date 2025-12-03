import os
import time
import requests
from datetime import datetime, timezone

BROKER_ORGA = os.getenv("BROKER_ORGA", "http://orionld_orga:1026/ngsi-ld/v1")
BROKER_ORGB = os.getenv("BROKER_ORGB", "http://orionld_orgb:1026/ngsi-ld/v1")

HEADERS_GET = {"Accept": "application/ld+json"}
HEADERS_POST = {
    "Content-Type": "application/ld+json",
    "Link": '<https://example.org/contexts/forest.jsonld>; '
            'rel="http://www.w3.org/ns/json-ld#context"; '
            'type="application/ld+json"'
}

PLOT_ID = "urn:ngsi-ld:ForestPlot:plot001"

def fetch_observations():
    url = f"{BROKER_ORGA}/entities?type=Observation"
    r = requests.get(url, headers=HEADERS_GET, timeout=10)
    r.raise_for_status()
    return r.json() or []

def compute_summary(observations):
    temps = []
    soils = []
    for e in observations:
        try:
            prop = e["observedProperty"]["value"]
            val = float(e["value"]["value"])
        except Exception:
            continue

        if prop == "airTemperature":
            temps.append(val)
        elif prop == "soilMoisture":
            soils.append(val)

    temp_mean = sum(temps) / len(temps) if temps else None
    soil_mean = sum(soils) / len(soils) if soils else None

    # Regla de juguete para riesgo
    if temp_mean is None or soil_mean is None:
        risk = "unknown"
    elif temp_mean > 30 and soil_mean < 0.15:
        risk = "high"
    elif temp_mean > 25 and soil_mean < 0.20:
        risk = "medium"
    else:
        risk = "low"

    return temp_mean, soil_mean, risk

def upsert_summary(temp_mean, soil_mean, risk):
    now_iso = datetime.now(timezone.utc).isoformat()
    entity = {
      "id": f"urn:ngsi-ld:PlotFireRiskSummary:plot001",
      "type": "PlotFireRiskSummary",
      "plotRef": {
        "type": "Relationship",
        "object": PLOT_ID
      },
      "temperatureMean": {
        "type": "Property",
        "value": temp_mean
      },
      "soilMoistureMean": {
        "type": "Property",
        "value": soil_mean
      },
      "riskLevel": {
        "type": "Property",
        "value": risk
      },
      "calculatedAt": {
        "type": "Property",
        "value": now_iso
      }
    }

    # Upsert vía /entityOperations/upsert
    url = f"{BROKER_ORGB}/entityOperations/upsert"
    payload = [entity]
    r = requests.post(url, json=payload, headers=HEADERS_POST, params={"options": "update"})
    if r.status_code not in (200, 201, 204):
        print("Error upserting summary in OrgB:", r.status_code, r.text)

def loop_connector():
    while True:
        try:
            obs = fetch_observations()
            temp_mean, soil_mean, risk = compute_summary(obs)
            print("Summary:", temp_mean, soil_mean, risk)
            upsert_summary(temp_mean, soil_mean, risk)
        except Exception as e:
            print("Error in connector loop:", e)
        time.sleep(30)  # cada 30 segundos

if __name__ == "__main__":
    loop_connector()
