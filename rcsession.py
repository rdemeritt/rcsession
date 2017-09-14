"""
Created by Ron DeMeritt <rdemeritt@gmail.com>

built on top of:
    python 3.5
    python-requests/2.9.1
"""
import requests
import json
from datetime import datetime

__version__ = '0.2.2'


class RCSession:

    def __init__(self, _token=False, _key=False, _auto_renew=False,
                 _content_type="json", _accept="json"):
        # check to see if we should use an API key instead
        # of Red Cloak token
        if _key:
            self.headers = {
                'authorization': 'APIKEY %s' % _key,
                'content-type': 'application/%s' % _content_type,
                'accept': 'application/%s' % _accept
            }
            self.base_url = "https://api.secureworks.com/api/redcloak/"

        # use the Red Cloak token
        elif _token:
            self.headers = {
                'authorization': 'TOKEN %s' % _token,
                'content-type': 'application/%s' % _content_type,
                'accept': 'application/%s' % _accept
            }
            self.base_url = "https://redcloak.secureworks.com/"
            self.auto_renew = _auto_renew

        try:
            self.session = requests.Session()
            self.session.headers.update(self.headers)

        except Exception as e:
            print("ERROR: Unable to build requests session: %s" % e)
            exit(1)

        self.token_url = self.base_url + "token"
        self.hosts_url = self.base_url + "hosts"
        self.event_resolution_url = self.base_url + "event_resolution"
        self.hcc_url = self.base_url + "host_color_contributions"
        self.search_url = self.base_url + "search"
        self.client_domains_url = self.base_url + "client_domains"
        self.watchlists_url = self.base_url + "watchlist"
        self.users_url = self.base_url + "users"
        self.packages_url = self.base_url + "packages"
        self.user_friendly_name = self.get_token()["token"]["user_friendly_name"]

    def close_requests(self):
        try:
            self.session.close()
        except Exception as e:
            print(e)

    def get_token(self):
        response = self.session.get(self.token_url)

        if response.status_code != 200:
            return False

        return json.loads(response.text)

    def renew_token(self):
        response = self.session.post(self.token_url)

        if response.status_code != 200:
            print("ERROR: Got %s, but expected 200" % response.status_code)
            return False

        # reinitialize our session using our new token
        RCSession.__init__(self, json.loads(response.text)['serialized'])
        return True

    # fetch our authentication token from a json document
    #
    # example below:
    # {
    #     "token": "3JkZW1lcml0dEBnbWFpbC5jb20QkJHtx/...."
    #  }
    #
    def get_token_from_file(self, _file_name):
        with open(_file_name) as token_json:
            return json.load(token_json)['token']

    # return datetime object w/ expiration date of token.  if the token has expired
    # it will return false
    # NOTE: likely don't need this function...
    def is_token_valid(self):
        if self.get_token() and \
                self.datetimefstr(self.get_token()['token']['expires']) > datetime.utcnow():
            return self.datetimefstr(self.get_token()['token']['expires'])
        return False

    # return a datetime object from a string
    @classmethod
    def datetimefstr(cls, _dto_string):
        return datetime.strptime(_dto_string, '%Y-%m-%dT%H:%M:%S.%f')
