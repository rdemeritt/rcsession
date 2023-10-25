import argparse
import re
from log import build_logger, logging
from rcsession.rd_utilities import *
from rcsession.rcsession import *


def build_hosts_cache(_session, _domain):
    hosts_cache_search = {
        'domain': '%s' % _domain,
        'type': 'host',
        'q': 'color:RED OR YELLOW OR GREEN',
        'bulk': True,
        'name': 'build_hosts_cache_%s' % start_time
    }
    logger.debug('building hosts cache')
    hosts_response = _session.get(_session.search_url, params=hosts_cache_search)

    if hosts_response.status_code is not 200:
        logger.warn('did not get 200, got %s instead' % hosts_response.status_code)
        logger.debug(hosts_response.text)
        return False
    return session.fetch_deferred_job(json.loads(hosts_response.text)['uuid'])


def build_fcm_watch_cache(_session, _domain):
    logger.debug('building fcm watch cache')
    fcm_watches_response = _session.get(_session.fcm_watches_url, params={'domain': _domain,
                                                                          'count': 10000})
    if fcm_watches_response.status_code is not 200:
        logger.warn('did not get 200, got %s instead' % fcm_watches_response.status_code)
        logger.debug(fcm_watches_response.text)
        return False
    return json.loads(fcm_watches_response.text)


def build_arg_parser():
    def datetime_regex(_arg):
        datetime_pattern = re.compile(
            '2[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]')
        if not datetime_pattern.match(_arg):
            raise argparse.ArgumentTypeError
        return _arg

    parser = argparse.ArgumentParser(
        prog='dd_reports', description='Script to generate reports for CC/DD')
    parser.add_argument('--log_level', help='Set the logging level')
    subparsers = parser.add_subparsers()

    # arg group for the fcm_events report
    events_report_sub = subparsers.add_parser('fcm_events_report')
    events_report_sub.set_defaults(command='fcm_events_report')
    events_report_sub.add_argument('--start', help='Start date and time in format: yyyy-mm-ddThh:mm:ss',
                                   type=datetime_regex, required=True)
    events_report_sub.add_argument('--end', help='End date and time in format: yyyy-mm-ddThh:mm:ss',
                                   type=datetime_regex, required=True)
    events_report_sub.add_argument('--key', help='Red Cloak API key', required=True)
    events_report_sub.add_argument('--domain', help='Domain ID to run report for', required=True)
    events_report_sub.add_argument('--output', help='Filename to save output to', required=True)

    # arg group for the out_of_contact report
    ooc_reports_sub = subparsers.add_parser('out_of_contact_report')
    ooc_reports_sub.set_defaults(command='out_of_contact_report')
    ooc_reports_sub.add_argument('--key', help='Red Cloak API key', required=True)
    ooc_reports_sub.add_argument('--domain', help='Domain ID to run report for', required=True)
    ooc_reports_sub.add_argument('--output', help='Filename to save output to', required=True)

    # arg group for the in_contact report
    ooc_reports_sub = subparsers.add_parser('in_contact_report')
    ooc_reports_sub.set_defaults(command='in_contact_report')
    ooc_reports_sub.add_argument('--key', help='Red Cloak API key', required=True)
    ooc_reports_sub.add_argument('--domain', help='Domain ID to run report for', required=True)
    ooc_reports_sub.add_argument('--output', help='Filename to save output to', required=True)

    return parser.parse_args()


def init(_build_cache=True):
    global start_time
    global session
    global logger
    global args
    global hosts_cache
    global fcm_watch_cache

    start_time = unix_time_now()
    args = build_arg_parser()

    if args.log_level:
        global log_level
        log_level = getattr(logging, args.log_level.upper())
    logger = build_logger()

    # process our arguments
    if args.key:
        session = RCSession(_key=args.key)

    # drop out if we don't have a way to setup session
    else:
        logger.error('No key provided')
        exit(1)

    # check to see if our session was successfully created
    if not session:
        exit(2)

    if _build_cache is True and args.command == 'fcm_events_report':
        logger.info('Building hosts and fcm_watch caches')
        hosts_cache = build_hosts_cache(session, args.domain)
        fcm_watch_cache = build_fcm_watch_cache(session, args.domain)


# define global variables
start_time = None
hosts_cache = None
fcm_watch_cache = None
logger = None
log_level = logging.INFO
args = None
session = None
