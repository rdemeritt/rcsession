import rc_prod_test
from rcsession.rd_utilities import *
from datetime import datetime, timedelta

lacuna_checks = {
    'netflows': {
        'enabled': True,
        'data': None
    },
    'dns_lookups': {
        'enabled': True,
        'data': None
    }
}


def do_lcna(_session, _q=None):
    rc_prod_test.logger.info('do_lcna')

    qt_start_dt = datetime.utcfromtimestamp(float(_q[0]['time']))
    qt_end_dt = qt_start_dt + timedelta(minutes=1)
    qt_start = qt_start_dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
    qt_end = qt_end_dt.strftime('%Y-%m-%dT%H:%M:%S.%f')

    def _dns_lookup_query(__session):
        dns_lookup_query = {
            'type': 'dns_lookup',
            'q': 'query_name: %s ' % _q[0]['dns_name'] +
                 'AND ' +
                 'rdata: %s ' % _q[0]['rdata'] +
                 'AND ' +
                 'query_time: [%s TO %s] ' % (qt_start, qt_end) +
                 'AND ' +
                 'id.host_id: %s' % rc_prod_test.args.host_id
        }
        rc_prod_test.logger.debug("  dns_lookup query: %s" % dns_lookup_query)
        response = __session.session.get(__session.search_url, params=dns_lookup_query)
        return response.text

    def _netflow_query(__session):
        netflow_query = {
            'type': 'netflow',
            'q': 'id.host_id: %s ' % rc_prod_test.args.host_id +
                 'AND ' +
                 'remote_port: 53 ' +
                 'AND ' +
                 'create_time: [%s TO %s]' % (qt_start, qt_end)
        }
        rc_prod_test.logger.debug("  netflow query: %s" % netflow_query)
        response = __session.session.get(__session.search_url, params=netflow_query)
        return response.text

    # if True, then we have yet to find matching telemetry
    # execute a search, and then store the results in lacuna_checks
    if lacuna_checks['netflows']['enabled'] is True:
        netflow_result = json.loads(_netflow_query(_session))
        rc_prod_test.logger.debug("   netflow_result: %s" % netflow_result)
        lacuna_checks['netflows']['data'] = netflow_result

    if lacuna_checks['dns_lookups']['enabled'] is True:
        dns_result = json.loads(_dns_lookup_query(_session))
        rc_prod_test.logger.debug("   dns_result: %s" % dns_result)
        lacuna_checks['dns_lookups']['data'] = dns_result

    for check in lacuna_checks:
        rc_prod_test.logger.debug("   %s is %s" % (check, lacuna_checks[check]['enabled']))
        if 'total_hits' in lacuna_checks[check]['data'] and lacuna_checks[check]['data']['total_hits'] is 0:
            rc_prod_test.logger.info("     %s lacuna_checks: nothing found: %s" %
                  (check, lacuna_checks[check]['data']['total_hits']))
            continue

        elif 'dns_lookups' in lacuna_checks[check]['data'] and lacuna_checks[check]['enabled'] is True:
            if lacuna_checks[check]['data']['dns_lookups'][0]['query_name'] == _q[0]['dns_name']:
                write_json(lacuna_checks[check]['data'], 'dns_result_%s.json' % rc_prod_test.file_time)
                lacuna_checks[check]['enabled'] = False
                rc_prod_test.logger.info('     found dns_lookup %s' % dns_result)
                rc_prod_test.logger.info('     wrote found dns_lookup to dns_result_%s.json' % rc_prod_test.file_time)
                rc_prod_test.logger.debug("     set %s to %s" % (check, lacuna_checks[check]['enabled']))

        elif 'netflows' in lacuna_checks[check]['data'] and lacuna_checks[check]['enabled'] is True:
            write_json(lacuna_checks[check]['data'], 'netflow_result_%s.json' % rc_prod_test.file_time)
            lacuna_checks[check]['enabled'] = False
            rc_prod_test.logger.info('     found netflows %s' % netflow_result)
            rc_prod_test.logger.info('     wrote found netflows to netflow_result_%s.json' % rc_prod_test.file_time)
            rc_prod_test.logger.debug("     set %s to %s" % (check, lacuna_checks[check]['enabled']))

    # if both of these are False, then we have found both pieces of telemetry and should disable
    # the entire check
    if lacuna_checks['netflows']['enabled'] is False and lacuna_checks['dns_lookups']['enabled'] is False:
        rc_prod_test.logger.debug('  disabling lacuna check')
        return True
    return False

