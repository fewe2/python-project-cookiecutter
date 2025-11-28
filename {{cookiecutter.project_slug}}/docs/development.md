# Development Guide

## Setting Up Development Environment

1. Clone the repository
2. Run `make install`
3. Activate the virtual environment: `source .venv/bin/activate`

## Code Quality Standards

This project maintains high code quality standards through automated checks:

### Linting and Formatting

We use **Ruff** for both linting and formatting:

```bash
# Check for issues
make lint

# Auto-format code
make format
```

### Type Checking

We use **MyPy** with strict mode:

```bash
make type-check
```

### Testing

We use **Pytest** with coverage tracking:

```bash
# Run tests
make test

# Run with coverage report
make test-cov
```

### Code Complexity

We monitor code complexity with **Radon** and **Xenon**:

```bash
make complexity
```

### Security

We scan for vulnerabilities and secrets:

```bash
make security
```

## Pre-commit Hooks

Pre-commit hooks run automatically before each commit:

- Ruff linting and formatting
- MyPy type checking
- Trailing whitespace removal
- YAML/JSON validation
- Secret detection

To run manually:

```bash
pre-commit run --all-files
```

## Writing Documentation

Documentation is written in Markdown and built with MkDocs:

```bash
# Serve documentation locally
make docs-serve

# Build documentation
make docs-build
```

## Docstring Style

We use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of the function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    return True
```

## Testing Guidelines

- Write tests for all new features
- Maintain >80% code coverage
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

Example:

```python
def test_process_message_success():
    """Test that process_message handles valid input correctly."""
    # Arrange
    message = {"key": "value"}
    
    # Act
    result = process_message(message)
    
    # Assert
    assert result["status"] == "success"
```

## CI/CD Pipeline

The GitLab CI pipeline runs:

1. **Test stage**: Unit tests, linting, type checking, complexity analysis
2. **Security stage**: Secret scanning, dependency vulnerability checks{% if cookiecutter.include_cdk == 'yes' %}
3. **Build stage**: CDK synthesis
4. **Deploy stage**: Infrastructure deployment{% endif %}

## Contributing

1. Create a feature branch
2. Make your changes
3. Ensure all tests pass: `make quality test`
4. Commit your changes (pre-commit hooks will run)
5. Push and create a merge request
