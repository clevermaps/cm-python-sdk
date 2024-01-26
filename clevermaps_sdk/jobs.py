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
    
    
    def start_new_data_pull_job(self, dataset, mode, upload_link, csv_options={}):
        
        url = '/rest/jobs'

        if not csv_options:
            csv_options = {
              "header": True,
              "separator": ",",
              "quote": "\"",
              "escape": "\\"
            }

        params = {
          "type": "dataPull",
          "projectId": self.project_id,
          "content": {
            "dataset": dataset,
            "mode": mode,
            "upload": upload_link,
            "type": "csv",
            "csvOptions": csv_options
          }
        }

        resp = self.client.make_request('post', url=url, params=params)

        return resp.json()
    
    
    def start_new_data_dump_job(self, dataset):
        
        url = '/rest/jobs'

        params = {
          "type": "dataDump",
          "projectId": self.project_id,
          "content": {
            "dataset": dataset
          }
        }

        resp = self.client.make_request('post', url=url, params=params)

        return resp.json()
    
    
    def start_new_bulk_point_query_job(self, points, pointQueries):
        
        url = '/rest/jobs'

        params = {
            "type": "bulkPointQuery",
            "projectId": self.project_id,
            "content": {
                "points": points,
                "pointQueries": pointQueries
            }
        }

        resp = self.client.make_request('post', url=url, params=params)

        return resp.json()


class JobDetail(base.Base):


    def get_job_status(self, url):

        resp = self.client.make_request('get', url=url)

        return resp.json()