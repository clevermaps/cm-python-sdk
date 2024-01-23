import json
import requests
from urllib.parse import urlparse
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_result

from .exceptions import AccessTokenException

RETRY_COUNT = 0
RETRY_WAIT = 0

class Client:

    def __init__(self, access_token, server_url, retry_count, retry_wait):

        self.base_url = server_url
        self.bearer_token = self._get_token(access_token)

        RETRY_COUNT = retry_count
        RETRY_WAIT = retry_wait

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
    

    def retry_if_result_is_code(result):
        
        retry_on_codes = [404]

        return result.status_code in retry_on_codes
    

    @retry(
        stop=stop_after_attempt(RETRY_COUNT),
        wait=wait_fixed(RETRY_WAIT),
        retry=retry_if_result(retry_if_result_is_code)
    )
    def http_request(self, method, url, params, headers):

        session = requests.Session()

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(self.bearer_token),
                "User-Agent": "CleverMaps Python SDK"
            }

        url='{}{}'.format(self.base_url, url) if not bool(urlparse(url).netloc) else url

        if method == 'post':
            resp = session.post(url, data=json.dumps(params), headers=headers)
        elif method == 'get':
            resp = session.get(url, params=params, headers=headers)
        elif method == 'put':
            resp = session.put(url, data=params, headers=headers)

        #resp.raise_for_status()

        return resp
    

    def paginate(self, method, url, params, headers):

        first_page = self.http_request(method=method, url=url, params=params, headers=headers)
        first_page.raise_for_status()
        yield first_page

        links = first_page.json()['links']
        while [l for l in links if l['rel'] == 'next']:
            next_url = next(l['href'] for l in links if l['rel'] == 'next')
            next_page = self.http_request(method=method, url=next_url, params={}, headers=headers)
            next_page.raise_for_status()
            links = next_page.json()['links']
            yield next_page


    def make_request_page(self, method, url, params={}, headers={}):

        pages = self.paginate(method, url, params, headers)

        return list(pages)
    

    def make_request(self, method, url, params={}, headers={}):

        resp = self.http_request(method=method, url=url, params=params, headers=headers)

        resp.raise_for_status()

        return resp