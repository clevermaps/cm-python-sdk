
def get_query_content(project_id, properties_names, metric_names, filter_by):

    metrics = []
    for m in metric_names:
        metrics.append({
            "id": m,
            "type": "metric",
            "metric": "/rest/projects/{}/md/metrics?name={}".format(project_id, m)
        })

    properties = []
    for prop in properties_names:
        properties.append(
            {
                'id': prop.replace('.', '_'),
                'type': 'property',
                'value': prop
            }
        )

    query = {
        "properties": properties + metrics,
        "filterBy": filter_by
    }

    return query