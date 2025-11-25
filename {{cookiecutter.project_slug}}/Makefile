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
	$(VENV)/pip install -e ".[dev]"{% if cookiecutter.include_cdk == 'yes' %}
	$(VENV)/pip install -e ".[cdk]"{% endif %}
	@echo "Installing pre-commit hooks..."
	$(VENV)/pre-commit install
	@echo "\nInstallation complete! Activate your virtual environment with:"
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
	$(VENV)/mypy src/{{cookiecutter.package_name}}

profile: ## Profile the app
	python -m cProfile -o profile_results.prof -m {{cookiecutter.package_name}}.main
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
	@exec $(SHELL) -c 'source .venv/bin/activate && exec $(SHELL)'{% if cookiecutter.include_cdk == 'yes' %}

# CDK Commands
cdk-bootstrap: ## Bootstrap CDK (run once per account/region)
	cd infrastructure && $(VENV)/cdk bootstrap

cdk-synth: ## Synthesize CDK templates
	cd infrastructure && $(VENV)/cdk synth

cdk-diff: ## Show CDK diff
	cd infrastructure && $(VENV)/cdk diff

cdk-deploy: ## Deploy CDK stacks
	cd infrastructure && $(VENV)/cdk deploy --all --require-approval never

cdk-destroy: ## Destroy CDK stacks
	cd infrastructure && $(VENV)/cdk destroy --all --force

cdk-cleanup-branch: ## Cleanup current branch deployment
	@echo "Cleaning up deployment for current branch..."
	cd infrastructure && $(VENV)/cdk destroy --all --force

cdk-list: ## List all CDK stacks
	cd infrastructure && $(VENV)/cdk list

cleanup-branches: ## Cleanup orphaned feature branch stacks
	$(VENV)/python scripts/cleanup-feature-branches.py

docker-build: ## Build Docker image
	docker build -t {{cookiecutter.project_slug}} .

docker-run: ## Run Docker container locally
	docker run -p 8000:8000 --env ENVIRONMENT=development {{cookiecutter.project_slug}}

dev-server: ## Run development server
	$(VENV)/python -m {{cookiecutter.package_name}}{% endif %}