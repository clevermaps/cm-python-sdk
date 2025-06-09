from . import projects
import os
import io



class DataWarehouse:

    def __init__(self, client, project_id):

        self.client = client

        self.queries = _Queries(self.client, project_id)
        self.property_values = _PropertyValues(self.client, project_id)
        self.metric_ranges = _MetricRanges(self.client, project_id)
        self.available_datasets = _AvailableDatasets(self.client, project_id)
        self.data_upload = _DataUpload(self.client, project_id)
    

class _DataWarehouseBase:

    def __init__(self, client, project_id):

        project = projects.Projects(client).project
        project_config = project.get_project_by_id(project_id)

        self.client = client
        self.project_id = project_id
        self.md_url = project_config['services']['md']
        self.dwh_url = project_config['services']['dwh']


class _Queries(_DataWarehouseBase):

    def accept_queries(self, query, size=200):

        url = '{}/queries?page=0&size={}'.format(self.dwh_url, size)
        resp = self.client.make_request('post', url=url, params=query)

        return resp.headers['location']

    def get_queries(self, location):

        resp = self.client.make_request_page('get', url=location, retry_enabled=True)

        results = []
        for page in resp:
            content = page.json()['content']
            results.extend(content)

        return results


class _AvailableDatasets(_DataWarehouseBase):

    def get_available_datasets(self, metric_name):

        url = '{}/availableDatasets?expand=dataset'.format(self.dwh_url)

        params = {
            "metrics": [
                {
                    "id": metric_name,
                    "type": "metric",
                    "metric": "{}/metrics?name={}".format(self.md_url, metric_name)
                }
            ]
        }

        resp = self.client.make_request('post', url=url, params=params)

        return resp.json()


class _PropertyValues(_DataWarehouseBase):

    # TODO filter, page, size, sort
    def accept_property_values(self, property_name):

        url = '{}/propertyValues?property={}'.format(self.dwh_url, property_name)
        resp = self.client.make_request('post', url=url)

        return resp.headers['location']

    def get_property_values(self, location):

        resp = self.client.make_request('get', url=location)

        return resp.json()


class _MetricRanges(_DataWarehouseBase):

    def accept_metric_ranges(self, query):

        url = '{}/metricRanges'.format(self.dwh_url)
        resp = self.client.make_request('post', url=url, params=query)

        return resp.headers['location']

    def get_metric_ranges(self, location):

        resp = self.client.make_request('get', url=location)

        return resp.json()


class _DataUpload(_DataWarehouseBase):

    def upload(self, file):

        if not isinstance(file, io.IOBase):
            if not os.path.isfile(file):
                raise FileNotFoundError
            else:
                file_obj = open(file, 'rb')
        else:
            file_obj = file

        url = '/rest/projects/{}/dwh/data/uploads'.format(self.project_id)

        resp = self.client.make_request('post', url=url, params=None)

        upload_url = resp.json()['uploadUrlEncoded']
        upload_link = list(filter(lambda l: l['rel'] == 'self', resp.json()['links']))[0]['href']

        headers = {
            'Content-type': 'text/csv',
            'Charset': 'utf-8'
        }

        resp = self.client.make_request('put', url=upload_url, params=file_obj, headers=headers)

        return upload_link

