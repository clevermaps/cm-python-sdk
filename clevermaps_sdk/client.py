import json
import requests


class Client:

    def __init__(self, project_id, dwh_id, access_token, server_url):

        self.project_id = project_id
        self.dwh_id = dwh_id
        self.base_url = server_url
        self.bearer_token = self._get_token(access_token)

    def _get_token(self, access_token):

        data = {
            "refresh_token": access_token
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        resp = self.make_request(method='post', url='/rest/oauth/token', data=data, headers=headers)

        return resp.json()['access_token']

    def make_request(self, method, url, data={}, headers=None):

        if not headers:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(self.bearer_token)
            }

        if method == 'post':
            resp = requests.post(url='{}{}'.format(self.base_url, url), data=json.dumps(data), headers=headers)
        elif method == 'get':
            resp = requests.get(url='{}{}'.format(self.base_url, url), params=json.dumps(data), headers=headers)
        else:
            raise ValueError('HTTP method {} is not supported. Supported values are: [get, post]'.format(method))

        resp.raise_for_status()

        return resp