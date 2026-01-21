"""Custom resource handler for Quick Suite setup with IAM Identity Center."""

from typing import Any

import boto3
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError
from crhelper import CfnResource

from common.observability import logger

helper = CfnResource()
quicksight = boto3.client("quicksight")
identitystore = boto3.client("identitystore")


def get_existing_group_id(identity_store_id: str, group_name: str) -> str | None:  # noqa: D103
    paginator = identitystore.get_paginator("list_groups")
    page_iterator = paginator.paginate(
        IdentityStoreId=identity_store_id, Filters=[{"AttributePath": "DisplayName", "AttributeValue": group_name}]
    )

    for page in page_iterator:
        if page["Groups"]:
            return page["Groups"][0]["GroupId"]

    return None


def create_identity_store_group(identity_store_id: str, group_name: str) -> str:  # noqa: D103
    response = identitystore.create_group(
        IdentityStoreId=identity_store_id, DisplayName=group_name, Description="Quick Suite Admin Pro Group"
    )
    group_id = response["GroupId"]
    logger.info(f"Created group {group_name} with ID {group_id}")
    return group_id


def ensure_identity_store_group(identity_store_id: str, group_name: str) -> str:  # noqa: D103
    existing_group_id = get_existing_group_id(identity_store_id, group_name)

    if existing_group_id:
        logger.info(f"Group {group_name} already exists with ID {existing_group_id}")
        return existing_group_id

    return create_identity_store_group(identity_store_id, group_name)


def check_quicksight_subscription_exists(account_id: str) -> bool:  # noqa: D103
    try:
        response = quicksight.describe_account_subscription(AwsAccountId=account_id)
        status = response["AccountInfo"]["AccountSubscriptionStatus"]
    except ClientError as error:
        if error.response["Error"]["Code"] == "ResourceNotFoundException":
            return False
        raise
    else:
        return status not in ["UNSUBSCRIBED", "UNSUBSCRIBE_IN_PROGRESS"]


def create_quicksight_subscription(  # noqa: D103
    account_id: str, account_name: str, admin_email: str, identity_center_arn: str, admin_group_name: str
) -> None:
    quicksight.create_account_subscription(
        Edition="ENTERPRISE",
        AuthenticationMethod="IAM_IDENTITY_CENTER",
        AwsAccountId=account_id,
        AccountName=account_name,
        NotificationEmail=admin_email,
        IAMIdentityCenterInstanceArn=identity_center_arn,
        AdminProGroup=[admin_group_name],
    )
    logger.info("Quick Suite account subscription created")


def ensure_quicksight_subscription(  # noqa: D103
    account_id: str, account_name: str, admin_email: str, identity_center_arn: str, admin_group_name: str
) -> None:
    if check_quicksight_subscription_exists(account_id):
        logger.info("Quick Suite account subscription already exists")
        return

    create_quicksight_subscription(account_id, account_name, admin_email, identity_center_arn, admin_group_name)


@helper.create
def create(event: dict[str, Any], _context: LambdaContext) -> str:  # noqa: D103
    logger.info("Creating Quick Suite resources")
    props = event["ResourceProperties"]
    account_id = event["StackId"].split(":")[4]
    identity_center_arn = props["IdentityCenterInstanceArn"]
    identity_store_id = props["IdentityStoreId"]
    account_name = props["AccountName"]
    admin_email = props["AdminEmail"]
    admin_group_name = props["AdminGroupName"]

    ensure_identity_store_group(identity_store_id, admin_group_name)
    ensure_quicksight_subscription(account_id, account_name, admin_email, identity_center_arn, admin_group_name)

    return account_id


@helper.update
def update(event: dict[str, Any], _context: LambdaContext) -> str:  # noqa: D103
    logger.info("Update called - ensuring resources exist")
    return create(event, _context)


@helper.delete
def delete(_event: dict[str, Any], _context: LambdaContext) -> None:  # noqa: D103
    logger.info("Delete called - Quick Suite subscription must be deleted manually")
    logger.info("See documentation for manual deletion instructions")


@logger.inject_lambda_context
def handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:  # noqa: D103
    logger.info("Received event", extra={"event": event})
    return helper(event, context)
