import re
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def _build_name(url, html=False):
    url = re.sub(r"https://|http://", '', url)
    if not Path(url).suffix or html is True:
        suffix = '.html'
    else:
        suffix = Path(url).suffix
        url = url.replace(suffix, '')
    file_name = re.sub(r"[_\W]", '-', url)
    return file_name, suffix


def get_directory_name(url):
    directory_name = get_html_name(url).replace('.html', '_files')
    return directory_name


def get_html_name(url):
    file_name, suffix = _build_name(url, html=True)
    return f'{file_name}{suffix}'


def get_file_name(url):
    file_name, suffix = _build_name(url)
    return f'{file_name}{suffix}'
