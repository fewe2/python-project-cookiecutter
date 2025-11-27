"""Main module for {{cookiecutter.project_name}}."""
{% if cookiecutter.include_cdk == 'yes' %}
from typing import Any, Dict

from {{cookiecutter.package_name}} import logging_config

logger = logging_config.get_logger('{{cookiecutter.package_name}}.main')


def process_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """Process a message from SQS.
    
    Args:
        message: Message data to process
        
    Returns:
        Processing result
    """
    logger.info(f"Processing message: {message}")
    
    # TODO: Add your business logic here
    # Example: validate, transform, store data, call APIs, etc.
    
    result = {
        "status": "success",
        "processed": message,
    }
    
    logger.info(f"Message processed successfully: {result}")
    return result


def main() -> None:
    """Main entry point for local testing."""
    logger.info("Hello from {{cookiecutter.project_name}}!")
    
    # Example usage
    test_message = {"test": "data"}
    result = process_message(test_message)
    logger.info(f"Result: {result}")


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