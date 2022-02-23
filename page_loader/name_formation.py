import re
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def get_name(url, format):
    url = re.sub(r"https://|http://", '', url)
    if format == 'directory':
        suffix = '_files'
    elif format == 'html' or not Path(url).suffix:
        suffix = '.html'
    else:
        suffix = Path(url).suffix
        url = url.replace(suffix, '')
    name_file = re.sub(r"[_\W]", '-', url)
    logging.debug(f'for {url} get name {name_file + suffix}')
    return name_file + suffix
