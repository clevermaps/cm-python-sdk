from clevermaps_sdk import sdk

# Your project_id (can be obtained from the url of the project or from the CleverMaps Shell)
project_id = ""
# Your access_token (https://clevermaps.docs.apiary.io/#reference/authentication)
access_token = ""

# CleverMaps SDK object initialization - WITHOUT specific project
cm_sdk = sdk.Sdk(access_token)

# In this case only some endpoints are available
print(cm_sdk.projects.list_projects())
print(cm_sdk.project.get_project_by_id(project_id))

# CleverMaps SDK object initialization - WITH specific project
cm_sdk = sdk.Sdk(access_token, project_id)

# In this case all endpoints are available

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

# List all datasets in the project
print(cm_sdk.datasets.list_datasets())

# Fulltext search in dataset
print(cm_sdk.search.search('poi_dwh', 'Albert'))
