"""Lambda handler for processing SQS messages."""
{% if cookiecutter.include_cdk == 'yes' %}
import json
import os
from typing import Any, Dict

from {{cookiecutter.package_name}} import logging_config

logger = logging_config.get_logger("processor")


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Process SQS messages from the queue.
    
    Args:
        event: Lambda event containing SQS records
        context: Lambda context object
        
    Returns:
        Response with batch item failures if any
    """
    logger.info(f"Processing {len(event.get('Records', []))} records")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'dev')}")
    
    batch_item_failures = []
    
    for record in event.get("Records", []):
        try:
            message_id = record["messageId"]
            body = json.loads(record["body"])
            
            logger.info(f"Processing message {message_id}: {body}")
            
            # TODO: Implement your business logic here
            # Example: Process data, write to S3, call other services, etc.
            
        except Exception as e:
            logger.error(f"Failed to process message {message_id}: {e}")
            batch_item_failures.append({"itemIdentifier": message_id})
    
    return {"batchItemFailures": batch_item_failures}
{% endif %}
