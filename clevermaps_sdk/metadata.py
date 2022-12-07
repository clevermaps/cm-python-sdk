from . import base


class Metrics(base.Base):

    def get_metric_by_name(self, metric_name):

        url = '{}/metrics?name={}'.format(self.md_url, metric_name)
        resp = self.client.make_request('get', url=url)

        return resp.json()

    def list_metrics(self):

        url = '{}/metrics'.format(self.md_url)
        resp = self.client.make_request('get', url=url)

        return resp.json()['content']


class Exports(base.Base):

    def list_exports(self):

        url = '{}/exports'.format(self.md_url)
        resp = self.client.make_request('get', url=url)

        return resp.json()['content']


class Datasets(base.Base):

    def get_dataset_by_name(self, dataset_name):

        url = '{}/datasets?name={}'.format(self.md_url, dataset_name)
        resp = self.client.make_request('get', url=url)

        return resp.json()

    def list_datasets(self):

        url = '{}/datasets'.format(self.md_url)
        resp = self.client.make_request('get', url=url)

        return resp.json()['content']
