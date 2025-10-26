.PHONY: help install test test-cov lint format type-check profile clean reinstall shell
.DEFAULT_GOAL := help

VENV := .venv/bin

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv .venv; \
	fi
	@echo "Installing package in development mode..."
	$(VENV)/pip install --upgrade pip
	$(VENV)/pip install -e ".[dev]"
	@echo "Installing pre-commit hooks..."
	$(VENV)/pre-commit install
	@echo "\n✅ Installation complete! Activate your virtual environment with:"
	@echo "source .venv/bin/activate"

test: ## Run tests
	$(VENV)/pytest

test-cov: ## Run tests with coverage
	$(VENV)/pytest --cov=src --cov-report=html --cov-report=term

lint: ## Run linting
	$(VENV)/ruff check .

format: ## Format code
	$(VENV)/ruff format .

type-check: ## Run type checking
	$(VENV)/mypy .

profile: ## Profile the app
	python -m cProfile -o profile_results.prof -m {{cookiecutter.package_name}}
	$(VENV)/snakeviz profile_results.prof

clean: ## Clean up cache and temporary files
	-find . -type d -name "__pycache__" -exec rm -rf {} + || true
	-find . -type d -name "*.egg-info" -exec rm -rf {} + || true
	-find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
	-find . -type d -name ".mypy_cache" -exec rm -rf {} + || true
	-find . -type d -name ".ruff_cache" -exec rm -rf {} + || true
	-rm -rf htmlcov/ || true

reinstall: clean install ## Clean and reinstall the package

shell: ## Activate virtual environment in a new shell
	@echo "Activating virtual environment..."
	@exec $(SHELL) -c 'source .venv/bin/activate && exec $(SHELL)'