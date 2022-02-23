import os
import logging
from progress.bar import Bar
from colorama import Fore
from page_loader.data_from_url import download_html, download_file
from page_loader.name_formation import get_name
from page_loader.page import Page


logger = logging.getLogger(__name__)


class My_bar(Bar):
    bar_prefix = ' '
    bar_suffix = ' '
    empty_fill = '.'
    fill = '█'


def download(url, path=os.getcwd()):
    path_to_html, response = download_html(url, path)
    directory_name, path_to_directory = make_directory(path, url)
    page_structure = Page(url, response)
    domain_links = page_structure.get_domain_links
    replacements = download_files(
        domain_links, path_to_directory, directory_name)
    page_structure.replace_links(replacements)
    save_file(path_to_html, page_structure.html, 'w')
    return path_to_html


def download_files(domain_links, path_to_directory, directory_name):
    spinner = My_bar(max=len(domain_links), message='Downloads files: ')
    replacements = dict()
    for link in domain_links:
        name_file = get_name(link, 'file')
        file_content = download_file(link)
        new_value = os.path.join(directory_name, name_file)
        full_path_to_file = os.path.join(path_to_directory, name_file)
        logger.debug(f'file will be saved in {full_path_to_file}')
        save_file(full_path_to_file, file_content, 'wb')
        replacements[link] = new_value
        spinner.next()
    if len(domain_links) > 0:
        print(Fore.GREEN + ' √' + Fore.RESET)
    else:
        print('No download links found')
    return replacements


def make_directory(path, url):
    directory_name = get_name(url, 'directory')
    path_to_directory = os.path.join(path, directory_name)
    try:
        os.mkdir(path_to_directory)
    except FileExistsError:
        logger.warning('Directory already exists')
    except FileNotFoundError:
        logger.critical(f"Directory not found '{path}'")
        raise FileNotFoundError(f'The directory "{path}" does not exist')
    except OSError as error:
        logger.warning(f"Can't create directory. {error}")
        raise OSError(error)
    return directory_name, path_to_directory


def save_file(path, content, format):
    try:
        with open(path, format) as file:
            file.write(content)
    except PermissionError:
        logger.critical(f"No right save into directory '{path}'")
        raise PermissionError(f'No access to save to "{path}"')
    except OSError as error:
        logger.warning(f'Unknown error: {error}')
