import json
import requests


class Client:

    def __init__(self, access_token, server_url):

        self.base_url = server_url
        self.bearer_token = self._get_token(access_token)

    def _get_token(self, access_token):

        data = {
            "refresh_token": access_token
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "CleverMaps Python SDK"
        }

        resp = self.make_request(method='post', url='/rest/oauth/token', data=data, headers=headers)

        return resp.json()['access_token']


    def http_request(self, method, url, data, headers):

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(self.bearer_token),
                "User-Agent": "CleverMaps Python SDK"
            }

        if method == 'post':
            resp = requests.post(url='{}{}'.format(self.base_url, url), data=json.dumps(data), headers=headers)
        elif method == 'get':
            resp = requests.get(url='{}{}'.format(self.base_url, url), params=json.dumps(data), headers=headers)

        resp.raise_for_status()

        return resp

    def paginate(self, method, url, data={}, headers=None):

        first_page = self.http_request(method, url, data, headers)
        yield first_page
        first_page_json = first_page.json()
        if 'page' in first_page_json:
            num_pages = first_page.json()['page']['totalPages']

            for page in range(2, num_pages + 1):
                next_page = self.http_request(method, url, data, headers)
                yield next_page

    def make_request(self, method, url, data={}, headers=None):

        pages = list(self.paginate(method, url, data, headers))

        if len(pages) == 1:
            return pages[0]
        else:
            return pages

