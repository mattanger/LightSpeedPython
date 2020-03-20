

class AccountApi:

    endpoint = "Account.json"

    def __init__(self, client):
        self.client = client

    def get_accounts(self):
        return self.client.get(self.endpoint, with_account=False).json()

    def get_account_id(self):
        r = self.get_accounts()
        if isinstance(r, list):
            r = r[0]
            return r['Account']['accountID']
        return r['Account']['accountID']
