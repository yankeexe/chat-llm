SHELL :=/bin/bash

VERSION ?= $(shell git rev-parse --short HEAD)

VENV_DIR = .venv

.PHONY: test clean check dev setup
.DEFAULT_GOAL=help

check-bp: # Check for breakpoints in the code
	@if grep -rnw --exclude-dir={env,venv,.venv} --include='*.py' -e "breakpoint"; then \
		echo "❌ Breakpoints found in code. Remove them to proceed."; \
		exit 1; \
	else \
		echo "✅ No breakpoints found."; \
	fi

check: # Check for linting issues
	@ruff check chat_app main.py
	@$(MAKE) check-bp

fix: # Fix auto-fixable linting issues
	@ruff check chat_app main.py --fix

clean: # Clean temporary files
	@rm -rf __pycache__ .pytest_cache
	@find . -name '*.pyc' -exec rm -r {} +
	@find . -name '__pycache__' -exec rm -r {} +
	@rm -rf build dist
	@find . -name '*.egg-info' -type d -exec rm -r {} +

setup: # Initial project setup
	@echo "Creating virtual env at: $(VENV_DIR)"
	@python3 -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	@source $(VENV_DIR)/bin/activate && pip install -r requirements/requirements-dev.txt && pip install -r requirements/requirements.txt
	@echo -e "\n✅ Done.\n🎉 Run the following commands to get started:\n\n ➡️ source $(VENV_DIR)/bin/activate\n ➡️ make run\n"

run: # Run the application
	@streamlit run main.py

help: # Show this help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
