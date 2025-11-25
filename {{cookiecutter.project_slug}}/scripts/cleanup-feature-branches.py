#!/usr/bin/env python3
"""Script to cleanup CDK stacks for deleted feature branches."""
{% if cookiecutter.include_cdk == 'yes' %}
import subprocess
import sys
from typing import List, Set


def get_remote_branches() -> Set[str]:
    """Get list of remote branches."""
    try:
        result = subprocess.run(
            ["git", "branch", "-r", "--format=%(refname:short)"],
            capture_output=True,
            text=True,
            check=True,
        )
        branches = set()
        for line in result.stdout.strip().split("\n"):
            if line and "/" in line:
                branch = line.split("/", 1)[1]
                if branch not in ["HEAD", "main", "master", "develop", "staging"]:
                    branches.add(branch)
        return branches
    except subprocess.CalledProcessError:
        return set()


def get_cdk_stacks() -> List[str]:
    """Get list of CDK stacks."""
    try:
        result = subprocess.run(
            ["cdk", "list"],
            capture_output=True,
            text=True,
            check=True,
            cwd="infrastructure",
        )
        return [stack.strip() for stack in result.stdout.strip().split("\n") if stack.strip()]
    except subprocess.CalledProcessError:
        return []


def get_feature_stacks(stacks: List[str]) -> List[str]:
    """Filter stacks that appear to be feature branch stacks."""
    feature_stacks = []
    for stack in stacks:
        # Look for stacks with 'feature-' pattern
        if "feature-" in stack.lower():
            feature_stacks.append(stack)
    return feature_stacks


def extract_branch_from_stack(stack_name: str) -> str:
    """Extract branch name from stack name."""
    # Assuming format: ProjectName-Feature-BranchName
    parts = stack_name.split("-")
    if len(parts) >= 3 and "feature" in parts[1].lower():
        return "-".join(parts[2:])
    return ""


def cleanup_orphaned_stacks():
    """Cleanup CDK stacks for branches that no longer exist."""
    print("Checking for orphaned feature branch stacks...")
    
    remote_branches = get_remote_branches()
    cdk_stacks = get_cdk_stacks()
    feature_stacks = get_feature_stacks(cdk_stacks)
    
    if not feature_stacks:
        print("No feature branch stacks found.")
        return
    
    orphaned_stacks = []
    for stack in feature_stacks:
        branch = extract_branch_from_stack(stack)
        if branch and branch not in remote_branches:
            orphaned_stacks.append(stack)
    
    if not orphaned_stacks:
        print("No orphaned stacks found.")
        return
    
    print(f"Found {len(orphaned_stacks)} orphaned stack(s):")
    for stack in orphaned_stacks:
        print(f"  - {stack}")
    
    if input("\\nDelete these stacks? (y/N): ").lower() == "y":
        for stack in orphaned_stacks:
            print(f"Deleting {stack}...")
            try:
                subprocess.run(
                    ["cdk", "destroy", stack, "--force"],
                    check=True,
                    cwd="infrastructure",
                )
                print(f"Deleted {stack}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to delete {stack}: {e}")
    else:
        print("Cleanup cancelled.")


if __name__ == "__main__":
    cleanup_orphaned_stacks()
{% endif %}