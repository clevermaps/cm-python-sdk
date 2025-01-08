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


    def get_metadata(self, url):

        resp = self.client.make_request('get', url=url)

        # return as raw response because of headers are needed in update metadata
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
    
    
    def create_metadata(self, url, create_metadata_json):

        resp = self.client.make_request('post', url=url, params=create_metadata_json)

        return resp
    

class _Metrics(_MetadataBase):

    def get_metric_by_name(self, metric_name):

        url = '{}/metrics?name={}'.format(self.md_url, metric_name)

        return self.get_metadata(url)
    

    def list_metrics(self):

        url = '{}/metrics'.format(self.md_url)

        return self.list_metadata(url)
    

    def update_metric(self, metric_name, md_json):

        resp = self.get_metric_by_name(metric_name)

        url = '{}/metrics/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, md_json)
    

    def create_metric(self, md_json):

        url = '{}/metrics'.format(self.md_url)

        resp = self.create_metadata(url, md_json)

        return resp.json()
    

class _Indicators(_MetadataBase):

    def get_indicator_by_name(self, indicator_name):

        url = '{}/indicators?name={}'.format(self.md_url, indicator_name)

        return self.get_metadata(url)
    

    def list_indicators(self):

        url = '{}/indicators'.format(self.md_url)

        return self.list_metadata(url)
    

    def update_indicator(self, indicator_name, md_json):

        resp = self.get_indicator_by_name(indicator_name)

        url = '{}/indicators/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, md_json)
    
    
    def create_indicator(self, md_json):

        url = '{}/indicators'.format(self.md_url)

        resp = self.create_metadata(url, md_json)

        return resp.json()
    

class _IndicatorDrills(_MetadataBase):

    def get_indicator_drill_by_name(self, indicator_drill_name):

        url = '{}/indicatorDrills?name={}'.format(self.md_url, indicator_drill_name)

        return self.get_metadata(url)
    

    def list_indicator_drills(self):

        url = '{}/indicatorDrills'.format(self.md_url)

        return self.list_metadata(url)
    

    def update_indicator_drill(self, indicator_drill_name, md_json):

        resp = self.get_indicator_by_name(indicator_drill_name)

        url = '{}/indicatorDrills/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, md_json)
    

    def create_indicator_drill(self, md_json):

        url = '{}/indicatorDrills'.format(self.md_url)

        resp = self.create_metadata(url, md_json)

        return resp.json()
    

class _Views(_MetadataBase):

    def get_view_by_name(self, view_name):

        url = '{}/views?name={}'.format(self.md_url, view_name)

        return self.get_metadata(url)
    
    
    def list_views(self):

        url = '{}/views'.format(self.md_url)

        return self.list_metadata(url)
    
    
    def update_view(self, view_name, md_json):

        resp = self.get_view_by_name(view_name)

        url = '{}/views/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, md_json)
    

    def create_view(self, md_json):

        url = '{}/views'.format(self.md_url)

        resp = self.create_metadata(url, md_json)

        return resp.json()


class _Maps(_MetadataBase):

    def get_map_by_name(self, map_name):

        url = '{}/maps?name={}'.format(self.md_url, map_name)

        return self.get_metadata(url)

    def list_maps(self):

        url = '{}/maps'.format(self.md_url)

        return self.list_metadata(url)
    
    
    def update_map(self, map_name, md_json):

        resp = self.get_map_by_name(map_name)

        url = '{}/maps/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, md_json)
    

    def create_map(self, md_json):

        url = '{}/maps'.format(self.md_url)

        resp = self.create_metadata(url, md_json)

        return resp.json()


class _Dashboards(_MetadataBase):

    def get_dashboard_by_name(self, dashboard_name):

        url = '{}/dashboards?name={}'.format(self.md_url, dashboard_name)

        return self.get_metadata(url)

    def list_dashboards(self):

        url = '{}/dashboards'.format(self.md_url)

        return self.list_metadata(url)
    
    
    def update_dashboard(self, dashboard_name, md_json):

        resp = self.get_dashboard_by_name(dashboard_name)

        url = '{}/dashboards/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, md_json)
    

    def create_dashboard(self, md_json):

        url = '{}/dashboards'.format(self.md_url)

        resp = self.create_metadata(url, md_json)

        return resp.json()


class _Datasets(_MetadataBase):

    def get_dataset_by_name(self, dataset_name):

        url = '{}/datasets?name={}'.format(self.md_url, dataset_name)

        return self.get_metadata(url)

    
    def list_datasets(self):

        url = '{}/datasets'.format(self.md_url)

        return self.list_metadata(url)
    
    
    def update_dataset(self, dataset_name, md_json):

        resp = self.get_dataset_by_name(dataset_name)

        url = '{}/datasets/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, md_json)
    

    def create_dataset(self, md_json):

        url = '{}/datasets'.format(self.md_url)

        resp = self.create_metadata(url, md_json)

        return resp.json()


class _Exports(_MetadataBase):

    def list_exports(self):

        url = '{}/exports'.format(self.md_url)

        return self.list_metadata(url)
    

class _ProjectSettings(_MetadataBase):

    def get_project_settings_by_name(self, project_settings_name):

        url = '{}/projectSettings?name={}'.format(self.md_url, project_settings_name)

        return self.get_metadata(url)
    

    def list_project_settings(self):

        url = '{}/projectSettings'.format(self.md_url)

        return self.list_metadata(url)
    
    
    def update_project_settings(self, project_settings_name, md_json):

        resp = self.get_project_settings_by_name(project_settings_name)

        url = '{}/projectSettings/{}'.format(self.md_url, resp.json()['id'])

        return self.update_metadata(resp, url, md_json)
    

    def create_project_settings(self, md_json):

        url = '{}/projectSettings'.format(self.md_url)

        resp = self.create_metadata(url, md_json)

        return resp.json()



