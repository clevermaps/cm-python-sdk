from . import base


class AuditLog(base.Base):

    def __init__(self, client, project_id):

        self.client = client
        self.project_id = project_id

    def get_audit_log(self, event_types, account_id=None, datetime_from=None, datetime_to=None):

        url = '/rest/auditlog'

        payload = {
            'projectId': self.project_id,
            'accountId': account_id,
            'eventTypes': event_types,
            'from': datetime_from,
            'to': datetime_to
        }

        resp = self.client.make_request_page('get', url=url, params=payload)

        results = []

        for page in resp:
            content = page.json()['content']
            results.extend(content)

        return results