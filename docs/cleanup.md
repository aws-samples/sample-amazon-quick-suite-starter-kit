# Cleanup and Deletion

This guide explains how to properly remove your Amazon Quick Suite deployment to avoid ongoing costs.

## Cleanup Process

To remove all resources:

1. **Delete the Quick Suite subscription** - Use the [Amazon QuickSight console](https://console.aws.amazon.com/quicksight/) or AWS CLI command `aws quicksight delete-account-subscription` to delete the subscription. This must be done before destroying the stack.

2. **Destroy the CDK stack** - Run `npm run cdk destroy` to remove the Lambda function, IAM roles, and other infrastructure.

3. **Remove IAM Identity Center groups** (optional) - Use the [IAM Identity Center console](https://console.aws.amazon.com/singlesignon) or AWS CLI to delete groups created during setup if no longer needed.

## Important Notes

The custom resource handler does not automatically delete the Quick Suite subscription during stack deletion to prevent accidental data loss. You must delete the subscription separately before running `npm run cdk destroy`.

[AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) groups are not automatically deleted and will remain in your Identity Center instance after stack deletion.

## Next Steps

After cleanup, you may want to:

- Review your [AWS billing dashboard](https://console.aws.amazon.com/billing/) to confirm all charges have stopped
- Remove any remaining CloudWatch log groups if desired
- Delete the CDK bootstrap stack if you're not using CDK for other projects
