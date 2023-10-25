import rc_prod_test
from rcsession.rd_utilities import *

procwall_checks = {
    'process': {
        'enabled': True,
        'data': None
    },
    'watchlists': {
        'enabled': True,
        'data': None
    }
}


# query for our process telemetry
def do_procq(_session, _q=None):
    rc_prod_test.logger.info('do_procq')

    def _redcloaktest_process_query(__session, __pid, __commandline='redcloaktest'):
        process_query = {
            'type': 'process',
            'q': 'commandline:%s ' % __commandline +
                 'AND ' +
                 'image_path: ping ' +
                 'AND ' +
                 'id.pid: %s ' % __pid +
                 'AND ' +
                 'id.host_id: %s' % rc_prod_test.args.host_id
        }

        rc_prod_test.logger.debug("  process_query: %s" % process_query)
        response = __session.session.get(__session.search_url, params=process_query)
        if response.status_code != 200:
            return False
        return response.text

    q_result = json.loads(_redcloaktest_process_query(_session, __pid=_q['pid']))
    if 'total_hits' in q_result and q_result['total_hits'] is 0:
        rc_prod_test.logger.info("   process_query result: %s" % q_result)
        return False
    elif 'processes' in q_result and q_result['processes'][0]['id']['pid'] == _q['pid']:
        write_json(q_result, 'process_result_%s.json' % rc_prod_test.file_time)
        rc_prod_test.logger.info('  found process %s' % q_result)
        rc_prod_test.logger.info('  wrote found process to process_result_%s.json' % rc_prod_test.file_time)
        rc_prod_test.logger.debug('  turned off procwall check')
        return True
