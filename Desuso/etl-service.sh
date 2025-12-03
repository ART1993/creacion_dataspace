curl -X POST \
  'http://localhost:1026/ngsi-ld/v1/subscriptions/' \
  -H 'Content-Type: application/ld+json' \
  -d '{
    "@context": [
      "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
    ],
    "id": "urn:ngsi-ld:Subscription:soilMoistureSimple",
    "type": "Subscription",
    "entities": [
      { "type": "Observation" }
    ],
    "notification": {
      "attributes": [
        "result",
        "observedProperty",
        "phenomenonTime",
        "madeBySensor",
        "observedFeatureOfInterest"
      ],
      "endpoint": {
        "uri": "http://etl-service:8000/notify",
        "accept": "application/ld+json"
      }
    }
  }'
