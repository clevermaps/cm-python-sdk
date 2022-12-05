from . import base


class Metrics(base.Base):

    def get_metric_by_name(self, metric_name):

        url = '/rest/projects/{}/md/metrics?name={}'.format(self.client.project_id, metric_name)
        resp = self.client.make_request('get', url=url)

        return resp.json()

    def list_metrics(self):

        url = '/rest/projects/{}/md/metrics'.format(self.client.project_id)
        resp = self.client.make_request('get', url=url)

        return resp.json()['content']


class Exports(base.Base):

    def list_exports(self):

        url = '/rest/projects/{}/md/exports'.format(self.client.project_id)
        resp = self.client.make_request('get', url=url)

        return resp.json()['content']


class Datasets(base.Base):

    def get_dataset_by_name(self, dataset_name):

        url = '/rest/projects/{}/md/datasets?name={}'.format(self.client.project_id, dataset_name)
        resp = self.client.make_request('get', url=url)

        return resp.json()

    def list_datasets(self):

        url = '/rest/projects/{}/md/datasets'.format(self.client.project_id)
        resp = self.client.make_request('get', url=url)

        return resp.json()['content']
