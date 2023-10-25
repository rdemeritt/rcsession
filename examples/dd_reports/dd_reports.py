import config
import reports
from rcsession.rd_utilities import *


def hostnamebyhostid(_session, _host_id, _cache=True):
    if _cache is True:
        for host in config.hosts_cache['hosts']:
            if host['id'] == _host_id:
                return host['name']
    response = _session.get(_session.hosts_url,
                            params={'filter': 'host_id: %s AND allowed_domain: %s' % (_host_id, config.args.domain)})
    config.logger.debug('response: %s' % json.loads(response.text))

    if response.status_code is not 200:
        return False
    return json.loads(response.text)['hosts'][0]['host_name']


def watchnamebywatchid(_session, _watch_id, _cache=True):
    if _cache is True:
        for watch in config.fcm_watch_cache['fcm_watches']:
            if watch['id']['instance_id'] == _watch_id:
                return watch['name']


def main():
    if config.args.command == 'out_of_contact_report':
        reports.generate_ooc_report()

    if config.args.command == 'in_contact_report':
        reports.generate_ic_report()

    if config.args.command == 'fcm_events_report':
        reports.generate_events_report()

    config.session.close_requests()


# kick off the whole thing
if __name__ == '__main__':
    config.init()
    config.logger.info('Starting')
    main()
