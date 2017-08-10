"""
Created by Ron DeMeritt <rdemeritt@gmail.com>
"""
import requests
import json
from _datetime import datetime

__version__ = '0.2.0'


class RCSession:

    token_url = 'https://redcloak.secureworks.com/token'

    def __init__(self, _token):
        self.headers = {
            'authorization': 'TOKEN %s' % _token,
            'content-type': 'application/json',
            'accept': 'application/json'
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.username = self.get_token()["token"]["user_friendly_name"]

    def get_token(self):
        response = self.session.get(self.token_url)

        if response.status_code == 404:
            return False

        return json.loads(response.text)

    def renew_token(self):
        response = self.session.post(self.token_url)

        if response.status_code != 200:
            print("ERROR: Got %s, but expected 200" % response.status_code)
            return False

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

    # return true if token is expired.  if it is not expired
    # it will return the expiration date
    def is_token_expired(self):
        if self.get_token() and \
                self.create_dto(self.get_token()['token']['expires'])\
                > datetime.utcnow():
            return self.create_dto(self.get_token()['token']['expires'])
        return True

    # return a datetime object from a string
    @classmethod
    def create_dto(cls, _dto_string):
        return datetime.strptime(_dto_string, '%Y-%m-%dT%H:%M:%S.%f')
