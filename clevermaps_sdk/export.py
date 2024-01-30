
class Export:

    def __init__(self, client):

        self.export_data = ExportData(client)


class ExportData:

    def __init__(self, client):

        self.client = client

    def get_export_data(self, export_url):

        headers = {
            "Accept": "text/csv",
            "Authorization": "Bearer {}".format(self.client.bearer_token)
        }
        resp = self.client.make_request('get', url=export_url, headers=headers)

        resp.encoding = 'utf-8'

        return resp.text