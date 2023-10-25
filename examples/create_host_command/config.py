import argparse
import re
from log import build_logger, logging
from rcsession.rd_utilities import *
from rcsession.rcsession import *


def build_arg_parser():
    parser = argparse.ArgumentParser(prog='', description='')
    parser.add_argument('--log_level', help='Set the logging level')
    parser.add_argument('--key', help='Red Cloak API key', required=True)
    parser.add_argument('--domain_id', help='Comma separated list of Domain IDs', required=True)
    parser.add_argument('--enable', help='Enable the submitted host commands', action='store_true')
    # parser.add_argument('--hc_json', help='JSON file containing the Host Command', required=True)

    return parser.parse_args()


def init():
    global start_time
    global session
    global logger
    global args

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


# define global variables
start_time = None
logger = None
log_level = logging.INFO
args = None
session = None
