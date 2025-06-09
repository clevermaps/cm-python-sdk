class Accounts:

    def __init__(self, client):

        self.client = client

        self.accounts = _Accounts(self.client)


class _Accounts:

    def __init__(self, client):

        self.client = client


    def find_account(self, email):

        url = '/rest/accounts'
        params = {
            'email': email
        }

        resp = self.client.make_request('get', url=url, params=params)

        #return resp.json()
    
        return resp.status_code
