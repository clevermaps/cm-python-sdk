import json
import requests

from .exceptions import AccessTokenException

class Client:

    def __init__(self, access_token, server_url):

        self.base_url = server_url
        self.bearer_token = self._get_token(access_token)

    def _get_token(self, access_token):

        params = {
            "refresh_token": access_token
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "CleverMaps Python SDK"
        }

        try:
            resp = self.make_request(method='post', url='/rest/oauth/token', params=params, headers=headers)
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 401:
                raise AccessTokenException('Verification of the access token was not successful. Please check if the access token value is valid.')
        except Exception as ex:
            raise ex

        return resp.json()['access_token']


    def http_request(self, method, url, params, headers):

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(self.bearer_token),
                "User-Agent": "CleverMaps Python SDK"
            }

        if method == 'post':
            resp = requests.post(url='{}{}'.format(self.base_url, url), data=json.dumps(params), headers=headers)
        elif method == 'get':
            #resp = requests.get(url='{}{}'.format(self.base_url, url), params=json.dumps(params), headers=headers)
            resp = requests.get(url='{}{}'.format(self.base_url, url), params=params, headers=headers)

        resp.raise_for_status()

        return resp

    def paginate(self, method, url, params, headers):

        first_page = self.http_request(method=method, url=url, params=params, headers=headers)
        yield first_page

        links = first_page.json()['links']
        while [l for l in links if l['rel'] == 'next']:
            next_url = next(l['href'] for l in links if l['rel'] == 'next')
            next_page = self.http_request(method=method, url=next_url, params=params, headers=headers)
            links = next_page.json()['links']
            yield next_page


    def make_request_page(self, method, url, params={}, headers={}):

        pages = self.paginate(method, url, params, headers)

        return list(pages)

    def make_request(self, method, url, params={}, headers={}):

        return self.http_request(method=method, url=url, params=params, headers=headers)