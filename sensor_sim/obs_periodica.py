import random
import requests
import uuid
import time
from datetime import datetime, timezone

from sensor_sim.simple_data_forest import setup_forest, create_entity

def create_observation(observed_property, value, unit_code):
    obs_id = f"urn:ngsi-ld:Observation:{uuid.uuid4()}"
    now_iso = datetime.now(timezone.utc).isoformat()

    obs = {
      "id": obs_id,
      "type": "Observation",
      "observedProperty": {
        "type": "Property",
        "value": observed_property
      },
      "value": {
        "type": "Property",
        "value": value
      },
      "unitCode": {
        "type": "Property",
        "value": unit_code
      },
      "resultTime": {
        "type": "Property",
        "value": now_iso
      },
      "madeBySensor": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:SensorDevice:sensor001"
      },
      "observedOnPlot": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:ForestPlot:plot001"
      },
      "location": {
        "type": "GeoProperty",
        "value": {
          "type": "Point",
          "coordinates": [-3.7, 40.4]
        }
      }
    }
    create_entity(obs)

def loop_simulation():
    setup_forest()
    while True:
        temp = round(random.uniform(10, 35), 1)
        soil = round(random.uniform(0.05, 0.35), 3)
        create_observation("airTemperature", temp, "CEL")
        create_observation("soilMoisture", soil, "P1")  # parte de volumen
        print("Sent observations", temp, soil)
        time.sleep(10)  # cada 10 segundos

if __name__ == "__main__":
    loop_simulation()
