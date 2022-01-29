import re


def directory(url):
    url_without_schema = re.sub(r"https://|http://", '', url)
    name_directory = re.sub(r"[_\W]", '-', url_without_schema)
    return f'{name_directory}_files'


def html(url):
    url_without_schema = re.sub(r"https://|http://", '', url)
    name_file = re.sub(r"[_\W]", '-', url_without_schema)
    return f'{name_file}.html'


def image(url):
    name_image = re.sub(r"\/", '-', url)
    return name_image