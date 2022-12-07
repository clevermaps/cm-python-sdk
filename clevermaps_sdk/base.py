from . import projects

class Base:

    def __init__(self, client, project_id):

        self.client = client
        self.project_id = project_id
        project = projects.Project(self.client)
        project_config = project.get_project_by_id(project_id)
        self.md_url = project_config['services']['md']
        self.dwh_url = project_config['services']['dwh']