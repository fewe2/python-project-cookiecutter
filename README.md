# Python Project Cookiecutter Template

A professional Python project template with modern tooling.

## Features

- **Ruff** for linting and formatting
- **MyPy** for type checking
- **Pytest** for testing with coverage
- **Pre-commit** hooks
- **Makefile** for common tasks
- Virtual environment management

## Usage

```bash
pip install cookiecutter
cookiecutter /path/to/cookiecutter-python-template
cd your-new-project
make install
```

## Template Variables

- `project_name`: Display name of your project
- `project_slug`: Directory/package name (auto-generated)
- `package_name`: Python package name (auto-generated)
- `author_name`: Your name
- `author_email`: Your email
- `description`: Project description
- `python_version`: Python version (default: 3.11)
- `license`: License type