curl -X POST \
  'http://localhost:1026/ngsi-ld/v1/entities/' \
  -H 'Content-Type: application/ld+json' \
  --data @ForestPlot.jsonld