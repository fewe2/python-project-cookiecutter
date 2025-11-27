{% if cookiecutter.include_cdk == 'yes' %}# =============================================================================
# Lambda Container Image Dockerfile (CURRENTLY NOT USED)
# =============================================================================
# This project uses ZIP package deployment with Lambda Layers (see CDK stack).
# If you want to switch to container-based deployment, uncomment this Dockerfile
# and update the CDK stack to use:
#
#   code=lambda_.DockerImageCode.from_image_asset(
#       "../",
#       file="Dockerfile",
#       cmd=["handlers.processor.handler"],
#   )
#
# Benefits of container deployment:
# - Larger package size (up to 10GB vs 250MB for zip)
# - Include system dependencies and binaries
# - More control over runtime environment
# =============================================================================

# FROM public.ecr.aws/lambda/python:{{cookiecutter.python_version}}

# # Copy requirements and install dependencies
# COPY pyproject.toml ./
# RUN pip install --no-cache-dir .

# # Copy application code
# COPY src/ ${LAMBDA_TASK_ROOT}/

# # Set the CMD to your handler
# CMD ["handlers.processor.handler"]
{% endif %}