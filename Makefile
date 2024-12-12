.PHONY: install test run clean update check-python test test-unit test-all help

# Python environment variables
PYTHON := python3
REQUIRED_PYTHON_VERSION := 3.10
PYTHON_PATCH_VERSION := 16
VENV := .venv
UV := UV_LINK_MODE=copy uv  # Set UV link mode to suppress warning
SHELL := /bin/zsh  # Use zsh instead of bash

# Check Python version and install if needed
check-python:
	@if ! command -v brew >/dev/null 2>&1; then \
		echo "Installing Homebrew..."; \
		/bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || exit 1; \
	fi
	@if ! command -v pyenv >/dev/null 2>&1; then \
		echo "Installing pyenv..."; \
		if ! brew install pyenv; then \
			echo "Failed to install pyenv"; \
			exit 1; \
		fi; \
		echo 'eval "$$(pyenv init --path)"' >> ~/.zshrc; \
		echo 'eval "$$(pyenv init -)"' >> ~/.zshrc; \
		source ~/.zshrc || true; \
	fi
	@if ! pyenv versions | grep -q "$(REQUIRED_PYTHON_VERSION).$(PYTHON_PATCH_VERSION)"; then \
		echo "Installing Python $(REQUIRED_PYTHON_VERSION).$(PYTHON_PATCH_VERSION)..."; \
		pyenv install $(REQUIRED_PYTHON_VERSION).$(PYTHON_PATCH_VERSION) || { echo "Failed to install Python"; exit 1; }; \
	fi
	@pyenv local $(REQUIRED_PYTHON_VERSION).$(PYTHON_PATCH_VERSION)
	@pyenv global $(REQUIRED_PYTHON_VERSION).$(PYTHON_PATCH_VERSION)
	@eval "$$(pyenv init -)"

# Create directories if they don't exist
$(shell mkdir -p recordings screenshots)

# Installation
install: check-python
	@if ! brew list portaudio > /dev/null 2>&1; then \
		echo "Installing portaudio..."; \
		brew install portaudio; \
	fi
	$(UV) venv --python=$(PYTHON)
	$(UV) pip install -r requirements.txt
	@echo "\nInstallation complete!"
	@echo "To activate the virtual environment, run:"
	@echo "source .venv/bin/activate"
	@if [ "$(shell uname)" = "Darwin" ]; then \
		echo "source .venv/bin/activate" | pbcopy && \
		echo "\033[90m(This command has been copied to your clipboard - just press Cmd+V and hit enter)\033[0m"; \
	fi

# Run tests
test: test-unit  ## Run unit tests (default)
	@echo "Completed unit tests"

test-unit:  ## Run only unit tests
	python3 run_tests.py --pattern "test_*.py" --type unit

test-all:  ## Run all tests (unit, integration, etc)
	python3 run_tests.py --pattern "test_*.py"

# Run the application
run: check-python
	$(PYTHON) main.py

# Clean temporary files and caches
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf *.log || true
	rm -rf .nev
	rm -rf .venv
	rm -rf myenv
	find . -type d -name "__pycache__" -exec rm -r {} +

# Update dependencies
update: check-python
	$(UV) pip install --upgrade -r requirements.txt

# Initialize development environment
init: check-python
	$(UV) venv --python=$(PYTHON)
	$(UV) pip install -r requirements.txt
	touch .env
	@echo "Remember to add your API keys to .env file"

help:  ## Display this help message
	@echo "Available commands:"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'