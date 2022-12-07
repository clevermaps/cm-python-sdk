from . import base


class Projects():

    def __init__(self, client):

        self.client = client

    def list_projects(self):

        url = '/rest/projects'
        resp = self.client.make_request('get', url=url)

        return resp.json()['content']

class Project():

    def __init__(self, client):

        self.client = client

    def get_project_by_id(self, project_id):

        url = '/rest/projects/{}'.format(project_id)
        resp = self.client.make_request('get', url=url)

        return resp.json()
