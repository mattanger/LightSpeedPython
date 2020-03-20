class EmployeeApi:

    endpoint = 'Employee.json'

    def __init__(self, client):
        self.client = client

    def get_employee(self, employeeId):
        return self.client.get(endpoint=self.endpoint, payload={
            "employeeID": employeeId,
            "load_relations": '["Contact"]'
        })