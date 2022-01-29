import requests


def get_data_from_url(url, option='text'):
    response = requests.get(url)
    if option == 'text':
        return response.text
    else:
        return response.content
