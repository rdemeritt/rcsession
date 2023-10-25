import argparse
from rcsession import rcsession
from time import sleep
from rcsession.rd_utilities import *
import generate_telemetry
from procwall_check import do_procq
from lacuna_check import do_lcna
from log import build_logger


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog='rc_prod_test', description='Test production Red Cloak functionality')
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument('--token', help='User auth via Red Cloak Token')
    auth_group.add_argument('--key', help='User auth via API key')
    parser.add_argument('--domain', help='Test against the provided list of domains')
    telemetry_group = parser.add_mutually_exclusive_group(required=True)
    telemetry_group.add_argument(
        '--unixtime', help='Unix time corresponding to the files we want to pull the telemetry from')
    telemetry_group.add_argument(
        '--generate_telemetry', help='Generate local activity', action='store_true')
    parser.add_argument('--telemetry_types', help='Run tests for these telemetry types')
    parser.add_argument('--host_id', help='The host_id of the endpoint the telemetry was generated on', required=True)
    parser.add_argument(
        '--verbose', help='Print extra stuff', action='store_true')
    return parser.parse_args()


def domain_dump(_session, _domains):
    for domain in _domains.split(','):
        print('DOMAIN INDEX DUMP: %s' % domain)
        print(_session.session.get(_session.index_url, params={'domain': '%s' % domain}).text + "\n")


# makeshift case statements
def do_dflt():
    print('default')


def do_ti(_session, _q=None):
    print('thread injection')


def do_we(_session, _q=None):
    print('windows event')


def do_persq(_session, _q=None):
    print('persistence')


def set_telemetry_types(_type, _init=False, _disable=False):
    def _all_to_false():
        for telemetry_type in telemetry_types:
            telemetry_types.get(telemetry_type)['enabled'] = False

    if _init is True:
        _all_to_false()

    for t_type in _type.split(','):
        if _disable:
            ed_value = False
        else:
            ed_value = True
        telemetry_types.get(t_type)['enabled'] = ed_value


def main():
    # process our arguments
    #
    # figure out how we should get our token and configure our https session
    if args.token:
        session = rcsession.RCSession(_token=args.token)

    elif args.key:
        session = rcsession.RCSession(_key=args.key)

    # drop out if we don't have a way to setup session
    else:
        logger.error('No token or key provided')
        exit(1)

    # check to see if our session was successfully created
    if not session:
        exit(2)

    # figure out which tests we will be checking
    if args.telemetry_types:
        set_telemetry_types(args.telemetry_types, _init=True)

    # check for our predicates on portal
    # loop for the telemetry
    work = True
    generate = True
    while work is True:
        for telemetry_type in telemetry_types:
            if telemetry_types.get(telemetry_type)['enabled'] is False:
                logger.debug('%s check is disabled, skipping' % telemetry_type)
                continue

            # generate telemetry
            if args.generate_telemetry is True and generate is True:
                logger.info('  generating: %s telemetry' % telemetry_type)
                getattr(generate_telemetry, telemetry_type)()
                continue

            logger.debug('using %s_%s.json to get my info' % (telemetry_type, str(file_time)))
            did_find = telemetry_types.get(telemetry_type, do_dflt)['case'](
                session, get_json_file_contents('%s_%s.json' % (telemetry_type, str(file_time))))
            # decide if we need to turn off the check
            if did_find is True:
                logger.info('  found %s telemetry' % telemetry_type)
                set_telemetry_types(telemetry_type, _disable=True)
        # ensure we only generate one set of data
        generate = False
        sleep(10)

    # close our session once we have finished
    session.close_requests()


# parse the command line arguments
args = build_arg_parser()

# check to see if someone gave us a unix timestamp to key off of
if args.unixtime:
    file_time = str(args.unixtime)
else:
    file_time = unix_time_now()

logger = build_logger()

telemetry_types = {
    'procwall': {
        'enabled': True,
        'case': do_procq
    },
    'thread_injection': {
        'enabled': False,
        'case': do_ti
    },
    'lacuna': {
        'enabled': True,
        'case': do_lcna
    },
    'windows_event': {
        'enabled': False,
        'case': do_we
    },
    'persistence': {
        'enabled': False,
        'case': do_persq
    }
}

# check to see if someone gave us a unix timestamp to key off of
if args.unixtime:
    file_time = str(args.unixtime)
else:
    file_time = unix_time_now()
# files to store telemetry
lacuna_file_name = 'lacuna_%s.json' % file_time
procwall_file_name = 'procwall_%s.json' % file_time

# kick off the whole thing
if __name__ == '__main__':
    logger.info('Starting')
    main()
