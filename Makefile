.PHONY: minimal
minimal: venv

venv: Pipfile Pipfile.lock
	pipenv install --dev
	pipenv run pre-commit install -f --install-hooks

.PHONY: test
test:
	tox

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .tox
	rm -rf venv
	rm -rf dist

.PHONY: dist
dist: venv
	pipenv run python setup.py sdist bdist_wheel

.PHONY: upload-to-pypi
upload-to-pypi: dist
	pipenv run twine upload dist/*

.PHONY: pre-commit
pre-commit: venv
	pipenv run pre-commit run --all-files
