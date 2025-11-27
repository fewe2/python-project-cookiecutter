"""Tests for Lambda handler."""
{% if cookiecutter.include_cdk == 'yes' %}
from src.handlers.processor import handler


def test_lambda_handler_sqs_event():
    """Test Lambda handler with SQS event."""
    event = {
        "Records": [
            {
                "messageId": "test-123",
                "body": '{"test": "data"}',
            }
        ]
    }
    context = {}
    
    result = handler(event, context)
    
    assert "batchItemFailures" in result
    assert isinstance(result["batchItemFailures"], list)


def test_lambda_handler_empty_event():
    """Test Lambda handler with empty event."""
    result = handler({}, {})
    
    assert "batchItemFailures" in result
    assert result["batchItemFailures"] == []
{% endif %}