# IWOS specification repository: validation entry points (see tools/validate/README.md).
PYTHON ?= python3

.PHONY: validate test test-validator test-iwos guard lock install-deps

validate:
	$(PYTHON) tools/validate/validate.py

test: test-validator test-iwos

test-validator:
	$(PYTHON) -m unittest discover -s tools/validate -p 'test_*.py' -v

test-iwos:
	PYTHONPATH=tools/iwos/src $(PYTHON) -m unittest discover -s tools/iwos/tests -p 'test_*.py' -v

guard:
	PYTHONPATH=tools/iwos/src $(PYTHON) -m iwos.cli validate

lock:
	$(PYTHON) tools/validate/validate.py --write-lock

install-deps:
	$(PYTHON) -m pip install --upgrade pyyaml jsonschema
