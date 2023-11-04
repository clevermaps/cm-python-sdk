from . import base
import json


class Metadata(base.Base):

    def get_metadata(self, url):

        resp = self.client.make_request('get', url=url)

        return resp
    

    def list_metadata(self, url):

        resp = self.client.make_request_page('get', url=url)

        results = []

        for page in resp:
            content = page.json()['content']
            results.extend(content)

        return results
    
    
    def update_metadata(self, get_metadata_resp, update_metadata_url, update_metadata_json):

        http_etag = get_metadata_resp.headers['ETag']
        metadata_json = get_metadata_resp.json()
        metadata_json.update(update_metadata_json)

        headers = {
            "Authorization": "Bearer {}".format(self.client.bearer_token),
            "User-Agent": "CleverMaps Python SDK",
            'If-Match': http_etag,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CAN-STRICT-JSON-VALIDATION': 'false'
        }

        resp = self.client.make_request('put', url=update_metadata_url, params=json.dumps(metadata_json), headers=headers)

        return resp.json()
    

class Metrics(Metadata):

    def get_metric_by_name(self, metric_name):

        url = '{}/metrics?name={}'.format(self.md_url, metric_name)

        return self.get_metadata(url)
    

    def list_metrics(self):

        url = '{}/metrics'.format(self.md_url)

        return self.list_metadata(url)
    

    def update_metric(self, metric_name, metric_update_json):

        resp = self.get_metric_by_name(metric_name)

        url = '{}/metrics/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, metric_update_json)
    

class Views(Metadata):

    def get_view_by_name(self, view_name):

        url = '{}/views?name={}'.format(self.md_url, view_name)

        return self.get_metadata(url)
    
    
    def list_views(self):

        url = '{}/views'.format(self.md_url)

        return self.list_metadata(url)
    
    
    def update_view(self, view_name, view_update_json):

        resp = self.get_view_by_name(view_name)

        url = '{}/views/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, view_update_json)


class Datasets(Metadata):

    def get_dataset_by_name(self, dataset_name):

        url = '{}/datasets?name={}'.format(self.md_url, dataset_name)

        return self.get_metadata(url)

    
    def list_datasets(self):

        url = '{}/datasets'.format(self.md_url)

        return self.list_metadata(url)
    
    
    def update_dataset(self, dataset_name, dataset_update_json):

        resp = self.get_dataset_by_name(dataset_name)

        url = '{}/datasets/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, dataset_update_json)


class Exports(Metadata):

    def list_exports(self):

        url = '{}/exports'.format(self.md_url)

        return self.list_metadata(url)
