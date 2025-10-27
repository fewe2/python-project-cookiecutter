"""Main module for {{cookiecutter.project_name}}."""

from {{cookiecutter.package_name}} import logging_config

logger = logging_config.get_logger('{{cookiecutter.package_name}}.main')

def main() -> None:
    """Main entry point."""
    logger.info("Hello from {{cookiecutter.project_name}}!")


if __name__ == "__main__":
    main()