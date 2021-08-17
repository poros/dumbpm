.PHONY: minimal
minimal: install

install: pyproject.toml poetry.lock
	poetry install
	poetry run pre-commit install -f --install-hooks

.PHONY: test
test:
	tox

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .tox
	rm -rf dist

.PHONY: dist
dist: install
	poetry build

.PHONY: upload-to-pypi
upload-to-pypi: dist
	poetry run twine upload dist/*

.PHONY: pre-commit
pre-commit: install
	poetry run pre-commit run --all-files
