import config
import reports
from rcsession.rd_utilities import *


def hostnamebyhostid(_session, _host_id, _cache=True):
    if _cache is True:
        for host in config.hosts_cache['hosts']:
            if host['id'] == _host_id:
                return host['name']
    config.logger.debug('getting hostname for host_id: %s' % _host_id)
    # response = _session.get(_session.hosts_url,
    #                         params={'filter': 'host_id: %s AND allowed_domain: %s' % (_host_id, config.args.domain)})
    response = _session.get(_session.hosts_url + '/%s' % _host_id)
    config.logger.debug('hostnamebyhostid response: %s' % json.loads(response.text))

    if response.status_code is not 200:
        return False
    return json.loads(response.text)['hosts'][0]['host_name']


def main():
    if config.args.command == 'out_of_contact_report':
        reports.generate_ooc_report()

    if config.args.command == 'in_contact_report':
        reports.generate_ic_report()

    config.session.close_requests()


# kick off the whole thing
if __name__ == '__main__':
    config.init()
    config.logger.info('Starting')
    main()
