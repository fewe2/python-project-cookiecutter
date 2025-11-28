# API Reference

This page contains the auto-generated API documentation from the source code docstrings.

## Main Module

::: {{cookiecutter.package_name}}.main
    options:
      show_root_heading: true
      show_source: true

## Logging Configuration

::: {{cookiecutter.package_name}}.logging_config
    options:
      show_root_heading: true
      show_source: true
{% if cookiecutter.include_cdk == 'yes' %}
## Lambda Handlers

::: handlers.processor
    options:
      show_root_heading: true
      show_source: true
{% endif %}
