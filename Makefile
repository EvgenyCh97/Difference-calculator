install:
	poetry install

package-install:
	python3 -m pip install --user dist/*.whl

reinstall: build package-install
	pip install --user dist/*.whl --force-reinstall

full-reinstall: build package-install reinstall

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

.PHONY: install build reinstall