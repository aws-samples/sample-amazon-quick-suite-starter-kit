# Architecture

Overview of how Amazon Quick Suite integrates with [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/).

## Authentication Flow

![Authentication Flow](images/auth-flow.png)

Users authenticate through AWS IAM Identity Center to access Amazon Quick Suite:

1. User initiates login to Amazon Quick Suite
2. Amazon Quick Suite redirects to AWS IAM Identity Center for authentication
3. AWS IAM Identity Center validates credentials and returns authentication token
4. Amazon Quick Suite grants access based on user's assigned role

## Components

### AWS IAM Identity Center

[AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) manages user identities and group memberships. Groups are mapped to Amazon Quick Suite roles.

**Identity Provider Options:**

This starter kit creates an account-level AWS IAM Identity Center instance by default for quick setup. If you have an existing instance (account or organizational level) with a federated identity provider, you can provide the instance ARN via configuration. Ensure your federated groups are mapped to the appropriate Quick Suite roles.

**Admin Group:**

The deployment automatically creates a `QUICK_SUITE_ADMIN` group in AWS IAM Identity Center, which is required for Quick Suite setup. If you have an existing admin group synced from your federated identity provider, you can modify the `ADMIN_PRO_GROUP_NAME` constant in the Lambda function to use your group name instead.

**Note:** The `manage-users` tool manages users directly in AWS IAM Identity Center, not in external identity providers.

### Amazon Quick Suite

[Amazon Quick Suite](https://aws.amazon.com/quicksuite/) is an AI-powered digital workspace that uses AWS IAM Identity Center for authentication and authorization. The service uses [Amazon QuickSight](https://docs.aws.amazon.com/quicksight/) APIs under the hood.

### CDK Infrastructure

Deploys:

- AWS IAM Identity Center instance (or uses existing)
- Amazon Quick Suite subscription
- AWS Lambda functions for resource management

### Operator Tools

Post-deployment CLI tools for managing users and monitoring usage. See the [Operator Tools documentation](operator-tools/index.md) for details.

## See Also

- [Getting Started](getting-started.md)
- [User Management Runbook](operator-tools/user-management-runbook.md)
