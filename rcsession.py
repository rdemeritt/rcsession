"""
Created by Ron DeMeritt <rdemeritt@gmail.com>
"""
import requests
import json

__version__ = '0.1.1'


def setupSession(_token):
    headers = {
        'authorization': 'TOKEN %s' % _token,
        'content-type': 'application/json',
        'accept': 'application/json'
    }

    session = requests.Session()
    session.headers.update(headers)

    # ensure our token is still valid
    token = getToken(session)

    if not token:
        print('Token Expired...  Trying to renew')

        # attempt to get a new token
        new_token = renewToken(session)

        if not new_token:
            return False

        # update our session headers with our new token
        session.headers.update(
            {'authorization': 'TOKEN %s' % new_token})
    global user_name
    # user_name = json.loads(
    #     session.get(token_url).text)["token"]["user_friendly_name"]
    # print(json.loads(session.get(token_url).text))
    user_name = getToken(session)["token"]["user_friendly_name"]
    return session


def getToken(_session):
    response = _session.get(token_url)

    if response.status_code == 404:
        return False

    return json.loads(response.text)


# fetch our authentication token from a json file
def getTokenFromFile(_file_name):
    with open(_file_name) as token_json:
        return json.load(token_json)['token']


def renewToken(_session):
    response = _session.post(token_url)

    if response.status_code != 200:
        print("ERROR: Got %s, but expected 200" % response.status_code)
        print(
            'Your token has expired.  '
            'Get a new token at %s' % token_url)
        return False

    return json.loads(response.text)['serialized']


token_url = 'https://redcloak.secureworks.com/token'
user_name = ''
