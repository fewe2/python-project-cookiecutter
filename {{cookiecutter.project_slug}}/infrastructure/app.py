#!/usr/bin/env python3
"""CDK App entry point."""
{% if cookiecutter.include_cdk == 'yes' %}
import os

import aws_cdk as cdk
from constructs import Construct

from stacks.{{cookiecutter.package_name}}_stack import {{cookiecutter.package_name.title().replace('_', '')}}Stack


def get_environment() -> str:
    """Get deployment environment from CI/CD variable or default to dev."""
    return os.getenv("ENVIRONMENT", "dev")


class {{cookiecutter.package_name.title().replace('_', '')}}App(Construct):
    """Main CDK application."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get environment from CI/CD variable
        env_name = get_environment()
        
        # Create stack for the environment
        {{cookiecutter.package_name.title().replace('_', '')}}Stack(
            self,
            f"{{cookiecutter.package_name.title().replace('_', '')}}-{env_name.title()}",
            env=cdk.Environment(
                account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                region=os.getenv("CDK_DEFAULT_REGION", "{{cookiecutter.aws_region}}")
            ),
            environment_name=env_name,
            stack_name=f"{{cookiecutter.project_slug}}-{env_name}",
        )


app = cdk.App()
{{cookiecutter.package_name.title().replace('_', '')}}App(app, "{{cookiecutter.package_name.title().replace('_', '')}}App")
app.synth()
{% endif %}