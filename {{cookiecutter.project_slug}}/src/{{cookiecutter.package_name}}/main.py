"""Main module for {{cookiecutter.project_name}}."""
{% if cookiecutter.include_cdk == 'yes' %}
from {{cookiecutter.package_name}} import logging_config

logger = logging_config.get_logger('{{cookiecutter.package_name}}.main')


def main() -> None:
    """Main entry point."""
    logger.info("Hello from {{cookiecutter.project_name}}!")
    logger.info("Customize this module with your application logic")


if __name__ == "__main__":
    main()
{% else %}
from {{cookiecutter.package_name}} import logging_config

logger = logging_config.get_logger('{{cookiecutter.package_name}}.main')

def main() -> None:
    """Main entry point."""
    logger.info("Hello from {{cookiecutter.project_name}}!")


if __name__ == "__main__":
    main()
{% endif %}