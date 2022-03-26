import requests
import logging


logger = logging.getLogger(__name__)


def download_file(url, local_file=False):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        logger.warning(f'failed to download file from link {url}. Status code: {requests.get(url).status_code}')  # noqa: E501
        if local_file is False:
            raise Exception(f'Status code {error}') from error
    return response.content
