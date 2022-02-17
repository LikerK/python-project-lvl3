import re
from pathlib import Path


def get_name(url, format):
    url = re.sub(r"https://|http://", '', url)
    if format == 'html':
        suffix = '.html'
    elif format == 'directory':
        suffix = '_files'
    else:
        suffix = Path(url).suffix
        url = url.replace(suffix, '')
    name_file = re.sub(r"[_\W]", '-', url)
    return name_file + suffix
