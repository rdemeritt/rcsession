import argparse
import re
from log import build_logger, logging
from rcsession.rd_utilities import *
from rcsession.rcsession import *


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog='rc_dff', description='Utility to manage the Domain-Feature-Flag settings of the Red Cloak portal')
    parser.add_argument('--log_level', help='Set the logging level')
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument(
        '--token', help='User auth via Red Cloak Token')
    auth_group.add_argument(
        '--key', help='User auth via API key')
    parser.add_argument('--domain_id', help='Domain ID(s) to add/remove')
    parser.add_argument('--module', help='Module to manage', required=True,
                        choices=['hostel', 'fcm', 'ignition', 'huntingcertified'])
    parser.add_argument('--action', help='Action to be taken', required=True,
                        choices=['DISABLE_ALL', 'ENABLE_ALL', 'ENABLE_FOR_DOMAINS', 'LIST'])
    parser.add_argument('--clear_existing', help='Clear the existing Domain ID(s)?', action='store_true')

    return parser.parse_args()


def init():
    global start_time
    global session
    global logger
    global args
    global dff_url

    start_time = unix_time_now()
    args = build_arg_parser()

    if args.log_level:
        global log_level
        log_level = getattr(logging, args.log_level.upper())
    logger = build_logger()

    # process our arguments
    if args.key:
        session = RCSession(_key=args.key)
    elif args.token:
        session = RCSession(_token=args.token)
    # drop out if we don't have a way to setup session
    else:
        logger.error('No key or token provided')
        exit(1)

    # check to see if our session was successfully created
    if not session:
        exit(2)
    dff_url = session.base_url + 'domain_feature_flags'
    logger.debug('dff_url: %s' % dff_url)


# define global variables
start_time = None
logger = None
log_level = logging.INFO
args = None
session = None
dff_url = None
