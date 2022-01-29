import tempfile
from page_loader.loader import downloads

def fake_get_repos():
    pass


downloads.get_data_from_url = fake_get_repos


def test_page_loader():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir_name = tmp
        page_loader = downloads('https://ru.hexlet.io/courses', tmp_dir_name)
        assert page_loader == f'{tmp_dir_name}/ru-hexlet-io-courses.html'