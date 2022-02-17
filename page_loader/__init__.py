from page_loader.loader import downloads
import logging
import sys


def init_logger():
    logger = logging.getLogger('page_loader')
    format = '%(asctime)s || %(name)s || %(levelname)s || %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(stream=sys.stderr)
    sh.setFormatter(logging.Formatter(format))
    sh.setLevel(logging.CRITICAL)
    logger.addHandler(sh)


__all__ = ('downloads', 'init_logger')
init_logger()
