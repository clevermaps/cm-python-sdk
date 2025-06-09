from . import projects
import json
from pydantic.utils import deep_update



class Metadata:

    def __init__(self, client, project_id):
        
        self.client = client
        self.project_id = project_id

        self.metrics = _Metrics(self.client, project_id)
        self.indicators = _Indicators(self.client, project_id)
        self.indicator_drills = _IndicatorDrills(self.client, project_id)
        self.views = _Views(self.client, project_id)
        self.maps = _Maps(self.client, project_id)
        self.dashboards = _Dashboards(self.client, project_id)
        self.datasets = _Datasets(self.client, project_id)
        self.exports = _Exports(self.client, project_id)
        self.project_settings = _ProjectSettings(self.client, project_id)


class _MetadataBase:

    def __init__(self, client, project_id):

        project = projects.Projects(client).project
        project_config = project.get_project_by_id(project_id)

        self.client = client
        self.project_id = project_id
        self.md_url = project_config['services']['md']
        self.dwh_url = project_config['services']['dwh']


    def _get_metadata(self, url):

        resp = self.client.make_request('get', url=url)

        # return as raw response because of headers are needed in update metadata
        return resp
    

    def _list_metadata(self, url):

        resp = self.client.make_request_page('get', url=url)

        results = []

        for page in resp:
            content = page.json()['content']
            results.extend(content)

        return results
    
    
    def _update_metadata(self, get_metadata_resp, update_metadata_url, update_metadata_json):

        http_etag = get_metadata_resp.headers['ETag']
        metadata_json = get_metadata_resp.json()
        #metadata_json.update(update_metadata_json)
        metadata_json = deep_update(metadata_json, update_metadata_json)

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
    
    
    def _create_metadata(self, url, create_metadata_json):

        resp = self.client.make_request('post', url=url, params=create_metadata_json)

        return resp
    
    
    def _delete_metadata(self, url):

        resp = self.client.make_request('delete', url)

        return resp.status_code
    

    def get_by_name(self, md_type, md_name):

        url = '{}/{}?name={}'.format(self.md_url, md_type, md_name)

        return self._get_metadata(url)
    
    
    def list(self, md_type):

        url = '{}/{}'.format(self.md_url, md_type)

        return self._list_metadata(url)
    

    def create(self, md_type, md_json):

        url = '{}/{}'.format(self.md_url, md_type)

        resp = self._create_metadata(url, md_json)

        return resp.json()


    def update(self, md_type, md_name, md_json):

        resp = self.get_by_name(md_name)

        url = '{}/{}/{}'.format(self.md_url, md_type, resp.json()['id'])

        return self._update_metadata(resp, url, md_json)

    
    def delete(self, md_type, md_name):

        md_id = self.get_by_name(md_name).json()['id']

        url = '{}/{}/{}'.format(self.md_url, md_type, md_id)

        return self._delete_metadata(url)


class _Metrics(_MetadataBase):

    def __init__(self, client, project_id):

        super().__init__(client, project_id)

        self.md_type = 'metrics'
    
    def get_by_name(self, md_name):

        return super().get_by_name(self.md_type, md_name)

    def list(self):

        return super().list(self.md_type)
    
    def create(self, md_json):

        return super().create(self.md_type, md_json)
    
    def update(self, md_name, md_json):

        return super().update(self.md_type, md_name, md_json)
    
    def delete(self, md_name):

        return super().delete(self.md_type, md_name)
    

class _Indicators(_MetadataBase):

    def __init__(self, client, project_id):

        super().__init__(client, project_id)

        self.md_type = 'indicators'
    
    def get_by_name(self, md_name):

        return super().get_by_name(self.md_type, md_name)

    def list(self):

        return super().list(self.md_type)
    
    def create(self, md_json):

        return super().create(self.md_type, md_json)
    
    def update(self, md_name, md_json):

        return super().update(self.md_type, md_name, md_json)
    
    def delete(self, md_name):

        return super().delete(self.md_type, md_name)
    

class _IndicatorDrills(_MetadataBase):

    def __init__(self, client, project_id):

        super().__init__(client, project_id)

        self.md_type = 'indicatorDrills'
    
    def get_by_name(self, md_name):

        return super().get_by_name(self.md_type, md_name)

    def list(self):

        return super().list(self.md_type)
    
    def create(self, md_json):

        return super().create(self.md_type, md_json)
    
    def update(self, md_name, md_json):

        return super().update(self.md_type, md_name, md_json)
    
    def delete(self, md_name):

        return super().delete(self.md_type, md_name)
    

class _Views(_MetadataBase):

    def __init__(self, client, project_id):

        super().__init__(client, project_id)

        self.md_type = 'views'
    
    def get_by_name(self, md_name):

        return super().get_by_name(self.md_type, md_name)

    def list(self):

        return super().list(self.md_type)
    
    def create(self, md_json):

        return super().create(self.md_type, md_json)
    
    def update(self, md_name, md_json):

        return super().update(self.md_type, md_name, md_json)
    
    def delete(self, md_name):

        return super().delete(self.md_type, md_name)


class _Maps(_MetadataBase):

    def __init__(self, client, project_id):

        super().__init__(client, project_id)

        self.md_type = 'maps'
    
    def get_by_name(self, md_name):

        return super().get_by_name(self.md_type, md_name)

    def list(self):

        return super().list(self.md_type)
    
    def create(self, md_json):

        return super().create(self.md_type, md_json)
    
    def update(self, md_name, md_json):

        return super().update(self.md_type, md_name, md_json)
    
    def delete(self, md_name):

        return super().delete(self.md_type, md_name)


class _Dashboards(_MetadataBase):

    def __init__(self, client, project_id):

        super().__init__(client, project_id)

        self.md_type = 'dashboards'
    
    def get_by_name(self, md_name):

        return super().get_by_name(self.md_type, md_name)

    def list(self):

        return super().list(self.md_type)
    
    def create(self, md_json):

        return super().create(self.md_type, md_json)
    
    def update(self, md_name, md_json):

        return super().update(self.md_type, md_name, md_json)
    
    def delete(self, md_name):

        return super().delete(self.md_type, md_name)


class _Datasets(_MetadataBase):

    def __init__(self, client, project_id):

        super().__init__(client, project_id)

        self.md_type = 'datasets'
    
    def get_by_name(self, md_name):

        return super().get_by_name(self.md_type, md_name)

    def list(self):

        return super().list(self.md_type)
    
    def create(self, md_json):

        return super().create(self.md_type, md_json)
    
    def update(self, md_name, md_json):

        return super().update(self.md_type, md_name, md_json)
    
    def delete(self, md_name):

        return super().delete(self.md_type, md_name)


class _Exports(_MetadataBase):

    def __init__(self, client, project_id):

        super().__init__(client, project_id)

        self.md_type = 'exports'
    
    def get_by_name(self, md_name):

        return super().get_by_name(self.md_type, md_name)

    def list(self):

        return super().list(self.md_type)
    
    def create(self, md_json):

        return super().create(self.md_type, md_json)
    
    def update(self, md_name, md_json):

        return super().update(self.md_type, md_name, md_json)
    
    def delete(self, md_name):

        return super().delete(self.md_type, md_name)
    

class _ProjectSettings(_MetadataBase):

    def __init__(self, client, project_id):

        super().__init__(client, project_id)

        self.md_type = 'projectSettings'
    
    def get_by_name(self, md_name):

        return super().get_by_name(self.md_type, md_name)

    def list(self):

        return super().list(self.md_type)
    
    def create(self, md_json):

        return super().create(self.md_type, md_json)
    
    def update(self, md_name, md_json):

        return super().update(self.md_type, md_name, md_json)

    def delete(self, md_name):

        return super().delete(self.md_type, md_name)

