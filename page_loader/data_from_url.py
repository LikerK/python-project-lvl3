import requests
import logging

logger = logging.getLogger(__name__)


def get_data_from_url(url, option='text'):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        logger.warning(f'{url} raises connection error')
        message = f'could not establish connection to"{url}" '
        raise requests.exceptions.ConnectionError(message)
    if option == 'text':
        return response.text
    else:
        return response.content
