import os
from urllib.parse import urljoin
from tempfile import TemporaryDirectory
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
        mocker.get('https://test-dowloads.files.com/assert/scripts.js', text=js_code)  # noqa: E501
        path_to_html = download('https://test-dowloads.files.com', tmp_path)
        path_to_css = os.path.join(tmp_path, 'test-dowloads-files-com_files/test-dowloads-files-com-style.css')  # noqa: E501
        path_to_js = os.path.join(tmp_path, 'test-dowloads-files-com_files/test-dowloads-files-com-assert-scripts.js')  # noqa: E501
        with open('tests/fixtures/scripts.js') as script:
            with open(path_to_js) as result_js:
                assert script.read() == result_js.read()
        with open(path_to_html) as html_file:
            with open('tests/fixtures/index_result.html') as html_file_result:
                assert html_file.read() == html_file_result.read()
        with open('tests/fixtures/style.css') as css_file:
            with open(path_to_css) as result_css:
                assert css_file.read() == result_css.read()
        path = os.path.join(tmp_path, 'test-dowloads-files-com_files')
        assert len(os.listdir(path)) == 3


@pytest.mark.parametrize('code', [404, 500])
def test_response_with_error(requests_mock, code):
    url = urljoin("https://ru.hexlet.io/courses", str(code))
    requests_mock.get(url, status_code=code)

    with TemporaryDirectory() as tmpdirname:
        with pytest.raises(Exception):
            assert download(url, tmpdirname)
