import logging
import rc_prod_test


def build_logger():
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    _logger = logging.getLogger('rc_prod_test')

    # log to file
    fh = logging.FileHandler('%s_%s.log' % ('rc_prod_test', rc_prod_test.file_time))
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    # log to the console as well
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logging.basicConfig(level=logging.DEBUG, handlers=(fh, ch))
    return _logger