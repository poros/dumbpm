.PHONY: minimal
minimal: venv

venv: Pipfile Pipfile.lock
	pipenv install --dev
	pipenv run pre-commit install -f --install-hooks
	pipenv shell

.PHONY: test
test:
	tox

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .tox
	rm -rf venv
