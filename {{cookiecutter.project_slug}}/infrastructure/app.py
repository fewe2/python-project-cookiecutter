#!/usr/bin/env python3
"""CDK App entry point."""
{% if cookiecutter.include_cdk == 'yes' %}
import os
import re
import subprocess
from typing import List

import aws_cdk as cdk
from constructs import Construct

from stacks.{{cookiecutter.package_name}}_stack import {{cookiecutter.package_name.title().replace('_', '')}}Stack


def get_git_branch() -> str:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return os.getenv("BRANCH_NAME", "main")


def sanitize_name(name: str) -> str:
    """Sanitize name for AWS resource naming."""
    # Replace invalid characters with hyphens and limit length
    sanitized = re.sub(r"[^a-zA-Z0-9-]", "-", name.lower())
    return sanitized[:20].strip("-")


def get_deployment_environments() -> List[str]:
    """Get environments using hybrid deployment strategy."""
    fixed_environments = "{{cookiecutter.environment_stages}}".split(",")
    fixed_environments = [env.strip() for env in fixed_environments]
    
    branch = get_git_branch()
    
    # Use fixed environments for main branches
    if branch in ["main", "master", "develop", "staging", "production"]:
        # Map branch to environment
        branch_env_map = {
            "main": "prod",
            "master": "prod",
            "develop": "dev",
            "staging": "staging",
            "production": "prod",
        }
        mapped_env = branch_env_map.get(branch, "dev")
        return [mapped_env] if mapped_env in fixed_environments else ["dev"]
    else:
        # Use branch name for feature branches
        return [f"feature-{sanitize_name(branch)}"]


class {{cookiecutter.package_name.title().replace('_', '')}}App(Construct):
    """Main CDK application."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get environments based on deployment strategy
        environments = get_deployment_environments()
        
        for env_name in environments:
            # Create stack for each environment
            {{cookiecutter.package_name.title().replace('_', '')}}Stack(
                self,
                f"{{cookiecutter.package_name.title().replace('_', '')}}-{env_name.title()}",
                env=cdk.Environment(
                    account=cdk.Aws.ACCOUNT_ID,
                    region="{{cookiecutter.aws_region}}"
                ),
                environment_name=env_name,
                stack_name=f"{{cookiecutter.project_slug}}-{env_name}",
            )


app = cdk.App()
{{cookiecutter.package_name.title().replace('_', '')}}App(app, "{{cookiecutter.package_name.title().replace('_', '')}}App")
app.synth()
{% endif %}