import json
import requests

from .exceptions import AccessTokenException

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

        try:
            resp = self.make_request(method='post', url='/rest/oauth/token', data=data, headers=headers)
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 401:
                raise AccessTokenException('Verification of the access token was not successful. Please check if the access token value is valid.')
        except Exception as ex:
            raise ex

        return resp.json()['access_token']


    def http_request(self, method, url, data, params, headers):

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
            resp = requests.get(url='{}{}'.format(self.base_url, url), params=json.dumps(params), headers=headers)

        resp.raise_for_status()

        return resp

    def paginate(self, method, url, data, headers):

        first_page = self.http_request(method=method, url=url, data=data, params={}, headers=headers)
        yield first_page

        if 'application/json' in first_page.headers.get('Content-Type', '') and 'page' in first_page.json():
            num_pages = first_page.json()['page']['totalPages']

            for page in range(2, num_pages + 1):
                next_page = self.http_request(method=method, url='{}/?page={}'.format(url, page), data=data, params={}, headers=headers)
                yield next_page

    def make_request(self, method, url, data={}, headers={}):

        pages = self.paginate(method, url, data, headers)

        pages = list(pages)
        if len(pages) == 1:
            return pages[0]
        else:
            return pages

