import logging


def build_logger():
    logger_name = 'rcsession'
    # formatter = logging.Formatter("[%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:%(filename)s(%(lineno)s)] "
    #                               "%(message)s", "%Y-%m-%dT%H:%M:%S")
    log_format = "[%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:%(filename)s(%(lineno)s)] %(message)s"
    time_format = "%Y-%m-%dT%H:%M:%S"

    _logger = logging.getLogger(logger_name)

    logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=time_format)

    return _logger
