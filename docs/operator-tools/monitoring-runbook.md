# Monitoring Runbook

Guide for monitoring Quick Suite usage and users using the `monitor` tool.

## Purpose

The `monitor` tool provides visibility into Quick Suite users, groups, and account status.

## Prerequisites

- Quick Suite deployed and configured
- Access to AWS account with Quick Suite permissions

## Tools

### account-summary

Displays Quick Suite account overview with user counts and role distribution.

```bash
uv run monitor account-summary
```

Shows:

- Total users
- Active vs inactive users
- Users by role
- Total groups

---

### list-users

Lists all Quick Suite users with their roles and status.

```bash
uv run monitor list-users
```

**Options:**

- `--namespace`: Quick Suite namespace (default: "default")

---

### list-groups

Lists all Quick Suite groups.

```bash
uv run monitor list-groups
```

**Options:**

- `--namespace`: Quick Suite namespace (default: "default")

---

### list-group-members

Lists all members of a specific Quick Suite group.

```bash
uv run monitor list-group-members --group-name QUICK_SUITE_ADMIN
```

**Options:**

- `--group-name`: Group name (required)
- `--namespace`: Quick Suite namespace (default: "default")

## See Also

- [User Management Runbook](user-management-runbook.md)
- [Getting Started](../getting-started.md)
