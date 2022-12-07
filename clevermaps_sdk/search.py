from . import base


class Search(base.Base):

    def search(self, dataset, query, size=200):

        url = '/rest/projects/{}/search?query={}&dataset={}&size={}&page=0'.format(self.project_id, query, dataset, size)
        res = self.client.make_request('get', url)

        return res.json()

    def geo_search(self):

        pass