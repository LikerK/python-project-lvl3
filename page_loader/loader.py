import os
from bs4 import BeautifulSoup
from page_loader.data_from_url import get_data_from_url
from page_loader.style import FORMAT


def downloads(url, path=''):
    content = get_data_from_url(url)    
    file_name = FORMAT['html'](url)
    directory_name = FORMAT['directory'](url)
    path_to_file = os.path.join(os.getcwd(), path, file_name)
    os.mkdir(path + directory_name)
    content = download_images(url, directory_name, content)
    save_file(path_to_file, str(content), 'w')
    return path_to_file


def download_images(url, directory_name, content):
    soup = BeautifulSoup(content, 'lxml')
    images = soup.find_all('img')
    print(images)
    for image in images:
        source_to_image = image.get('src')
        image_bytes = get_data_from_url(f'{url}/{source_to_image}', option='content')
        name_file_image = FORMAT['image'](source_to_image)
        image['src'] = f'{directory_name}/{name_file_image}'
        save_file(f'{directory_name}/{name_file_image}', image_bytes, 'wb')
    return soup.prettify(soup.original_encoding)


def save_file(path, content, format):
    with open(path, format) as file:
        file.write(content)
