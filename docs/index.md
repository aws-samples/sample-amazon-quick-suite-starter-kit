# Amazon Quick Suite Starter Kit

Automated deployment of [Amazon Quick Suite](https://aws.amazon.com/quicksuite/) using [AWS IAM Identity Center](https://aws.amazon.com/iam/identity-center/) as an identity provider.

## What is Amazon Quick Suite?

[Amazon Quick Suite](https://aws.amazon.com/quicksuite/) is an agentic AI-powered digital workspace that combines business intelligence, research, automation, and AI agents in one integrated experience. It helps teams:

- Answer questions using AI agents across enterprise data
- Automate workflows with Quick Flows and Quick Automate
- Conduct research with Quick Research
- Create dashboards and visualizations with Quick Sight
- Collaborate in shared Spaces

!!! note "QuickSight Service Name"
Amazon Quick Suite is the new name for Amazon QuickSight. The underlying AWS service still uses QuickSight APIs, service principals, and console pages. This is why you'll see `quicksight` in IAM policies, CLI commands, and CloudFormation resources. See the [Amazon QuickSight documentation](https://docs.aws.amazon.com/quicksight/) for API references.

## What This Starter Kit Provides

This starter kit automates the deployment and management of Quick Suite with:

- **Infrastructure as Code** - AWS CDK deployment of Quick Suite with [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/)
- **User Management** - CLI tools for managing users and groups
- **Monitoring** - Tools to track usage and costs
- **Best Practices** - Pre-configured security and governance settings

## Quick Start

New to this project? Here's your path:

1. **[Getting Started](getting-started.md)** - Deploy Quick Suite in ~15 minutes
2. **[Architecture](architecture.md)** - Understand how authentication works
3. **[Operator Tools](operator-tools/index.md)** - Manage users and monitor usage
4. **[Cleanup](cleanup.md)** - Remove resources when done

## Role Mappings

This starter kit uses [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) groups mapped to Quick Suite roles:

| Identity Center Group      | Quick Suite Role | Notes                                         |
| -------------------------- | ---------------- | --------------------------------------------- |
| **QUICK_SUITE_ADMIN**      | Admin Pro        | Created automatically during deployment       |
| **QUICK_SUITE_ENTERPRISE** | Author Pro       | Create using the `manage-users` operator tool |
| **QUICK_SUITE_PRO**        | Reader Pro       | Create using the `manage-users` operator tool |

For role capabilities and pricing, see [Amazon Quick Suite Pricing](https://aws.amazon.com/quicksuite/pricing/).

!!! tip "Using Your Own Admin Group"
If you have an existing admin group synced from your federated identity provider, you can configure the deployment to use it instead of creating `QUICK_SUITE_ADMIN`. See [Getting Started](getting-started.md#step-2-configure-deployment-optional) for configuration options.

## Documentation

- [Getting Started](getting-started.md) - Deployment guide
- [Architecture](architecture.md) - How it works
- [Operator Tools](operator-tools/index.md) - Management runbooks
- [Cleanup Instructions](cleanup.md) - Remove resources

## Support

For issues or questions, please [open an issue](https://github.com/aws-samples/sample-amazon-quick-suite-starter-kit/issues) on GitHub.
