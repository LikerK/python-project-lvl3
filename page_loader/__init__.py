from page_loader.loader import download
import logging
import sys


def init_logger():
    logger = logging.getLogger('page_loader')
    format = '| %(name)s | %(levelname)s | %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(stream=sys.stderr)
    sh.setFormatter(logging.Formatter(format))
    sh.setLevel(logging.CRITICAL)
    logger.addHandler(sh)


__all__ = ('download', 'init_logger')
init_logger()
