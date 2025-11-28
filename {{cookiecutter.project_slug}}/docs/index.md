# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Overview

Welcome to the documentation for {{cookiecutter.project_name}}. This project provides a modern Python development setup with comprehensive tooling and best practices.

## Quick Start

```bash
# Install the package
pip install {{cookiecutter.project_slug}}

# Or for development
git clone <repository-url>
cd {{cookiecutter.project_slug}}
make install
```

## Features

- Modern Python tooling (Ruff, MyPy, Pytest)
- Comprehensive code quality checks
- Pre-commit hooks for automated validation
- CI/CD pipeline with GitLab{% if cookiecutter.include_cdk == 'yes' %}
- AWS CDK infrastructure as code
- Automated Lambda deployments{% endif %}

## Documentation Sections

- **[Getting Started](getting-started.md)** - Installation and basic usage
- **[API Reference](api.md)** - Detailed API documentation
- **[Development](development.md)** - Contributing and development guide{% if cookiecutter.include_cdk == 'yes' %}
- **[Infrastructure](infrastructure.md)** - AWS infrastructure documentation{% endif %}

## License

This project is licensed under the {{cookiecutter.license}} license.
