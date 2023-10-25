import logging
import config


def build_logger():
    logger_name = 'host_reports_example'
    formatter = logging.Formatter("[%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:%(filename)s(%(lineno)s)] "
                                  "%(message)s", "%Y-%m-%dT%H:%M:%S")
    logger = logging.getLogger(logger_name)

    # log to file
    fh = logging.FileHandler('%s_%s.log' % (logger_name, config.start_time))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # log to the console as well
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logging.basicConfig(level=config.log_level, handlers=(fh, ch))
    return logger
