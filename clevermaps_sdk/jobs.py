from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_result
import logging

logger = logging.getLogger("cm-python-sdk")
logger.propagate = True
logger.setLevel(logging.DEBUG)

class Jobs:
    
    def __init__(self, client, project_id):
        
        self.client = client
        
        self.jobs = _Jobs(self.client, project_id)
        self.job_detail = _JobDetail(self.client, project_id)
        self.job_history = _JobHistory(self.client, project_id)
    

class _JobsBase:
    
  def __init__(self, client, project_id):

        self.client = client
        self.project_id = project_id


class _Jobs(_JobsBase):

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
    

    def start_new_import_project_job(self, project_id, source_project_id):
        
        url = '/rest/jobs'

        params = {
            "type": "importProject",
            "projectId": project_id,
            "content": {
              "sourceProjectId": source_project_id,
              "force": True
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


class _JobDetail(_JobsBase):

    def get_job_status(self, url, retry_count=180, retry_wait=1):
        
      http_retry = retry(
          stop=stop_after_attempt(retry_count),
          wait=wait_fixed(retry_wait),
          retry=retry_if_result(lambda r: r['status'] == 'RUNNING')
      )

      get_job_status_retry = http_retry(self._get_job_status)

      return get_job_status_retry(url)
      

    def _get_job_status(self, url):

        resp = self.client.make_request('get', url=url)

        resp_json = resp.json()

        logger.debug(resp_json)

        return resp_json
    

class _JobHistory(_JobsBase):
    
    def get_job_history(self, type, account_id):
        
        url = '/rest/jobs/history'

        params = {
            "type": type,
            "projectId": self.project_id,
            "accountId": account_id
        }

        resp = self.client.make_request_page('get', url=url, params=params)

        results = []
        for page in resp:
            content = page.json()['content']
            results.extend(content)

        return results

