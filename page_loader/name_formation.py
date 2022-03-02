import re
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def get_name(func):
    def wrapper(url):
        url = re.sub(r"https://|http://", '', url)
        url, suffix = func(url)
        name_file = re.sub(r"[_\W]", '-', url)
        return name_file + suffix
    return wrapper


@get_name
def get_name_directory(url):
    suffix = '_files'
    return url, suffix


@get_name
def get_name_html(url):
    suffix = '.html'
    return url, suffix


@get_name
def get_name_file(url):
    if not Path(url).suffix:
        suffix = '.html'
    else:
        suffix = Path(url).suffix
        url = url.replace(suffix, '')
    return url, suffix
