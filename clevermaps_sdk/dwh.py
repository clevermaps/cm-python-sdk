from . import base


class Queries(base.Base):

    def accept_queries(self, query, size=200):

        url = '{}/queries?page=0&size={}'.format(self.dwh_url, size)
        resp = self.client.make_request('post', url=url, data=query)

        return resp.headers['location']

    def get_queries(self, location):

        # TODO muze vratit 404, pak cekat dalsich 30s a zkusit znovu
        resp = self.client.make_request('get', url=location)

        return resp.json()


class AvailableDatasets(base.Base):

    def get_available_datasets(self, metric_name):

        url = '{}/availableDatasets?expand=dataset'.format(self.dwh_url)

        data = {
            "metrics": [
                {
                    "id": metric_name,
                    "type": "metric",
                    "metric": "{}/metrics?name={}".format(self.md_url, metric_name)
                }
            ]
        }

        resp = self.client.make_request('post', url=url, data=data)

        return resp.json()


class PropertyValues(base.Base):

    # TODO filter, page, size, sort
    def accept_property_values(self, property_name):

        url = '{}/propertyValues?property={}'.format(self.dwh_url, property_name)
        resp = self.client.make_request('post', url=url)

        return resp.headers['location']

    def get_property_values(self, location):

        # TODO muze vratit 404, pak cekat dalsich 30s a zkusit znovu
        resp = self.client.make_request('get', url=location)

        return resp.json()
