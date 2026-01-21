<div align="center">

# Amazon Quick Suite Starter Kit

Starter kit for deploying [Amazon Quick Suite](https://aws.amazon.com/quicksuite/) with [AWS IAM Identity Center](https://aws.amazon.com/iam/identity-center/)

<div align="center">
  <a href="https://github.com/aws-samples/sample-amazon-quick-suite-starter-kit/graphs/commit-activity"><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/aws-samples/sample-amazon-quick-suite-starter-kit"/></a>
  <a href="https://github.com/aws-samples/sample-amazon-quick-suite-starter-kit/issues"><img alt="GitHub open issues" src="https://img.shields.io/github/issues/aws-samples/sample-amazon-quick-suite-starter-kit"/></a>
  <a href="https://github.com/aws-samples/sample-amazon-quick-suite-starter-kit/pulls"><img alt="GitHub open pull requests" src="https://img.shields.io/github/issues-pr/aws-samples/sample-amazon-quick-suite-starter-kit"/></a>
  <a href="https://github.com/aws-samples/sample-amazon-quick-suite-starter-kit/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/aws-samples/sample-amazon-quick-suite-starter-kit"/></a>
</div>

</div>

## What is This?

This starter kit automates the deployment of Amazon Quick Suite (formerly Amazon QuickSight) with AWS IAM Identity Center for authentication. It provides:

- Infrastructure as Code using AWS CDK
- Automated user and group management
- Monitoring and usage tracking tools
- Pre-configured security best practices

## Architecture

![Authentication Flow](docs/images/auth-flow.png)

Users authenticate through AWS IAM Identity Center to access Amazon Quick Suite. The starter kit automates the deployment and configuration of both services.

## Quick Start

Ready to deploy? Follow our complete documentation:

**📚 [Full Documentation](https://aws-samples.github.io/sample-amazon-quick-suite-starter-kit/)**

Or jump directly to:

1. **[Overview](https://aws-samples.github.io/sample-amazon-quick-suite-starter-kit/)** - What is Quick Suite and this starter kit
2. **[Getting Started](https://aws-samples.github.io/sample-amazon-quick-suite-starter-kit/getting-started/)** - Deploy in ~15 minutes
3. **[Architecture](https://aws-samples.github.io/sample-amazon-quick-suite-starter-kit/architecture/)** - How it works
4. **[Operator Tools](https://aws-samples.github.io/sample-amazon-quick-suite-starter-kit/operator-tools/)** - Manage users and monitor usage
5. **[Cleanup](https://aws-samples.github.io/sample-amazon-quick-suite-starter-kit/cleanup/)** - Remove resources

## Project Structure

- `/lib` - CDK infrastructure (TypeScript)
- `/lambdas` - Lambda functions (Python)
- `/operator_tools` - Management CLI tools (Python)
- `/docs` - Documentation source (MkDocs)

## Contributing

If you find this starter kit helpful, please ⭐ star the repository!

For feature requests or bug reports, please [open an issue](https://github.com/aws-samples/sample-amazon-quick-suite-starter-kit/issues/new).

For development and contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

See [LICENSE](./LICENSE) file.

## Contributors

<a href="https://github.com/aws-samples/sample-amazon-quick-suite-starter-kit/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=aws-samples/sample-amazon-quick-suite-starter-kit" />
</a>
