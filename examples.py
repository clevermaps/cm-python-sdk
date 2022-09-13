from clevermaps_sdk import sdk


project_id = ""
dwh_id = "viw8l4"
server_url = "https://secure.clevermaps.io"
access_token = ""


cm_sdk = sdk.Sdk(project_id, dwh_id, access_token, server_url)

# Query
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
print(cm_sdk.query(query_json, 20000))

# Export
export_json = {
    'query': query_json,
    'filename': 'test.csv',
    'format': 'csv'
}

# export_result = cm_sdk.export_to_csv(export_json)
# with open('export.csv', 'w') as outf:
#     outf.write(export_result)

# List metrics
print(cm_sdk.metrics.list_metrics())

# Search
print(cm_sdk.search.search('poi_dwh', 'Albert'))

# Get property values
print(cm_sdk.get_property_values("poi_dwh.subtype_name"))
