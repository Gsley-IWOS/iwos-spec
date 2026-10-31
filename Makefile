# IWOS specification repository: validation entry points (see tools/validate/README.md).
PYTHON ?= python3

.PHONY: validate test lock install-deps

validate:
	$(PYTHON) tools/validate/validate.py

test:
	$(PYTHON) -m unittest discover -s tools/validate -p 'test_*.py' -v

lock:
	$(PYTHON) tools/validate/validate.py --write-lock

install-deps:
	$(PYTHON) -m pip install --upgrade pyyaml jsonschema
