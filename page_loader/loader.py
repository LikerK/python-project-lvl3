import os
import logging
from progress.bar import Bar
from colorama import Fore
from page_loader.data_from_url import download_file
from page_loader.name_formation import get_directory_name, get_file_name, get_html_name  # noqa: E501
from page_loader.page import Page


logger = logging.getLogger(__name__)


class ProgressDownload(Bar):
    bar_prefix = ' '
    bar_suffix = ' '
    empty_fill = '.'
    fill = '█'


def download(url, path=os.getcwd()):
    response = download_file(url)
    html_name = get_html_name(url)
    path_to_html = os.path.join(path, html_name)
    directory_name, path_to_directory = make_directory(path, url)
    page_structure = Page(url, response)
    domain_links = page_structure.domain_links

    spinner = ProgressDownload(max=len(domain_links), message='Downloads files: ')
    replacements = dict()
    if len(domain_links) > 0:   
        for link in domain_links:  
            name_local_file = get_file_name(link)
            content_local_file = download_file(link)
            path_to_local_file = os.path.join(directory_name, name_local_file)
            full_path_to_file = os.path.join(path_to_directory, name_local_file)
            logger.debug(f'file will be saved in {full_path_to_file}')
            save_file(full_path_to_file, content_local_file)
            replacements[link] = path_to_local_file
        spinner.next()
        print(Fore.GREEN + ' √' + Fore.RESET)
    else:
        print('No download links found')
    page_structure.replace_links(replacements)
    save_file(path_to_html, page_structure.html)
    return path_to_html


def make_directory(path, url):
    directory_name = get_directory_name(url)
    path_to_directory = os.path.join(path, directory_name)
    try:
        os.mkdir(path_to_directory)
    except FileExistsError:
        logger.warning('Directory already exists')
    except FileNotFoundError:
        logger.critical(f"Directory not found '{path}'")
        raise FileNotFoundError(f'The directory "{path}" does not exist')
    except PermissionError:
        logger.critical(f"No right save into directory '{path}'")
        raise PermissionError(f'No access to save to "{path}"')
    except OSError as error:
        logger.critical(f"Can't create directory. {error}")
        raise OSError(error)
    return directory_name, path_to_directory


def save_file(path, content):
    try:
        with open(path, 'wb') as file:
            file.write(content)
    except PermissionError:
        logger.critical(f"No right save into directory '{path}'")
        raise PermissionError(f'No access to save to "{path}"')
    except OSError as error:
        logger.critical(f'Unknown error: {error}')
        raise OSError(error)
