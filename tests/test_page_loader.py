import os
import stat
from bs4 import BeautifulSoup
from tempfile import TemporaryDirectory
from requests.exceptions import Timeout, ConnectionError, HTTPError
import requests_mock
import pytest
from page_loader.loader import download
from page_loader.name_formation import get_html_name

URL = 'https://test-dowloads.files.com'
URL_IMAGE = 'https://test-dowloads.files.com/img/hexlet.png'
URL_CSS = 'https://test-dowloads.files.com/style.css'
URL_JS = 'https://test-dowloads.files.com/assert/scripts.js'

HTML = 'tests/fixtures/index.html'
JS = 'tests/fixtures/scripts.js'
CSS = 'tests/fixtures/style.css'
IMAGE = 'tests/fixtures/hexlet.png'
HTML_RESULT = 'tests/fixtures/index_result.html'
HTML_NAME = 'test-dowloads-files-com.html'
PATH_TO_CSS = 'test-dowloads-files-com_files/test-dowloads-files-com-style.css'
PATH_TO_JS = 'test-dowloads-files-com_files/test-dowloads-files-com-assert-scripts.js'  # noqa: E501
PATH_TO_IMG = 'test-dowloads-files-com_files/test-dowloads-files-com-img-hexlet.png'  # noqa: E501
NAME_DIRECTORY = 'test-dowloads-files-com_files'


@pytest.mark.parametrize('url, result', [
    ('https://hexlet.io', 'hexlet-io.html'),
    ('https://cdn2.hexlet.io/courses', 'cdn2-hexlet-io-courses.html'),
])
def test_name(url, result):
    assert get_html_name(url) == result


def test_dowloads(tmp_path):
    html_code = get_content(HTML).decode()
    with open(HTML_RESULT, 'r') as file:
        html_result = file.read()
    css_code = get_content(CSS).decode()
    js_code = get_content(JS).decode()
    image = get_content(IMAGE)
    with requests_mock.mock() as mocker:
        mocker.get(URL, text=html_code)
        mocker.get(URL_IMAGE, content=image)
        mocker.get(URL_CSS, text=css_code)
        mocker.get(URL_JS, text=js_code)
        download(URL, tmp_path)
        path_to_html = os.path.join(tmp_path, HTML_NAME)
        path_to_css = os.path.join(tmp_path, PATH_TO_CSS)
        path_to_js = os.path.join(tmp_path, PATH_TO_JS)
        path_to_img = os.path.join(tmp_path, PATH_TO_IMG)

        result_html = get_content(path_to_html).decode()
        assert result_html == html_result

        result_css = get_content(path_to_css).decode()
        assert result_css == css_code

        result_js = get_content(path_to_js).decode()
        assert result_js == js_code

        result_img = get_content(path_to_img)
        assert result_img == image

        path = os.path.join(tmp_path, NAME_DIRECTORY)
        assert len(os.listdir(path)) == 3


def get_content(file):
    with open(file, 'rb') as file:
        return file.read()


@pytest.mark.parametrize('exc', [
    Timeout, ConnectionError, HTTPError])
def test_response_with_error(requests_mock, exc):
    requests_mock.get(URL, exc=exc)
    with TemporaryDirectory() as tmpdirname:
        with pytest.raises(Exception):
            assert download(URL, tmpdirname)


def test_permissions_error_to_write(requests_mock, tmp_path):
    requests_mock.get(URL)
    os.chmod(tmp_path, stat.S_IRUSR)
    with pytest.raises(PermissionError) as error:
        assert download(URL, tmp_path) == error
