from clevermaps_sdk import sdk

# Your project_id (can be obtained from the url of the project or from the CleverMaps Shell)
project_id = ""
# Your access_token (https://clevermaps.docs.apiary.io/#reference/authentication)
access_token = ""

# CleverMaps SDK object initialization
cm_sdk = sdk.Sdk(access_token)

# Call some global workspace methods
print(cm_sdk.projects.projects.list_projects())
print(cm_sdk.projects.project.get_project_by_id(project_id))

# Open specific project and work with data or metadata
cm_project = cm_sdk.open(project_id)

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
print(cm_project.query(query_json))

# Export query results to the file
export_json = {
    'query': query_json,
    'filename': 'test.csv',
    'format': 'csv'
}

export_result = cm_project.export_to_csv(export_json)
with open('export.csv', 'w') as outf:
    outf.write(export_result)

# Get available datasets for the metric
print(cm_project.get_available_datasets('pois_count_metric'))

# Get property values of the column
print(cm_project.get_property_values("poi_dwh.subtype_name"))

# List all metrics in the project
print(cm_project.metadata.metrics.list_metrics())

# List all datasets in the project
print(cm_project.metadata.datasets.list_datasets())

# Fulltext search in dataset
print(cm_project.fulltext_search('poi_dwh', 'Albert'))

# Upload CSV file to CleverMaps
csv_options = {
    "header": True,
    "separator": ",",
    "quote": "\"",
    "escape": "\\"
}
with open('./data/poi_dwh.csv', 'rb') as f:
    print(cm_project.upload_data('poi_dwh', 'full', f, csv_options))

# Dump CSV file from CleverMaps
dump_result = cm_project.dump_data('poi_dwh')
with open('./data/poi_dwh_dump.csv', 'w') as outf:
    outf.write(dump_result)

# Update metadata
metric_update_json = {
    'description': 'New description'
}
print(cm_project.metadata.metrics.update_metric('pois_sum_metric', metric_update_json))

view_update_json = {
    'description': 'New description'
}
print(cm_project.metadata.views.update_view('exposure_index_view', view_update_json))

dataset_update_json = {
    'description': 'New description'
}
print(cm_project.metadata.datasets.update_dataset('poi_dwh', dataset_update_json))