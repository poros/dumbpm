.PHONY: minimal
minimal: venv

venv: tox.ini Pipfile Pipfile.lock
	tox -e venv

.PHONY: test
test:
	tox

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .tox
	rm -rf venv
