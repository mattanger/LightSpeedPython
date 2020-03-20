
class WorkorderStatusApi:
    """

    """
    endpoint = "WorkorderStatus.json"

    def __init__(self, client):
        self.client = client

    def get_workorder_status(self):
        return self.client.get(endpoint=self.endpoint)
