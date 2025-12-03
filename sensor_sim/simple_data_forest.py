import requests
import os
import uuid
import time
from datetime import datetime, timezone

BROKER_URL = os.getenv("BROKER_URL", "http://orionld_orga:1026/ngsi-ld/v1")

HEADERS = {
    "Content-Type": "application/ld+json",
    "Link": '<https://example.org/contexts/forest.jsonld>;'
    'rel="http://www.w3.org/ns/json-ld#context";'
    'type="application/ld+json"'
    #'"Content-Type": "application/ld+json"'
    ,"Link": '<https://example.org/contexts/forest.jsonld>; '
            'rel="http://www.w3.org/ns/json-ld#context"; '
            'type="application/ld+json"'
}

def create_entity(entity):
    r = requests.post(f"{BROKER_URL}/entities", json=entity, headers=HEADERS)
    if r.status_code not in (201, 409):  # 409 = ya existe
        print("Error creating entity", r.status_code, r.text)

def setup_forest():
    forest_plot = {
      "id": "urn:ngsi-ld:ForestPlot:plot001",
      "type": "ForestPlot",
      "name": { "type": "Property", "value": "Parcela 001" },
      "plotId": { "type": "Property", "value": "P001" },
      "areaHa": { "type": "Property", "value": 3.5 },
      "dominantSpecies": { "type": "Property", "value": "Pinus pinaster" },
      "location": {
        "type": "GeoProperty",
        "value": {
          "type": "Point",
          "coordinates": [-3.7, 40.4]
        }
      }
    }

    sensor = {
      "id": "urn:ngsi-ld:SensorDevice:sensor001",
      "type": "SensorDevice",
      "name": { "type": "Property", "value": "Sensor parcela 001" },
      "deviceModel": { "type": "Property", "value": "DemoTempV1" },
      "measurementTypes": {
        "type": "Property",
        "value": ["airTemperature", "soilMoisture"]
      },
      "installedOnPlot": {
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

    create_entity(forest_plot)
    create_entity(sensor)
