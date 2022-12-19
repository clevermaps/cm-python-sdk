from . import projects, exceptions

class Base:

    def __init__(self, client, project_id):

        projects_ls = projects.Projects(client).list_projects()
        if project_id not in [p['id'] for p in projects_ls]:
            raise exceptions.CleverMapsException('CleverMaps project_id {} is not valid value.'.format(project_id))

        project = projects.Project(client)
        project_config = project.get_project_by_id(project_id)

        self.client = client
        self.project_id = project_id
        self.md_url = project_config['services']['md']
        self.dwh_url = project_config['services']['dwh']