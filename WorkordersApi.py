
class WorkOrdersApi():
    """
    Class is the interface for talking to the work orders
    api in lightspeed.
    """
    endpoint = "Workorder.json"

    def __init__(self, client):
        self.client = client

    def get_workorders(self, params={}, limit=100, offset=0):
        params["limit"] = limit
        params["offset"] = offset
        return self.client.get(self.endpoint, params)

    def get_workorders_2(self, params={}, limit=100, offset=0):
        workorders = []
        r = self.get_workorders(params, limit, offset)
        if r is None:
            return []
        wo = r.json()
        if 'Workorder' not in wo:
            return []
        attrib = wo["@attributes"]
        if int(attrib['count']) <= 100:
            return wo["Workorder"]
        workorders = wo['Workorder']
        count = int(attrib['count'])
        while offset <= count:
            offset = offset + 100
            r = self.get_workorders(params, limit, offset)
            w = r.json()
            if 'Workorder' in w:
                workorders = workorders + w['Workorder']
        return workorders
