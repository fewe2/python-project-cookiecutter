# Python Project Cookiecutter Template

A professional Python project template with modern tooling and comprehensive code quality checks.

## Features

### Code Quality & Testing
- **Ruff** for linting and formatting
- **MyPy** for type checking
- **Pytest** for testing with coverage
- **Radon/Xenon** for code complexity analysis
- **Safety** for dependency vulnerability scanning
- **Detect-secrets** for secret detection
- **Pre-commit** hooks for automated checks

### Development Tools
- **Makefile** for common tasks
- Virtual environment management
- GitLab CI/CD pipelines

### Infrastructure (Optional)
- **AWS CDK** for infrastructure as code
- Lambda deployment with layers
- Automated feature branch deployments
- Scheduled cleanup of orphaned stacks

### Code Quality Notes
This template uses Python-native tools instead of SonarQube because:
- Better Python support (Ruff, MyPy are Python-specific)
- Faster execution (no external service calls)
- No additional infrastructure needed
- See `.sonarcloud-example.yml` if SonarCloud integration is required

## Usage

```bash
pip install cookiecutter
cookiecutter /path/to/cookiecutter-python-template
cd your-new-project
make install
```

## Documentation

The template includes automatic documentation generation with MkDocs:

```bash
# Serve documentation locally
make docs-serve

# Build documentation
make docs-build
```

Documentation is auto-generated from:
- Markdown files in `docs/`
- Python docstrings (Google style)
- Code examples and API references

## Template Variables

- `project_name`: Display name of your project
- `project_slug`: Directory/package name (auto-generated)
- `package_name`: Python package name (auto-generated)
- `author_name`: Your name
- `author_email`: Your email
- `description`: Project description
- `python_version`: Python version (default: 3.11)
- `license`: License type
- `include_cdk`: Include AWS CDK infrastructure (yes/no)
- `aws_region`: AWS region for deployments
- `environment_stages`: Comma-separated environment names