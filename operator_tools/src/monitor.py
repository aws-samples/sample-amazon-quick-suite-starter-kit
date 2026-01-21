"""CLI tool for monitoring Quick Suite usage and users."""

import sys

import boto3
import click
from botocore.exceptions import ClientError
from common.observability import logger

quicksight = boto3.client("quicksight")
sts = boto3.client("sts")


@click.group()
def cli() -> None:
    """Monitor Quick Suite usage and users."""
    pass


@cli.command()
@click.option("--namespace", default="default", help="Quick Suite namespace (default: default)")
def list_users(namespace: str) -> None:
    """List all Quick Suite users with their roles."""
    account_id = sts.get_caller_identity()["Account"]

    try:
        paginator = quicksight.get_paginator("list_users")
        users = []

        for page in paginator.paginate(AwsAccountId=account_id, Namespace=namespace):
            users.extend(page.get("UserList", []))

        if not users:
            click.echo("No users found")
            return

        click.echo(f"\nFound {len(users)} user(s) in namespace '{namespace}':\n")

        role_counts = {}
        for user in users:
            username = user.get("UserName", "N/A")
            email = user.get("Email", "N/A")
            role = user.get("Role", "N/A")
            active = user.get("Active", False)
            status = "Active" if active else "Inactive"

            role_counts[role] = role_counts.get(role, 0) + 1

            click.echo(f"Username: {username}")
            click.echo(f"  Email: {email}")
            click.echo(f"  Role: {role}")
            click.echo(f"  Status: {status}")
            click.echo()

        click.echo("Summary by Role:")
        for role, count in sorted(role_counts.items()):
            click.echo(f"  {role}: {count}")

    except ClientError as e:
        logger.exception("Failed to list users", extra={"error": str(e)})
        click.echo(f"✗ Failed to list users: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--namespace", default="default", help="Quick Suite namespace (default: default)")
def list_groups(namespace: str) -> None:
    """List all Quick Suite groups."""
    account_id = sts.get_caller_identity()["Account"]

    try:
        paginator = quicksight.get_paginator("list_groups")
        groups = []

        for page in paginator.paginate(AwsAccountId=account_id, Namespace=namespace):
            groups.extend(page.get("GroupList", []))

        if not groups:
            click.echo("No groups found")
            return

        click.echo(f"\nFound {len(groups)} group(s) in namespace '{namespace}':\n")

        for group in groups:
            group_name = group.get("GroupName", "N/A")
            arn = group.get("Arn", "N/A")
            description = group.get("Description", "N/A")

            click.echo(f"Group: {group_name}")
            click.echo(f"  Description: {description}")
            click.echo(f"  ARN: {arn}")
            click.echo()

    except ClientError as e:
        logger.exception("Failed to list groups", extra={"error": str(e)})
        click.echo(f"✗ Failed to list groups: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--group-name", required=True, help="Group name to inspect")
@click.option("--namespace", default="default", help="Quick Suite namespace (default: default)")
def list_group_members(group_name: str, namespace: str) -> None:
    """List all members of a Quick Suite group."""
    account_id = sts.get_caller_identity()["Account"]

    try:
        paginator = quicksight.get_paginator("list_group_memberships")
        members = []

        for page in paginator.paginate(GroupName=group_name, AwsAccountId=account_id, Namespace=namespace):
            members.extend(page.get("GroupMemberList", []))

        if not members:
            click.echo(f"No members found in group '{group_name}'")
            return

        click.echo(f"\nFound {len(members)} member(s) in group '{group_name}':\n")

        for member in members:
            member_name = member.get("MemberName", "N/A")
            arn = member.get("Arn", "N/A")

            click.echo(f"Member: {member_name}")
            click.echo(f"  ARN: {arn}")
            click.echo()

    except ClientError as e:
        logger.exception("Failed to list group members", extra={"error": str(e)})
        click.echo(f"✗ Failed to list group members: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--namespace", default="default", help="Quick Suite namespace (default: default)")
def account_summary(namespace: str) -> None:
    """Display Quick Suite account summary."""
    account_id = sts.get_caller_identity()["Account"]

    click.echo("\n=== Quick Suite Account Summary ===")
    click.echo(f"Account ID: {account_id}")
    click.echo(f"Namespace: {namespace}\n")

    try:
        paginator = quicksight.get_paginator("list_users")
        users = []
        for page in paginator.paginate(AwsAccountId=account_id, Namespace=namespace):
            users.extend(page.get("UserList", []))

        active_users = sum(1 for u in users if u.get("Active", False))
        role_counts = {}
        for user in users:
            role = user.get("Role", "UNKNOWN")
            role_counts[role] = role_counts.get(role, 0) + 1

        click.echo(f"Total Users: {len(users)}")
        click.echo(f"Active Users: {active_users}")
        click.echo(f"Inactive Users: {len(users) - active_users}\n")

        click.echo("Users by Role:")
        for role, count in sorted(role_counts.items()):
            click.echo(f"  {role}: {count}")

        paginator = quicksight.get_paginator("list_groups")
        groups = []
        for page in paginator.paginate(AwsAccountId=account_id, Namespace=namespace):
            groups.extend(page.get("GroupList", []))

        click.echo(f"\nTotal Groups: {len(groups)}")

    except ClientError as e:
        logger.exception("Failed to get account summary", extra={"error": str(e)})
        click.echo(f"✗ Failed to get account summary: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
