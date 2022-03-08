import requests
import logging


logger = logging.getLogger(__name__)


def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        logger.warning(f'{error} Status code: {requests.get(url).status_code}')
        raise Exception(f'Status code {error}') from error
    return response.content
