"""
Created by Ron DeMeritt <rdemeritt@gmail.com>

built on top of:
    python 3.5
    python-requests/2.9.1
"""
import requests
import json
import os
from datetime import datetime

__version__ = '0.2.4'


class RCSession:

    def __init__(self, _token=False, _key=False, _base_url=None,
                 _content_type="json", _accept="json"):

        def set_base_url(__url):
            if _base_url is None:
                return __url
            return _base_url

        # check to see if we should use an API key instead
        # of Red Cloak token
        if _key:
            if os.path.isfile(_key):
                _key = self.get_key_from_file(_key)

            self.headers = {
                'authorization': 'APIKEY %s' % _key,
                'content-type': 'application/%s' % _content_type,
                'accept': 'application/%s' % _accept
            }
            # set self.base_url
            self.base_url = set_base_url('https://api.secureworks.com/api/redcloak/')

        # use the Red Cloak token
        elif _token:
            if os.path.isfile(_token):
                _token = self.get_token_from_file(_token)

            self.headers = {
                'authorization': 'TOKEN %s' % _token,
                'content-type': 'application/%s' % _content_type,
                'accept': 'application/%s' % _accept
            }
            # set self.base_url
            self.base_url = set_base_url('https://redcloak.secureworks.com/')

        self.token_url = self.base_url + "token"
        self.hosts_url = self.base_url + "hosts"
        self.event_resolution_url = self.base_url + "event_resolution"
        self.hcc_url = self.base_url + "host_color_contributions"
        self.search_url = self.base_url + "search"
        self.client_domains_url = self.base_url + "client_domains"
        self.watchlists_url = self.base_url + "watchlists"
        self.users_url = self.base_url + "users"
        self.packages_url = self.base_url + "packages"
        self.index_url = self.base_url + 'index'
        self.jobs_url = self.base_url + 'jobs'
        self.datafilters_url = self.base_url + 'datafilters'
        self.known_hashes_url = self.base_url + 'known_hashes'
        self.investigations_url = self.base_url + 'investigations'
        self.suppression_rules_url = self.base_url + 'suppression_rules'
        self.process_disruptions_url = self.base_url + 'process_disruptions'
        self.processes_url = self.base_url + 'processes'
        self.ruleresuls_url = self.base_url+ 'ruleresults'
        self.persistence_events_url = self.base_url + 'persistence_events_all'
        self.netflows_url = self.base_url + 'netflows'
        self.dns_lookups_url = self.base_url + 'dns_lookups'
        self.thread_injections_url = self.base_url + 'thread_injections'
        self.windows_events_url = self.base_url + 'windows_events'

        # setup our python requests session
        try:
            self.session = requests.Session()
            self.session.headers.update(self.headers)

        except Exception as e:
            print("ERROR: Unable to build requests session: %s" % str(e))
            exit(1)

        # make sure that we have a valid RC session and if so, set user_friendly_name
        try:
            token = self.get_token()
            if not token:
                print("ERRR: Unable to build a Red Cloak Session to %s" % self.base_url)
                exit(2)

            else:
                self.user_friendly_name = token["token"]["user_friendly_name"]

        except Exception as e:
            print("ERRR: Unable to build a Red Cloak Session to %s: %s" % (self.base_url, str(e)))
            exit(3)
        # self.user_friendly_name = self.get_token()["token"]["user_friendly_name"]

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
    @staticmethod
    def get_token_from_file(_file_name):
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

    # api-gw key functionality
    # fetch our api-gw key from a json document
    #
    # example below:
    # {
    #     "key": "rdemeritt@gmail.com:s0m3P@$$w0rd"
    #  }
    @staticmethod
    def get_key_from_file(_file_name):
        with open(_file_name) as token_json:
            return json.load(token_json)['key']

    # return a datetime object from a string
    @classmethod
    def datetimefstr(cls, _dto_string):
        return datetime.strptime(_dto_string, '%Y-%m-%dT%H:%M:%S.%f')
