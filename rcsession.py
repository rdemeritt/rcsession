"""
Created by Ron DeMeritt <rdemeritt@gmail.com>

built on top of:
    python 3.5
    python-requests/2.9.1
"""
import requests
import json
import os
from time import sleep
from datetime import datetime
import rcsession.config as rc_config

__version__ = '0.4.3'


class RCSession:
    def __init__(self, _token=False, _key=False, _base_url=None, _verify=True,
                 _content_type="json", _accept="json"):
        rc_config.init()
        rc_config.logger.info('Starting RCSession')

        def set_base_url(__url):
            if _base_url is None:
                return __url
            return _base_url

        # check to see if we should use an API key instead
        # of Red Cloak token
        if _key:
            if os.path.isfile(str(_key)):
                _key = self.get_key_from_file(_key)
                rc_config.logger.debug('using key from file %s' % _key)
            else:
                rc_config.logger.debug('using static key: %s' % _key)

            self.headers = {
                'authorization': 'APIKEY %s' % _key,
                'content-type': 'application/%s' % _content_type,
                'accept': 'application/%s' % _accept
            }
            # set self.base_url
            self.base_url = set_base_url('https://api.secureworks.com/api/redcloak/')

        # use the Red Cloak token
        elif _token:
            if os.path.isfile(str(_token)):
                _token = self.get_token_from_file(_token)
                rc_config.logger.debug('using token from file %s' % _token)
            else:
                rc_config.logger.debug('using static token: %s' % _token)

            self.headers = {
                'authorization': 'TOKEN %s' % _token,
                'content-type': 'application/%s' % _content_type,
                'accept': 'application/%s' % _accept
            }
            # set self.base_url
            self.base_url = set_base_url('https://redcloak.secureworks.com/api/')

        self.token_url = self.base_url + "token"
        self.hosts_url = self.base_url + "hosts"
        self.hosts_tag_url = self.base_url + "hosts/tag"
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
        self.periodic_scans_url = self.base_url + 'periodicscans'
        self.ruleresuls_url = self.base_url + 'ruleresults'
        self.persistence_events_url = self.base_url + 'persistence_events_all'
        self.netflows_url = self.base_url + 'netflows'
        self.dns_lookups_url = self.base_url + 'dns_lookups'
        self.thread_injections_url = self.base_url + 'thread_injections'
        self.windows_events_url = self.base_url + 'windows_events'
        self.fcm_events_url = self.base_url + 'fcm_change_events'
        self.fcm_watches_url = self.base_url + 'fcm_watches'
        self.host_commands_url = self.base_url + 'host_commands'
        self.host_color_contributions_url = self.base_url + 'host_color_contributions'
        self.isolate_url = self.base_url + 'hosts/isolate'
        self.files_url = self.base_url + 'files'
        self.host_events_url = self.base_url + 'host_events'

        # setup our python requests session
        try:
            self.session = requests.Session()
            self.session.headers.update(self.headers)
            if _verify is False:
                self.session.verify = _verify

        except Exception as e:
            rc_config.logger.error("Unable to build requests session: %s" % str(e))
            exit(1)

        # make sure that we have a valid RC session and if so, set user_friendly_name
        try:
            token = self.get_token()
            if not token:
                rc_config.logger.error("Unable to build a Red Cloak Session to %s" % self.base_url)
                # exit(2)

            else:
                self.user_friendly_name = token["token"]["user_friendly_name"]

        except Exception as e:
            rc_config.logger.error("Unable to build a Red Cloak Session to %s: %s" % (self.base_url, str(e)))
            exit(3)
        # self.user_friendly_name = self.get_token()["token"]["user_friendly_name"]

    # make it easier to pass through standard http methods
    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.session.delete(*args, **kwargs)

    def head(self, *args, **kwargs):
        return self.session.head(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.session.put(*args, **kwargs)

    def options(self, *args, **kwargs):
        return self.session.options(*args, **kwargs)

    def close_requests(self):
        try:
            self.session.close()
            return True
        except Exception as e:
            rc_config.logger.error(str(e))
            return False

    def get_token(self):
        response = self.session.get(self.token_url)

        if response.status_code != 200:
            rc_config.logger.debug('unable to get token: %s' % response.text)
            return False

        return json.loads(response.text)

    def renew_token(self):
        response = self.session.post(self.token_url)

        if response.status_code != 200:
            rc_config.logger.warn("Got %s, but expected 200" % response.status_code)
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

    def fetch_deferred_job(self, _job_id, _sleep=10, _delete=True):
        while True:
            job_response = self.session.get(self.jobs_url + '/' + _job_id)
            if job_response.status_code != 200:
                rc_config.logger.error("Did not get 200 as expected, got %s instead" % job_response.status_code)
                return False
            job_response_json = json.loads(job_response.text)
            rc_config.logger.debug('job_response_json: %s' % job_response_json)
            if job_response_json['status'] == 'FAILED':
                rc_config.logger.warn('bulk job %s %s' % (job_response_json['uuid'], job_response_json['status']))
                return False
            if job_response_json['status'] == 'COMPLETE':
                rc_config.logger.debug('job %s is complete' % job_response_json['uuid'])
                break
            # report back if we see result set that has been truncated
            if job_response_json['status'] == 'COMPLETE_LIMIT_REACHED':
                rc_config.logger.warn('job %s is complete, but the results were not complete' % job_response_json['uuid'])
                break
            rc_config.logger.debug('job has not completed, %s is status %s' %
                                   (job_response_json['uuid'], job_response_json['status']))
            sleep(_sleep)
        fetch_response = self.session.get(self.jobs_url + '/' + job_response_json['uuid'] + '/contents')
        if fetch_response.status_code != 200:
            return False
        if _delete is True:
            self.delete_deferred_job(job_response_json['uuid'])
        rc_config.logger.info('fetched deferred job %s' % job_response_json['uuid'])
        return json.loads(fetch_response.text)

    def delete_deferred_job(self, _job_id):
        delete_response = self.session.delete(self.jobs_url + '/' + _job_id)
        if delete_response.status_code != 204:
            rc_config.logger.warn('response code was not 204, got %s instead' % delete_response.status_code)
            return False
        rc_config.logger.info('deleted deferred job %s' % _job_id)
        return True

    def edit_tag(self, _action, _tag, _domain, _host_id):
        entry_dict = dict(action=_action, host=[_host_id], tag=[_tag], domain=[_domain])
        response = self.session.post(self.hosts_tag_url, json=entry_dict)
        if response.status_code != 200:
            rc_config.logger.warn(
                'WARN: Unable to add tag(s): %s to host_id: %s' % (entry_dict['tag'], entry_dict['host']))
            return False
        if _action == 'add':
            rc_config.logger.debug('Added tag: %s to host_id: %s' % (entry_dict['tag'], entry_dict['host']))
        elif _action == 'remove':
            rc_config.logger.debug('Removed tag: %s from host_id: %s' % (entry_dict['tag'], entry_dict['host']))
        return True
