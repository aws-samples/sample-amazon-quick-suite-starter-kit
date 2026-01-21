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

## Documentation

**[View Full Documentation](https://special-adventure-5lgmjjy.pages.github.io/)**

Complete setup guides, architecture details, and operator tools are available in the documentation site.

## Architecture

![Authentication Flow](docs/images/auth-flow.png)

Users authenticate through AWS IAM Identity Center to access Amazon Quick Suite. The starter kit automates the deployment and configuration of both services.

## Quick Links

1. [Getting Started](https://special-adventure-5lgmjjy.pages.github.io/getting-started/) - Deploy in ~15 minutes
2. [Architecture](https://special-adventure-5lgmjjy.pages.github.io/architecture/) - How it works
3. [Operator Tools](https://special-adventure-5lgmjjy.pages.github.io/operator-tools/) - Manage users and monitor usage
4. [Cleanup](https://special-adventure-5lgmjjy.pages.github.io/cleanup/) - Remove resources

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
