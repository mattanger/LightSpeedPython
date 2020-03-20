from requests_oauthlib import OAuth2Session
from flask.json import jsonify
from .LSApi import LSApiBase
from flask.json import dumps
import json
import os
auth_uri = "https://cloud.lightspeedapp.com/oauth/authorize.php"
token_uri = "https://cloud.lightspeedapp.com/oauth/access_token.php"
scopes = ["employee:workbench","employee:register_read"]
client_id = "" # lightspeed api client id 
client_secret = "" # lightspeed api client secret 
LS_CREDENTIAL_STORE = "" # path to file where tokens are stored 
REDIRECT_URI = "http://LsGcalSync-env.2cimmfibps.us-east-1.elasticbeanstalk.com/oauth"

extra = {
    'client_id': client_id,
    'client_secret': client_secret
}


class LsAuth:

    def __init__(self, cred_store_path, account_id):
        self.credential_store_path = cred_store_path
        self.client = None
        self.account_id = account_id
        if self.get_token() is None:
            self.auth_needed = True
        else:
            self.auth_needed = False

    def start_flow(self):
        ls_oauth = OAuth2Session(client_id=client_id, scope=scopes)
        authorization_url, state = ls_oauth.authorization_url(auth_uri)
        return authorization_url, state

    def retrieve_token(self, state, auth_response):
        ls = OAuth2Session(client_id, state=state)
        token = ls.fetch_token(token_uri,
                               client_secret=client_secret,
                               authorization_response=auth_response)
        self.token_saver(token)
        return token

    def get_session(self):
        token = self.get_token()
        ls = OAuth2Session(client_id=client_id,
                           token=token,
                           auto_refresh_kwargs=extra,
                           auto_refresh_url=token_uri,
                           token_updater=self.token_saver)
        return ls

    def get_client(self):
        if self.client is None:
            self.client = LSApiBase(self.get_session(), self.account_id)
            return self.client
        return self.client

    def get_token(self):
        if os.path.exists(self.credential_store_path) and os.path.isfile(self.credential_store_path):
            fp = open(self.credential_store_path)
            token = json.loads(fp.read())
            fp.close()
            return token
        return None

    def token_saver(self, token):
        with open(self.credential_store_path, 'w') as file:
            file.write(dumps(token))
