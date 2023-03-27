from . import base


class Jobs(base.Base):

    def start_new_export_job(self, query, filename, format):

        url = '/rest/jobs'

        params = {
          "type": 'export',
          "projectId": self.project_id,
          "headerTitles": False,
          "content": {
            "filename": filename,
            "format": format,
            "query": query,
            "csvOptions": {
              "header": True,
              "separator": ",",
              "quote": "\"",
              "escape": "\\"
            }
          }
        }

        resp = self.client.make_request('post', url=url, params=params)

        return resp.json()


class JobDetail(base.Base):


    def get_job_status(self, url):

        resp = self.client.make_request('get', url=url)

        return resp.json()