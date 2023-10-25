import argparse
from log import build_logger, logging
from rcsession.rd_utilities import *
from rcsession.rcsession import *


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog='isolate_hosts')
    parser.add_argument('--log_level', help='Set the logging level')
    parser.add_argument('--key', help='Red Cloak API key', required=True)
    parser.add_argument('--host_id_list', required=True)
    parser.add_argument('--action', choices=['isolate','integrate'], required=True)
    parser.add_argument('--reason', required=True)

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
