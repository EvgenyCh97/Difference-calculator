install:
	poetry install

package-install:
	python3 -m pip install --user dist/*.whl

selfcheck:
	poetry check

test:
	poetry run pytest

lint:
	poetry run flake8 gendiff tests

check: selfcheck test lint

build: check
	poetry build

reinstall: build package-install
	pip install --user dist/*.whl --force-reinstall

full-reinstall: build package-install reinstall

test-coverage:
	poetry run pytest --cov=gendiff tests/ --cov-report xml tests/

.PHONY: install test lint selfcheck check build