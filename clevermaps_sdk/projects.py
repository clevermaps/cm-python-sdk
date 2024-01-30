
class Projects:

    def __init__(self, client):

        self.client = client
        
        self.projects = _Projects(self.client)
        self.project = _Project(self.client)
        self.members = _Members(self.client)


class _ProjectsBase:

    def __init__(self, client):

        self.client = client


class _Projects(_ProjectsBase):

    def list_projects(self):

        url = '/rest/projects'
        resp = self.client.make_request_page('get', url=url)

        results = []

        for page in resp:
            content = page.json()['content']
            results.extend(content)

        return results
    

    def create_project(self, organization_id, title, description):

        url = '/rest/projects'
        params = {
            "title": title,
            "description": description,
            "status": "ENABLED",
            "organizationId": organization_id 
        }

        resp = self.client.make_request('post', params=params, url=url)

        return resp.json()



class _Project(_ProjectsBase):

    def get_project_by_id(self, project_id):

        url = '/rest/projects/{}'.format(project_id)
        resp = self.client.make_request('get', url=url)

        return resp.json()


class _Members(_ProjectsBase):

    def list_members(self, project_id):

        url = '/rest/projects/{}/members'.format(project_id)
        resp = self.client.make_request_page('get', url=url)

        results = []

        for page in resp:
            content = page.json()['content']
            results.extend(content)

        return results
    
    def add_new_member(self, project_id, account_id, role, status):

        url = '/rest/projects/{}/members'.format(project_id)
        params = {
            'accountId': account_id,
            'role': role,
            'status': status
        }

        resp = self.client.make_request('post', params=params, url=url)

        return resp.json()
    
