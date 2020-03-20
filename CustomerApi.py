
class CustomerApi:

    endpoint = "Customer.json"

    def __init__(self, client):
        self.client = client

    def get_customer(self, customer_id):
        return self.client.get(self.endpoint, payload={
            "customerID": customer_id,
            "load_relations": "all"
        })
