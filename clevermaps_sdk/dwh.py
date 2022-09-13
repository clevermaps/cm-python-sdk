from . import base


class Queries(base.Base):

    def accept_queries(self, query, size=200):

        url = '/rest/projects/{}/dwh/{}/queries?page=0&size={}'.format(self.client.project_id, self.client.dwh_id, size)
        resp = self.client.make_request('post', url=url, data=query)

        return resp.headers['location']

    def get_queries(self, location):

        # TODO muze vratit 404, pak cekat dalsich 30s a zkusit znovu
        resp = self.client.make_request('get', url=location)

        return resp.json()


class AvailableDatasets(base.Base):

    def get_available_datasets(self, metric_name):

        url = '/rest/projects/{}/dwh/{}/availableDatasets?expand=dataset'.format(self.client.project_id, self.client.dwh_id)

        data = {
            "metrics": [
                {
                    "id": metric_name,
                    "type": "metric",
                    "metric": "/rest/projects/{}/md/metrics?name={}".format(self.client.project_id, metric_name)
                }
            ]
        }

        resp = self.client.make_request('post', url=url, data=data)

        return resp.json()


class PropertyValues(base.Base):

    # TODO filter, page, size, sort
    def accept_property_values(self, property_name):

        url = '/rest/projects/{}/dwh/{}/propertyValues?property={}'.format(self.client.project_id, self.client.dwh_id, property_name)
        resp = self.client.make_request('post', url=url)

        return resp.headers['location']

    def get_property_values(self, location):

        # TODO muze vratit 404, pak cekat dalsich 30s a zkusit znovu
        resp = self.client.make_request('get', url=location)

        return resp.json()
