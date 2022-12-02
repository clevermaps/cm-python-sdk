from clevermaps_sdk import sdk

project_id = ""
dwh_id = ""
server_url = "https://secure.clevermaps.io"
access_token = ""

# CleverMaps SDK main object initialization
cm_sdk = sdk.Sdk(project_id, dwh_id, access_token, server_url)

# Query data and metrics
query_json = {
    "properties": [
        "obec_dwh.nazev",
        "poi_dwh.type_name",
        "poi_dwh.subtype_name",
    ],
    "metrics": [
        "pois_sum_metric",
        "pois_count_metric"
    ],
    "filter_by": [
        {
            "property": "obec_dwh.nazev",
            "operator": "eq",
            "value": "Brno"
        },
        {
            "property": "poi_dwh.subtype_name",
            "operator": "in",
            "value": ["cafe", "restaurant"]
        }
    ]
}

query_json = {
  "metrics": [
      "pois_count_metric",
      "pois_sum_metric"
  ],
  "properties": [
      "poi_dwh.type_name"
  ],
  "filter_by": [
      {
          "property": "obec_dwh.nazev",
          "operator": "eq",
          "value": "Brno"
      }
  ]
}

# Print query results as json
print(cm_sdk.query(query_json))

# Export query results to the file
export_json = {
    'query': query_json,
    'filename': 'test.csv',
    'format': 'csv'
}

export_result = cm_sdk.export_to_csv(export_json)
with open('export.csv', 'w') as outf:
    outf.write(export_result)

# Get available datasets for the metric
print(cm_sdk.get_available_datasets('pois_count_metric'))

# Get property values of the column
print(cm_sdk.get_property_values("poi_dwh.subtype_name"))

# List all metrics in the project
print(cm_sdk.metrics.list_metrics())

# Fulltext search in dataset
print(cm_sdk.search.search('poi_dwh', 'Albert'))
