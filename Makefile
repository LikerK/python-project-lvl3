install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 page_loader
	poetry run flake8 tests

test:
	poetry run pytest

check: test lint

coverage:
	poetry run coverage run -m pytest -v
	poetry run coverage xml
