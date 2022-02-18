import os
import requests_mock
import pytest
from page_loader.loader import download
from page_loader.name_formation import get_name


@pytest.mark.parametrize('url, result', [
    ('https://hexlet.io', 'hexlet-io.html'),
    ('https://cdn2.hexlet.io/courses', 'cdn2-hexlet-io-courses.html'),
])
def test_name(url, result):
    assert get_name(url, 'html') == result


def test_dowloads(tmp_path):
    with open('tests/fixtures/index.html') as html_file:
        html_code = html_file.read()
    with open('tests/fixtures/scripts.js') as js_file:
        js_code = js_file.read()
    with open('tests/fixtures/style.css') as css_file:
        css_code = css_file.read()
    with requests_mock.mock() as mocker:
        mocker.get('https://test-dowloads.files.com', text=html_code)
        mocker.get('https://test-dowloads.files.com/img/01.png')
        mocker.get('https://test-dowloads.files.com/style.css', text=css_code)
        mocker.get('https://test-dowloads.files.com/scripts.js', text=js_code)
        path_to_html = download('https://test-dowloads.files.com', tmp_path)
        # path_to_css = os.path.join(tmp_dir_name, 'test-dowloads-files-com_files/style.css')  # noqa: E501
        path_to_js = os.path.join(tmp_path, 'test-dowloads-files-com_files/test-dowloads-files-com-scripts.js')  # noqa: E501
        with open('tests/fixtures/scripts.js') as script:
            with open(path_to_js) as test:
                assert script.read() == test.read()
        with open(path_to_html) as html_file:
            with open('tests/fixtures/index_result.html') as html_file_result:
                assert html_file.read() == html_file_result.read()
