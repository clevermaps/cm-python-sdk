from collections import OrderedDict
import re
import datetime

from . import dwh, jobs, export, metadata, search, client, auditlog, common, projects, accounts


class Sdk:

    # Top level SDK class providing general methods managing the CleverMaps Workspace

    def __init__(self, access_token, server_url=None):

        self.client = client.Client(access_token, server_url)

        self.export = export.Export(self.client)
        self.projects = projects.Projects(self.client)
        self.accounts = accounts.Accounts(self.client)


    def open(self, project_id):

        return ProjectSdk(self.client, project_id)


class ProjectSdk():

    # Project level SDK class providing user friendly wrapper methods

    def __init__(self, client, project_id):

        self.client = client
        self.project_id = project_id

        self.export = export.Export(self.client)
        self.projects = projects.Projects(self.client)
        self.accounts = accounts.Accounts(self.client)

        self.dwh = dwh.DataWarehouse(self.client, project_id)
        self.jobs = jobs.Jobs(self.client, project_id)
        self.metadata = metadata.Metadata(self.client, project_id)

        self.search = search.Search(self.client, project_id)
        self.auditlog = auditlog.AuditLog(self.client, project_id)


    def query(self, config, limit=1000):

        props = config.get('properties', [])
        metrics = config.get('metrics', [])
        filter_by = config.get('filter_by', [])

        query_content = common.get_query_content(self.project_id, props, metrics, filter_by)

        location = self.dwh.queries.accept_queries(query_content, limit)
        res = self.dwh.queries.get_queries(location)

        # Response does not preserve properties order, fix it back
        props_order = [p['id'] for p in query_content['properties']]

        res_reordered = []
        for r in res:
            res_reordered.append(dict(OrderedDict((k, r['content'][k]) for k in props_order)))

        return res_reordered


    def get_property_values(self, property_name):

        location = self.dwh.property_values.accept_property_values(property_name)
        res = self.dwh.property_values.get_property_values(location)

        return res['content']


    def get_metric_ranges(self, query):

        props = query.get('properties', [])
        metrics = query.get('metrics', [])
        filter_by = query.get('filter_by', [])

        query_content = common.get_query_content(self.project_id, props, metrics, filter_by)

        location = self.dwh.metric_ranges.accept_metric_ranges(query_content)
        res = self.dwh.metric_ranges.get_metric_ranges(location)

        return res['content']


    def get_available_datasets(self, metric_name):

        res = self.dwh.available_datasets.get_available_datasets(metric_name)
        datasets = [dataset['name'] for dataset in res['content'][0]['availableDatasets'] if dataset]

        return datasets


    def query_points(self, points, point_queries, retry_count=180, retry_wait=1):

        for q in point_queries:
            for m in q['properties']:
                if m['type'] == 'metric' and not m['metric'].startswith('/rest'):
                    m['metric'] = "/rest/projects/{}/md/metrics?name={}".format(self.project_id, m['metric']) 

            q['filterBy'] = q.pop('filter_by')

        job_resp = self.jobs.jobs.start_new_bulk_point_query_job(points, point_queries)
        job_result = self.jobs.job_detail.get_job_status(job_resp['links'][0]['href'], retry_count, retry_wait)

        return job_result


    def export_to_csv(self, config):

        query_content = common.get_query_content(
            self.project_id,
            config['query'].get('properties', []),
            config['query'].get('metrics', []),
            config['query'].get('filter_by', [])
        )

        job_resp = self.jobs.jobs.start_new_export_job(query_content, config['filename'], config['format'])
        job_result = self.jobs.job_detail.get_job_status(job_resp['links'][0]['href'])

        return self.export.export_data.get_export_data(job_result['result']['exportResult'])


    def upload_data(self,dataset, mode, file, csv_options={}, retry_count=600, retry_wait=5):

        upload_link = self.dwh.data_upload.upload(file)

        job_resp = self.jobs.jobs.start_new_data_pull_job(dataset, mode, upload_link, csv_options)
        job_result = self.jobs.job_detail.get_job_status(job_resp['links'][0]['href'], retry_count, retry_wait)

        return job_result


    def dump_data(self, dataset):

        job_resp = self.jobs.jobs.start_new_data_dump_job(dataset)
        job_result = self.jobs.job_detail.get_job_status(job_resp['links'][0]['href'])

        return job_result


    def clone_project(self, dest_organization_id, dest_project_title=None, dest_project_description=None):

        src_project_id = self.project_id
        src_project_info = self.projects.project.get_project_by_id(self.project_id)

        if not dest_project_title: dest_project_title = '{} - {}'.format(src_project_info['title'], datetime.datetime.now().strftime("%Y-%m-%d-%H:%M"))
        if not dest_project_description: dest_project_description = src_project_info['description']

        dest_project_id = self.projects.projects.create_project(dest_organization_id, dest_project_title, dest_project_description)['id']

        job_resp = self.jobs.jobs.start_new_import_project_job(dest_project_id, src_project_id)

        self.jobs.job_detail.get_job_status(job_resp['links'][0]['href'], retry_count=30, retry_wait=10)

        return dest_project_id


    def fulltext_search(self, dataset, text):

        return self.search.search.search(dataset, text)


    def _get_metadata_clone_name(self, existing_names, current_name=None):

        similar_names = [ n for n in existing_names if current_name in n ]
        existing_number_postfixes = [ n[-1:] for n in similar_names if re.match(r'_\d', n[-2:]) ]

        if not existing_number_postfixes:
            new_name_postfix = 0
        else:
            new_name_postfix = int(sorted(existing_number_postfixes)[-1]) + 1

        new_name = '{}_{}'.format(current_name, new_name_postfix)

        return new_name


    def clone_metadata(self, metadata_type, metadata_name):

        if metadata_type == 'view':
            view_json = self.metadata.views.get_view_by_name(metadata_name).json()
            existing_views_names = [ v['name'] for v in self.metadata.views.list_views() ]

            clone_name = self._get_metadata_clone_name(existing_views_names, view_json['name'])

            view_clone_json = {
                'name': clone_name,
                'type': view_json['type'],
                'title': view_json['title'],
                'description': view_json['description'],
                'content': view_json['content']
            }
            resp = self.metadata.views.create_view(view_clone_json)

            return resp

        else:
            return 'Metadata type {} is not supported yet.'.format(metadata_type)
