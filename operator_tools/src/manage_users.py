"""CLI tool for managing IAM Identity Center users and groups."""

import json
import sys
from enum import Enum
from pathlib import Path

import boto3
import click
from botocore.exceptions import ClientError
from common.observability import logger
from pydantic import BaseModel, EmailStr, Field, field_validator

sso_admin = boto3.client("sso-admin")
identitystore = boto3.client("identitystore")
quicksight = boto3.client("quicksight")
sts = boto3.client("sts")


class QuickSuiteGroup(Enum):
    """Quick Suite pricing tier groups."""

    ADMIN = "QUICK_SUITE_ADMIN"
    ENTERPRISE = "QUICK_SUITE_ENTERPRISE"
    PROFESSIONAL = "QUICK_SUITE_PRO"


QUICKSIGHT_ROLE_MAPPING = {
    QuickSuiteGroup.ADMIN.value: "ADMIN",
    QuickSuiteGroup.ENTERPRISE.value: "AUTHOR",
    QuickSuiteGroup.PROFESSIONAL.value: "READER",
}


class CreateUserRequest(BaseModel):
    """Request model for creating a user."""

    username: str = Field(min_length=1, max_length=128)
    email: EmailStr
    given_name: str = Field(min_length=1, max_length=100)
    family_name: str = Field(min_length=1, max_length=100)
    group: str | None = None

    @field_validator("group")
    @classmethod
    def validate_group(cls, v: str | None) -> str | None:
        """Validate group is a valid Quick Suite group."""
        if v is not None and v not in [g.value for g in QuickSuiteGroup]:
            valid_groups = ", ".join([g.value for g in QuickSuiteGroup])
            raise ValueError(f"Group must be one of: {valid_groups}")
        return v


class UsersFile(BaseModel):
    """Model for users configuration file."""

    users: list[CreateUserRequest]


def get_identity_store_id() -> str:
    """Get the Identity Store ID from IAM Identity Center instance."""
    try:
        paginator = sso_admin.get_paginator("list_instances")
        for page in paginator.paginate():
            instances = page.get("Instances", [])
            if instances:
                identity_store_id = instances[0]["IdentityStoreId"]
                logger.info("Found Identity Store", extra={"identity_store_id": identity_store_id})
                return identity_store_id

        logger.error("No IAM Identity Center instances found")
        sys.exit(1)
    except ClientError as e:
        logger.exception("Failed to get Identity Store ID", extra={"error": str(e)})
        sys.exit(1)


def get_user_by_username(identity_store_id: str, username: str) -> dict | None:
    """Get user by username."""
    try:
        paginator = identitystore.get_paginator("list_users")
        for page in paginator.paginate(
            IdentityStoreId=identity_store_id,
            Filters=[{"AttributePath": "UserName", "AttributeValue": username}],
        ):
            users = page.get("Users", [])
            if users:
                return users[0]
        return None  # noqa: TRY300
    except ClientError as e:
        logger.exception("Failed to get user", extra={"username": username, "error": str(e)})
        return None


def get_group_id(identity_store_id: str, group_name: str) -> str | None:
    """Get group ID by name."""
    try:
        paginator = identitystore.get_paginator("list_groups")
        for page in paginator.paginate(
            IdentityStoreId=identity_store_id,
            Filters=[{"AttributePath": "DisplayName", "AttributeValue": group_name}],
        ):
            groups = page.get("Groups", [])
            if groups:
                return groups[0]["GroupId"]
        return None  # noqa: TRY300
    except ClientError as e:
        logger.exception("Failed to get group", extra={"group_name": group_name, "error": str(e)})
        return None


def get_user_group_memberships(identity_store_id: str, user_id: str) -> list[dict]:
    """Get all Quick Suite group memberships for a user."""
    try:
        paginator = identitystore.get_paginator("list_group_memberships_for_member")
        memberships = []

        for page in paginator.paginate(IdentityStoreId=identity_store_id, MemberId={"UserId": user_id}):
            memberships.extend(page.get("GroupMemberships", []))

        quick_suite_memberships = []
        for membership in memberships:
            group_id = membership["GroupId"]
            try:
                group = identitystore.describe_group(IdentityStoreId=identity_store_id, GroupId=group_id)
                if group["DisplayName"] in [g.value for g in QuickSuiteGroup]:
                    quick_suite_memberships.append(membership)
            except ClientError:
                continue

        return quick_suite_memberships  # noqa: TRY300
    except ClientError as e:
        logger.exception("Failed to get user memberships", extra={"user_id": user_id, "error": str(e)})
        return []


def remove_user_from_all_groups(identity_store_id: str, user_id: str) -> None:
    """Remove user from all Quick Suite groups."""
    memberships = get_user_group_memberships(identity_store_id, user_id)

    for membership in memberships:
        try:
            identitystore.delete_group_membership(
                IdentityStoreId=identity_store_id, MembershipId=membership["MembershipId"]
            )
            logger.info(
                "Removed user from group",
                extra={"user_id": user_id, "membership_id": membership["MembershipId"]},
            )
        except ClientError as e:
            logger.warning(
                "Failed to remove user from group",
                extra={"user_id": user_id, "membership_id": membership["MembershipId"], "error": str(e)},
            )


def create_or_update_user(identity_store_id: str, request: CreateUserRequest) -> str:
    """Create or update a user (idempotent)."""
    existing_user = get_user_by_username(identity_store_id, request.username)

    if existing_user:
        user_id = existing_user["UserId"]
        logger.info("User already exists", extra={"username": request.username, "user_id": user_id})
        click.echo(f"⚠ User already exists: {request.username} (ID: {user_id})")
    else:
        try:
            response = identitystore.create_user(
                IdentityStoreId=identity_store_id,
                UserName=request.username,
                Name={"GivenName": request.given_name, "FamilyName": request.family_name},
                DisplayName=f"{request.given_name} {request.family_name}",
                Emails=[{"Value": request.email, "Type": "Work", "Primary": True}],
            )
            user_id = response["UserId"]
            logger.info("Created user", extra={"username": request.username, "user_id": user_id})
            click.echo(f"✓ Created user: {request.username} (ID: {user_id})")
        except ClientError as e:
            logger.exception("Failed to create user", extra={"username": request.username, "error": str(e)})
            click.echo(f"✗ Failed to create user {request.username}: {e}", err=True)
            raise

    if request.group:
        remove_user_from_all_groups(identity_store_id, user_id)

        group_id = get_group_id(identity_store_id, request.group)
        if not group_id:
            logger.error("Group not found", extra={"group_name": request.group})
            click.echo(f"✗ Group not found: {request.group}. Run 'setup-groups' first.", err=True)
            return user_id

        try:
            identitystore.create_group_membership(
                IdentityStoreId=identity_store_id, GroupId=group_id, MemberId={"UserId": user_id}
            )
            logger.info("Added user to group", extra={"user_id": user_id, "group_name": request.group})
            click.echo(f"✓ Added user to group: {request.group}")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConflictException":
                logger.info("User already in group", extra={"user_id": user_id, "group_name": request.group})
                click.echo(f"⚠ User already in group: {request.group}")
            else:
                logger.warning(
                    "Failed to add user to group",
                    extra={"user_id": user_id, "group_name": request.group, "error": str(e)},
                )
                click.echo(f"⚠ Failed to add user to group: {e}")

    return user_id


@click.group()
def cli() -> None:
    """Manage IAM Identity Center users and groups."""
    pass


@cli.command()
@click.option("--identity-store-id", help="Identity Store ID (auto-detected if not provided)")
def setup_groups(identity_store_id: str | None) -> None:
    """Create the required Quick Suite pricing tier groups."""
    if not identity_store_id:
        identity_store_id = get_identity_store_id()

    for tier in QuickSuiteGroup:
        try:
            response = identitystore.create_group(
                IdentityStoreId=identity_store_id,
                DisplayName=tier.value,
                Description=f"Quick Suite {tier.name} tier users",
            )
            logger.info(
                "Created group",
                extra={"group_name": tier.value, "group_id": response["GroupId"]},
            )
            click.echo(f"✓ Created group: {tier.value} (ID: {response['GroupId']})")
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConflictException":
                logger.info("Group already exists", extra={"group_name": tier.value})
                click.echo(f"⚠ Group already exists: {tier.value}")
            else:
                logger.warning("Failed to create group", extra={"group_name": tier.value, "error": str(e)})
                click.echo(f"⚠ Failed to create group {tier.value}: {e}")


@cli.command()
@click.option("--username", required=True, help="Username for the user")
@click.option("--email", required=True, help="Email address")
@click.option("--given-name", required=True, help="First name")
@click.option("--family-name", required=True, help="Last name")
@click.option(
    "--group",
    type=click.Choice([tier.value for tier in QuickSuiteGroup]),
    help="Quick Suite group to add user to",
)
@click.option("--identity-store-id", help="Identity Store ID (auto-detected if not provided)")
def create_user(  # noqa: PLR0913
    username: str,
    email: str,
    given_name: str,
    family_name: str,
    group: str | None,
    identity_store_id: str | None,
) -> None:
    """Create a new user in IAM Identity Center (idempotent)."""
    if not identity_store_id:
        identity_store_id = get_identity_store_id()

    try:
        request = CreateUserRequest(
            username=username,
            email=email,
            given_name=given_name,
            family_name=family_name,
            group=group,
        )
    except Exception as e:
        logger.error("Invalid user data", extra={"error": str(e)})
        click.echo(f"✗ Invalid user data: {e}", err=True)
        sys.exit(1)

    try:
        create_or_update_user(identity_store_id, request)
    except Exception:
        sys.exit(1)


@cli.command()
@click.option("--file", "file_path", required=True, type=click.Path(exists=True), help="JSON file with users")
@click.option("--identity-store-id", help="Identity Store ID (auto-detected if not provided)")
def sync_users(file_path: str, identity_store_id: str | None) -> None:
    """Create or update users from a JSON file (idempotent)."""
    if not identity_store_id:
        identity_store_id = get_identity_store_id()

    try:
        with Path(file_path).open() as f:
            data = json.load(f)
        users_file = UsersFile.model_validate(data)
    except Exception as e:
        logger.error("Failed to parse users file", extra={"file": file_path, "error": str(e)})
        click.echo(f"✗ Failed to parse users file: {e}", err=True)
        sys.exit(1)

    click.echo(f"\nProcessing {len(users_file.users)} user(s)...\n")

    success_count = 0
    error_count = 0

    for user_request in users_file.users:
        try:
            create_or_update_user(identity_store_id, user_request)
            success_count += 1
        except Exception:
            error_count += 1
        click.echo()

    click.echo(f"Summary: {success_count} successful, {error_count} failed")


@cli.command()
@click.option("--user-id", "user_id", help="User ID to delete")
@click.option("--username", help="Username to delete")
@click.option("--identity-store-id", help="Identity Store ID (auto-detected if not provided)")
def delete_user(user_id: str | None, username: str | None, identity_store_id: str | None) -> None:
    """Delete a user from IAM Identity Center."""
    if not user_id and not username:
        click.echo("✗ Must provide either --user-id or --username", err=True)
        sys.exit(1)

    if not identity_store_id:
        identity_store_id = get_identity_store_id()

    if username and not user_id:
        user = get_user_by_username(identity_store_id, username)
        if not user:
            logger.error("User not found", extra={"username": username})
            click.echo(f"✗ User not found: {username}", err=True)
            sys.exit(1)
        user_id = user["UserId"]

    try:
        identitystore.delete_user(IdentityStoreId=identity_store_id, UserId=user_id)
        logger.info("Deleted user", extra={"user_id": user_id})
        click.echo(f"✓ Deleted user: {user_id}")
    except ClientError as e:
        logger.exception("Failed to delete user", extra={"user_id": user_id, "error": str(e)})
        click.echo(f"✗ Failed to delete user: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--user-id", required=True, help="User ID to add to group")
@click.option(
    "--group",
    "group_name",
    required=True,
    type=click.Choice([tier.value for tier in QuickSuiteGroup]),
    help="Group to add user to",
)
@click.option("--identity-store-id", help="Identity Store ID (auto-detected if not provided)")
def add_user_to_group(user_id: str, group_name: str, identity_store_id: str | None) -> None:
    """Add a user to a pricing tier group (removes from other Quick Suite groups)."""
    if not identity_store_id:
        identity_store_id = get_identity_store_id()

    remove_user_from_all_groups(identity_store_id, user_id)

    group_id = get_group_id(identity_store_id, group_name)
    if not group_id:
        logger.error("Group not found", extra={"group_name": group_name})
        click.echo(f"✗ Group not found: {group_name}. Run 'setup-groups' first.", err=True)
        sys.exit(1)

    try:
        response = identitystore.create_group_membership(
            IdentityStoreId=identity_store_id, GroupId=group_id, MemberId={"UserId": user_id}
        )

        logger.info(
            "Added user to group",
            extra={
                "user_id": user_id,
                "group_name": group_name,
                "membership_id": response["MembershipId"],
            },
        )
        click.echo(f"✓ Added user {user_id} to group {group_name}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConflictException":
            logger.info("User already in group", extra={"user_id": user_id, "group_name": group_name})
            click.echo(f"⚠ User already in group: {group_name}")
        else:
            logger.warning(
                "Failed to add user to group",
                extra={"user_id": user_id, "group_name": group_name, "error": str(e)},
            )
            click.echo(f"⚠ Failed to add user to group: {e}")


@cli.command()
@click.option("--identity-store-id", help="Identity Store ID (auto-detected if not provided)")
def list_users(identity_store_id: str | None) -> None:
    """List all users in the Identity Store."""
    if not identity_store_id:
        identity_store_id = get_identity_store_id()

    try:
        paginator = identitystore.get_paginator("list_users")
        users = []

        for page in paginator.paginate(IdentityStoreId=identity_store_id):
            users.extend(page.get("Users", []))

        if not users:
            click.echo("No users found")
            return

        click.echo(f"\nFound {len(users)} user(s):\n")
        for user in users:
            user_id = user["UserId"]
            username = user.get("UserName", "N/A")
            display_name = user.get("DisplayName", "N/A")
            emails = user.get("Emails", [])
            email = emails[0]["Value"] if emails else "N/A"

            click.echo(f"User ID: {user_id}")
            click.echo(f"  Username: {username}")
            click.echo(f"  Display Name: {display_name}")
            click.echo(f"  Email: {email}")
            click.echo()
    except ClientError as e:
        logger.exception("Failed to list users", extra={"error": str(e)})
        click.echo(f"✗ Failed to list users: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--identity-store-id", help="Identity Store ID (auto-detected if not provided)")
def list_groups(identity_store_id: str | None) -> None:
    """List all groups in the Identity Store."""
    if not identity_store_id:
        identity_store_id = get_identity_store_id()

    try:
        paginator = identitystore.get_paginator("list_groups")
        groups = []

        for page in paginator.paginate(IdentityStoreId=identity_store_id):
            groups.extend(page.get("Groups", []))

        if not groups:
            click.echo("No groups found")
            return

        click.echo(f"\nFound {len(groups)} group(s):\n")
        for group in groups:
            group_id = group["GroupId"]
            display_name = group.get("DisplayName", "N/A")
            description = group.get("Description", "N/A")

            click.echo(f"Group ID: {group_id}")
            click.echo(f"  Name: {display_name}")
            click.echo(f"  Description: {description}")
            click.echo()
    except ClientError as e:
        logger.exception("Failed to list groups", extra={"error": str(e)})
        click.echo(f"✗ Failed to list groups: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--namespace", default="default", help="Quick Suite namespace (default: default)")
def assign_groups_to_quick_suite(namespace: str) -> None:
    """Assign Identity Center groups to Quick Suite roles (idempotent)."""
    account_id = sts.get_caller_identity()["Account"]

    click.echo(f"\nAssigning groups to Quick Suite roles in namespace '{namespace}'...\n")

    success_count = 0
    skip_count = 0
    error_count = 0

    for group in QuickSuiteGroup:
        group_name = group.value
        role = QUICKSIGHT_ROLE_MAPPING[group_name]

        try:
            quicksight.create_role_membership(
                MemberName=group_name,
                AwsAccountId=account_id,
                Namespace=namespace,
                Role=role,
            )
            logger.info(
                "Assigned group to Quick Suite role",
                extra={"group": group_name, "role": role, "namespace": namespace},
            )
            click.echo(f"✓ Assigned {group_name} → {role}")
            success_count += 1
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceExistsException":
                logger.info("Group already assigned", extra={"group": group_name, "role": role})
                click.echo(f"⚠ {group_name} already assigned to {role}")
                skip_count += 1
            else:
                logger.exception(
                    "Failed to assign group",
                    extra={"group": group_name, "role": role, "error": str(e)},
                )
                click.echo(f"✗ Failed to assign {group_name}: {e}")
                error_count += 1

    click.echo(f"\nSummary: {success_count} assigned, {skip_count} skipped, {error_count} failed")


if __name__ == "__main__":
    cli()
