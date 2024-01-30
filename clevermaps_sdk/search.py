
class Search:

    def __init__(self, client, project_id):

        self.client = client
        self.search = _Search(self.client, project_id)


class _Search:

    def __init__(self, client, project_id):

        self.client = client
        self.project_id = project_id

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