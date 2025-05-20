import json
import requests
from urllib.parse import urlparse
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_result

from .exceptions import AccessTokenException


class Client:

    def __init__(self, access_token, server_url=None, retry_count=360, retry_wait=5):

        #self.base_url = self._get_server_url(server_url)
        self.base_url = server_url
        self.session = requests.Session()
        self.retry_count = retry_count
        self.retry_wait = retry_wait
        self.bearer_token = self._get_token(access_token)

    def _get_server_url(self, server_url):

        valid_urls = ["https://secure.clevermaps.io", "https://staging.clevermaps.io"]

        if not server_url:
            return valid_urls[0]
        elif server_url and server_url not in valid_urls:
            return valid_urls[0]
        
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
            return resp.json()['access_token']
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 401:
                raise AccessTokenException('Verification of the access token was not successful. Please check if the access token value is valid.')
        except Exception as ex:
            raise ex
    

    def http_request_retry(self, method, url, params, headers, retry_enabled):

        http_retry = retry(
            stop=stop_after_attempt(self.retry_count),
            wait=wait_fixed(self.retry_wait),
            retry=retry_if_result(lambda r: r.status_code in [404])
        )

        if retry_enabled:
            http_request_retry = http_retry(self.http_request)
            return http_request_retry(method, url, params, headers)
        else:
            return self.http_request(method, url, params, headers)


    def http_request(self, method, url, params, headers):

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(self.bearer_token),
                "User-Agent": "CleverMaps Python SDK"
            }

        url='{}{}'.format(self.base_url, url) if not bool(urlparse(url).netloc) else url

        if method == 'post':
            resp = self.session.post(url, data=json.dumps(params), headers=headers)
        elif method == 'get':
            resp = self.session.get(url, params=params, headers=headers)
        elif method == 'put':
            resp = self.session.put(url, data=params, headers=headers)
        elif method == 'delete':
            resp = self.session.delete(url, headers=headers)

        return resp
    

    def paginate(self, method, url, params, headers, retry_enabled):

        first_page = self.http_request_retry(method=method, url=url, params=params, headers=headers, retry_enabled=retry_enabled)
        
        first_page.raise_for_status()
        yield first_page

        links = first_page.json()['links']
        while [l for l in links if l['rel'] == 'next']:
            next_url = next(l['href'] for l in links if l['rel'] == 'next')
            next_page = self.http_request_retry(method=method, url=next_url, params={}, headers=headers, retry_enabled=retry_enabled)
            next_page.raise_for_status()
            links = next_page.json()['links']
            yield next_page


    def make_request_page(self, method, url, params={}, headers={}, retry_enabled=False):

        pages = self.paginate(method, url, params, headers, retry_enabled=retry_enabled)

        return list(pages)
    

    def make_request(self, method, url, params={}, headers={}, retry_enabled=False):

        resp = self.http_request_retry(method=method, url=url, params=params, headers=headers, retry_enabled=retry_enabled)

        resp.raise_for_status()

        return resp