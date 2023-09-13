import time
from collections import OrderedDict
from . import dwh, jobs, export, metadata, search, client, projects

from .exceptions import ExportException, InvalidDwhQueryException, DataUploadException, DataDumpException


class Sdk:

    def __init__(self, access_token, project_id=None, server_url=None):

        valid_urls = ["https://secure.clevermaps.io", "https://staging.clevermaps.io"]

        if not server_url:
            server_url = valid_urls[0]
        elif server_url and server_url not in valid_urls:
            server_url = valid_urls[0]

        self.client = client.Client(access_token, server_url)

        if project_id:

            self.project_id = project_id

            self.projects = projects.Projects(self.client)
            self.project = projects.Project(self.client)

            self.queries = dwh.Queries(self.client, self.project_id)
            self.property_values = dwh.PropertyValues(self.client, self.project_id)
            self.available_datasets = dwh.AvailableDatasets(self.client, self.project_id)
            self.data_upload = dwh.DataUpload(self.client, self.project_id)
            self.jobs = jobs.Jobs(self.client, self.project_id)
            self.job_detail = jobs.JobDetail(self.client, self.project_id)
            self.export_data = export.ExportData(self.client, self.project_id)
            self.metrics = metadata.Metrics(self.client, self.project_id)
            self.datasets = metadata.Datasets(self.client, self.project_id)
            self.search = search.Search(self.client, self.project_id)
        else:
            self.projects = projects.Projects(self.client)
            self.project = projects.Project(self.client)


    def _get_query_content(self, properties_names, metric_names, filter_by, validate=True):

        if validate:
            invalid_props = self._validate_query_properties(properties_names)
            invalid_metrics = self._validate_query_metrics(metric_names)
            invalid_filter_props = self._validate_query_properties([f['property'] for f in filter_by])

            if invalid_props or invalid_metrics or invalid_filter_props:
                raise InvalidDwhQueryException('Query definition is invalid. Invalid properties: {}. Invalid metrics: {}. Invalid filter properties: {}.'.format(
                        invalid_props, invalid_metrics, invalid_filter_props))

        metrics = []
        for m in metric_names:
            metrics.append({
                "id": m,
                "type": "metric",
                "metric": "/rest/projects/{}/md/metrics?name={}".format(self.project_id, m)
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
    

    def _validate_query_metrics(self, metrics):

        metrics_md = self.metrics.list_metrics()

        metrics_diff = list(set(metrics).difference(set([m['name'] for m in metrics_md])))

        return metrics_diff
    

    def _validate_query_properties(self, properties):

        invalid_props = []

        datasets_mds = self.datasets.list_datasets()
        for prop in properties:
            ds = prop.split('.')[0]
            if ds not in [d['name'] for d in datasets_mds]:
                invalid_props.append(prop)
                continue

            ds_md = next(d for d in datasets_mds if d['name'] == ds)
            ds_md_props = [dp['name'] for dp in ds_md['ref']['properties']]

            p = prop.split('.')[1]
            if p not in ds_md_props:
                invalid_props.append(prop)

        return invalid_props
    

    def query(self, config, limit=1000, validate=True):

        props = config.get('properties', [])
        metrics = config.get('metrics', [])
        filter_by = config.get('filter_by', [])

        query_content = self._get_query_content(props, metrics, filter_by, validate)
        print(query_content)

        location = self.queries.accept_queries(query_content, limit)
        res = self.queries.get_queries(location)

        # Response does not preserve properties order, fix it back
        props_order = [p['id'] for p in query_content['properties']]

        res_reordered = []
        for r in res:
            res_reordered.append(dict(OrderedDict((k, r['content'][k]) for k in props_order)))

        return res_reordered
    

    def get_property_values(self, property_name):

        location = self.property_values.accept_property_values(property_name)
        res = self.property_values.get_property_values(location)

        return res['content']
    

    def get_available_datasets(self, metric_name):

        res = self.available_datasets.get_available_datasets(metric_name)
        datasets = [dataset['name'] for dataset in res['content'][0]['availableDatasets'] if dataset]

        return datasets
    

    def export_to_csv(self, config):

        query_content = self._get_query_content(config['query'].get('properties', []),
                                                config['query'].get('metrics', []),
                                                config['query'].get('filter_by', []))

        job_resp = self.jobs.start_new_export_job(query_content, config['filename'], config['format'])

        while True:
            job_status = self.job_detail.get_job_status(job_resp['links'][0]['href'])

            if job_status['status'] == 'SUCCEEDED':
                return self.export_data.get_export_data(job_status['result']['exportResult'])
            elif job_status['status'] in ('FAILED', 'TIMED_OUT', 'ABORTED'):
                raise ExportException(job_status)

            time.sleep(5)


    def upload_data(self, dataset, mode, file, csv_options={}):

        upload_link = self.data_upload.upload(file)

        job_resp = self.jobs.start_new_data_pull_job(dataset, mode, upload_link, csv_options)

        while True:
            job_status = self.job_detail.get_job_status(job_resp['links'][0]['href'])
            print(job_status)

            if job_status['status'] == 'SUCCEEDED':
                return job_status
            elif job_status['status'] in ('FAILED', 'TIMED_OUT', 'ABORTED'):
                raise DataUploadException(job_status)

            time.sleep(5)


    def dump_data(self, dataset):

        job_resp = self.jobs.start_new_data_dump_job(dataset)

        while True:
            job_status = self.job_detail.get_job_status(job_resp['links'][0]['href'])
            print(job_status)

            if job_status['status'] == 'SUCCEEDED':
                return self.export_data.get_export_data(job_status['result']['links'][0]['href'])
            elif job_status['status'] in ('FAILED', 'TIMED_OUT', 'ABORTED'):
                raise DataDumpException(job_status)

            time.sleep(5)

