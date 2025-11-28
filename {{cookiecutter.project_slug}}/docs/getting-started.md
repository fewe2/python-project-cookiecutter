# Getting Started

## Installation

### From Source

```bash
git clone <repository-url>
cd {{cookiecutter.project_slug}}
make install
```

This will:
- Create a virtual environment
- Install the package in development mode
- Install all development dependencies
- Set up pre-commit hooks

### Activate Virtual Environment

```bash
source .venv/bin/activate
```

## Basic Usage

```python
from {{cookiecutter.package_name}}.main import main

# Run the main function
main()
```
{% if cookiecutter.include_cdk == 'yes' %}
## AWS Lambda Usage

The project includes Lambda handlers for processing SQS messages:

```python
from {{cookiecutter.package_name}}.main import process_message

# Process a message
result = process_message({"key": "value"})
print(result)
```
{% endif %}
## Development Commands

```bash
# Run tests
make test

# Run tests with coverage
make test-cov

# Lint code
make lint

# Format code
make format

# Type check
make type-check

# Check complexity
make complexity

# Run security checks
make security

# Run all quality checks
make quality
```
{% if cookiecutter.include_cdk == 'yes' %}
## Infrastructure Commands

```bash
# Deploy infrastructure
make cdk-deploy

# Show infrastructure diff
make cdk-diff

# Destroy infrastructure
make cdk-destroy

# List all stacks
make cdk-list
```
{% endif %}
## Configuration

Configuration is managed through environment variables:

- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR){% if cookiecutter.include_cdk == 'yes' %}
- `ENVIRONMENT`: Deployment environment (dev, staging, prod)
- `AWS_REGION`: AWS region for deployments{% endif %}
