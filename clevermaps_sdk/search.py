from . import base


class Search(base.Base):

    def search(self, dataset, query, size=20):

        url = '/rest/projects/{}/search?query={}&dataset={}&size={}&page=0'.format(self.project_id, query, dataset, size)
        res = self.client.make_request_page('get', url)

        results = []

        for page in res:
            content = page.json()['content']
            results.extend(content)

        return results

    def geo_search(self):

        pass