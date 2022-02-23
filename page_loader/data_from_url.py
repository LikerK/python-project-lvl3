import requests
import logging
from page_loader.name_formation import get_name
import os


logger = logging.getLogger(__name__)


def download_html(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        logger.warning(f'{error} Status code: {requests.get(url).status_code}')
        raise Exception(f'Status code {error}') from error
    html_name = get_name(url, 'html')
    path_to_file = os.path.join(path, html_name)
    return path_to_file, response.text


def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        logger.warning(f'Failed to download file. Status code: {error}')
    return response.content
