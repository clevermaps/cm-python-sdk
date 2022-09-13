from . import base


class ExportData(base.Base):

    def get_export_data(self, export_url):

        headers = {
            "Accept": "text/csv",
            "Authorization": "Bearer {}".format(self.client.bearer_token)
        }
        resp = self.client.make_request('get', url=export_url, headers=headers)

        return resp.text