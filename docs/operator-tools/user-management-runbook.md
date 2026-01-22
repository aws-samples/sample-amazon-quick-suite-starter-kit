# User Management Runbook

Guide for managing [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) users and Quick Suite access using the `manage-users` tool.

## Purpose

The `manage-users` tool manages AWS IAM Identity Center users and groups, and assigns them to Quick Suite roles. All operations are idempotent.

!!! info "Using Custom Group Names"

    This tool uses default group names: `QUICK_SUITE_ADMIN`, `QUICK_SUITE_ENTERPRISE`, and `QUICK_SUITE_PRO`. If you have custom group names from your federated identity provider, modify the `QuickSuiteGroup` enum and `QUICKSIGHT_ROLE_MAPPING` dictionary in `operator_tools/src/manage_users.py` before using these tools.

## Prerequisites

- Quick Suite deployed via CDK
- Access to AWS account with [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) permissions

## Tools

### setup-groups

Creates the Quick Suite pricing tier groups in [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/).

!!! warning "Run This Before Adding Non-Admin Users"

    You must run this command before creating users with `QUICK_SUITE_ENTERPRISE` or `QUICK_SUITE_PRO` groups. Without these groups, you cannot assign users to Author Pro or Reader Pro roles.

```bash
uv run manage-users setup-groups
```

Creates:

- `QUICK_SUITE_ENTERPRISE` (Author Pro)
- `QUICK_SUITE_PRO` (Reader Pro)

Note: `QUICK_SUITE_ADMIN` is created automatically during deployment.

---

### create-user

Creates a single user in [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) and optionally assigns them to a group.

```bash
uv run manage-users create-user \
  --username johndoe \
  --email john.doe@example.com \
  --given-name John \
  --family-name Doe \
  --group QUICK_SUITE_ADMIN
```

For all available options:

```bash
uv run manage-users create-user --help
```

---

### sync-users

Batch creates or updates users from a JSON file.

```bash
uv run manage-users sync-users --file users.json
```

**Example users.json:**

```json
{
  "users": [
    {
      "username": "admin.user",
      "email": "admin@example.com",
      "given_name": "Admin",
      "family_name": "User",
      "group": "QUICK_SUITE_ADMIN"
    }
  ]
}
```

---

### assign-groups-to-quick-suite

Maps [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) groups to Quick Suite roles.

!!! danger "Prerequisites"

    - Run `setup-groups` first to create the groups (if using default group names)
    - Groups must exist in AWS IAM Identity Center before running this command
    - If groups don't exist, the command will fail with an error for each missing group

```bash
uv run manage-users assign-groups-to-quick-suite
```

For all available options:

```bash
uv run manage-users assign-groups-to-quick-suite --help
```

**Default Mappings:**

See the [Role Mappings table](../index.md#role-mappings) for group-to-role assignments.

---

### add-user-to

Assigns a user to a Quick Suite group. Automatically removes user from other Quick Suite groups.

```bash
uv run manage-users add-user-to \
  --user-id <user-id> \
  --group QUICK_SUITE_ENTERPRISE
```

For all available options:

```bash
uv run manage-users add-user-to --help
```

---

### delete-user

Removes a user from [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/).

```bash
# By username
uv run manage-users delete-user --username johndoe

# By user ID
uv run manage-users delete-user --user-id <user-id>
```

---

### list-users

Lists all users in [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/).

```bash
uv run manage-users list-users
```

---

### list-groups

Lists all groups in [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/).

```bash
uv run manage-users list-groups
```

## See Also

- [Monitoring Runbook](monitoring-runbook.md)
- [Getting Started](../getting-started.md)
