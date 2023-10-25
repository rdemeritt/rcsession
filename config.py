from .log import build_logger
from .rd_utilities import unix_time_now


def init():
    global logger
    global start_time

    start_time = unix_time_now()
    logger = build_logger()


start_time = None
logger = None
