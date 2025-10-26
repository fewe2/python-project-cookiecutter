# {{cookiecutter.project_name}}

{{cookiecutter.description}}

## Setup

### With Make (Linux/macOS)
```bash
make install
source .venv/bin/activate
```

### Without Make (Windows/Manual)
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

## Usage

```bash
# Run the main module (recommended)
python -m {{cookiecutter.package_name}}

# Or run directly (not recommended - may break relative imports)
python src/{{cookiecutter.package_name}}/main.py
```

## Development

### With Make (Linux/macOS)
- `make test` - Run tests
- `make lint` - Run linting
- `make format` - Format code
- `make type-check` - Run type checking
- `make shell` - Activate virtual environment

### Without Make (Windows/Manual)
- `pytest` - Run tests
- `ruff check .` - Run linting
- `ruff format .` - Format code
- `mypy src/` - Run type checking
- `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/macOS) - Activate virtual environment

## License

{{cookiecutter.license}}