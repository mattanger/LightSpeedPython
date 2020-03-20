import requests
import time

class LSApiBase:
    """
    Base class for talking to the Lightspeed API
    """
    default_content_type = "application/json"
    last_request_time = None

    def __init__(self, session, account_id=None):
        self.base_url = "https://api.lightspeedapp.com/API"
        self.session = session
        self.account_id = account_id
        self.response = None
        self.request_counter = 0


    def get(self, endpoint, payload=None, with_account=True):
        """

        :param endpoint:
        :param payload:
        :param content_type:
        :return:
        """
        self.check_wait_needed()
        self.response = self.session.get(url=self.url(endpoint, with_account=with_account), params=payload)
        # print('Before 2: %s\n' % time.ctime())
        # time.sleep(2)
        # print('After 2: %s' % time.ctime())
        return self.response

    def post(self, endpoint, body, with_account=True):
        """

        :param endpoint:
        :param body:
        :param content_type:
        :return:
        """
        self.request_counter = self.request_counter + 1
        self.check_wait_needed()
        self.response = self.session.post(self.url(endpoint, with_account=with_account), json=body)
        return self.response

    def url(self, endpoint, with_account=True):
        """

        :param endpoint: The string endpoint to be added to the request url
        :return: the built string for the request
        """
        if self.account_id is not None and with_account:
            return self.base_url + '/Account/' + self.account_id + "/" + endpoint
        else:
            return self.base_url + '/' + endpoint

    def request_made(self):
        if self.last_request_time is None:
            self.last_request_time = time.time()
        self.request_counter = self.request_counter + 1
        now = time.time()
        if self.request_counter % 2 == 0:
            time.sleep(1.5)
        self.last_request_time = now

    def check_wait_needed(self):
        if self.response is None:
            return
        drip = self.response.headers.get('x-ls-api-drip-rate')
        bucket = self.response.headers.get('x-ls-api-bucket-level')
        bucket = bucket.split('/')
        used = float(bucket[0])
        size = float(bucket[1])
        if drip is not None:
            rate = float(drip)
        else:
            rate = 1.5
        needed = used + 2
        if needed >= size:
            wait = needed - size
            if (wait / rate) < 1:
                wait = 2
            else:
                wait = wait / rate * 2
            print("sleeping for %s" % wait )
            time.sleep(wait)
