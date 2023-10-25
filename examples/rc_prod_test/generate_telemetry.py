import subprocess
import socket
import rc_prod_test
from rcsession.rd_utilities import *


def procwall():
    # execute 'ping redcloaktest' and capture pid
    def _ping_redcloaktest():
        try:
            ping_process = subprocess.Popen(['ping', 'redcloaktest'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ping_process.wait()

        except Exception as e:
            rc_prod_test.logger.error("unable to run test: %s" % str(e))
            return False
        return ping_process

    prct_results = _ping_redcloaktest().__dict__
    write_json(prct_results, rc_prod_test.procwall_file_name)
    rc_prod_test.logger.debug('  _ping_redcloak_test: wrote process pid %s to %s' %
                              (prct_results['pid'], rc_prod_test.procwall_file_name))


def lacuna():
    # use sockets to generate a dns request
    def _dns_lookup(_dns_name):
        addr = socket.gethostbyname(_dns_name)
        return addr

    dns_name = 'rukind.com'
    try:
        dns_response = _dns_lookup(dns_name)
    except Exception as e:
        rc_prod_test.logger.error("unable to generate query: %s" % str(e))
        return False

    rc_prod_test.logger.debug("  dns_response: %s" % dns_response)

    dns_lookup_j = []
    dns_lookup_d = {
        'dns_name': '%s' % dns_name,
        'rdata': '%s' % dns_response,
        'time': '%s' % rc_prod_test.file_time
    }
    append_json(dns_lookup_d, dns_lookup_j)
    write_json(dns_lookup_j, rc_prod_test.lacuna_file_name)
    rc_prod_test.logger.debug("  dns_lookup_j: %s" % dns_lookup_j)
    return True


def thread_injection():
    pass


def windows_event():
    pass


def persistence():
    pass
