# Getting Started

This guide walks you through deploying Amazon Quick Suite with [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/).

## Prerequisites

- [AWS CLI](https://docs.aws.amazon.com/cli/) configured with appropriate credentials
- Node.js 18+ and npm
- Python 3.12+
- uv package manager
- Docker (for Lambda bundling)
- AWS CDK CLI: `npm install -g aws-cdk`

!!! warning "Region Restrictions"

    Amazon Quick Suite AI capabilities are only available in certain AWS regions. Check the [Quick Suite FAQs](https://aws.amazon.com/quicksuite/faqs/) for current regional availability.

## Step 1: Install Dependencies

```bash
npm install
```

## Step 2: Configure Deployment (Optional)

You can customize the deployment via `cdk.json` context or command line parameters:

### Configuration Options

**IDENTITY_CENTER_INSTANCE_ARN** (optional)  
Existing [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) instance ARN. If not provided, a new instance will be created.

**QUICK_SUITE_ACCOUNT_NAME** (default: `QuickSuiteStarterKit`)  
Display name for your Quick Suite account.

!!! danger "Important"

    - End users must type this name when signing in - choose wisely!
    - **Cannot be changed** after account creation
    - Must be **globally unique** across all AWS accounts
    - Length: 1-62 characters
    - Must start with a letter or digit
    - Can contain letters, digits, and hyphens
    - Cannot end with a hyphen

**QUICK_SUITE_ADMIN_EMAIL** (default: `admin@example.com`)  
Email address for Quick Suite admin notifications. Please choose a real email to get important updates concerning your account.

**QUICK_SUITE_ADMIN_GROUP_NAME** (default: `QUICK_SUITE_ADMIN`)  
Name of the [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) group for Quick Suite administrators. This group is automatically created during deployment if it does not exist and is mapped to the Admin Pro role.

### Example Configuration

=== "cdk.json"

    ```json
    {
      "context": {
        "IDENTITY_CENTER_INSTANCE_ARN": "arn:aws:sso:::instance/ssoins-xxxxx",
        "QUICK_SUITE_ACCOUNT_NAME": "MyCompanyQuickSuite",
        "QUICK_SUITE_ADMIN_EMAIL": "quicksuite-admin@mycompany.com",
        "QUICK_SUITE_ADMIN_GROUP_NAME": "QuickSuiteAdmins"
      }
    }
    ```

=== "Command Line"

    ```bash
    npm run cdk deploy \
      -c IDENTITY_CENTER_INSTANCE_ARN=arn:aws:sso:::instance/ssoins-xxxxx \
      -c QUICK_SUITE_ACCOUNT_NAME=MyCompanyQuickSuite \
      -c QUICK_SUITE_ADMIN_EMAIL=quicksuite-admin@mycompany.com \
      -c QUICK_SUITE_ADMIN_GROUP_NAME=QuickSuiteAdmins
    ```

## Step 3: Bootstrap AWS Account

If you haven't already bootstrapped your AWS account for CDK:

```bash
npx cdk bootstrap
```

## Step 4: Deploy Infrastructure

```bash
npm run cdk deploy
```

This deployment will:

1. Create or use your existing [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) instance
2. Deploy Quick Suite infrastructure using a custom resource Lambda
3. Create the `QUICK_SUITE_ADMIN` group automatically (required for setup)

!!! warning "Do Not Access Quick Suite Yet"

    After deployment completes, **do not** navigate to <https://us-east-1.quicksight.aws.amazon.com> yet. You must create an admin user first (Step 6), otherwise you won't be able to sign in.

!!! note "Using Existing Admin Group"

    If you have an existing admin group synced from your federated identity provider to [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/), you can modify the CDK code to use that group name instead of `QUICK_SUITE_ADMIN`.

## Step 5: Enable Email OTP for API-Created Users

!!! danger "CRITICAL: Required Before Creating Users"

    This is a **one-time manual step** that you must complete before creating users via the operator tools. Without this setting, users created via API will not receive the invite to sign in.

**Steps:**

1. Open the [IAM Identity Center console](https://console.aws.amazon.com/singlesignon)
2. Choose **Settings**
3. Choose the **Authentication** tab
4. In the **Standard authentication** section, choose **Configure**
5. Check the **Send email OTP** checkbox
6. Choose **Save**

This setting allows users created via API to receive a verification email on their first sign-in attempt, enabling them to set their password. Learn more in the [AWS IAM Identity Center documentation](https://docs.aws.amazon.com/singlesignon/).

## Step 6: Create Your First Admin User

!!! danger "CRITICAL: Do This Before Accessing Quick Suite"

    You **must** create an admin user before attempting to access Quick Suite. Without a user in the `QUICK_SUITE_ADMIN` group, you cannot sign in.

Navigate to the operator tools directory:

```bash
cd operator_tools
```

### Create Your First Admin User

```bash
uv run manage-users create-user \
  --username admin \
  --email admin@example.com \
  --given-name Admin \
  --family-name User \
  --group QUICK_SUITE_ADMIN
```

### Complete User Email Verification

After you create a user, they must verify their email and set up authentication in [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/):

1. **Email Verification**: The user will receive an email with subject "Your administrator has requested you to verify your email address". They should follow the instructions in the email.

2. **First Sign-In to IAM Identity Center**: The user enters their username and sets up MFA.

3. **Set Password**: The user creates their password.

!!! tip "Password Requirements"

    Passwords must be at least 8 characters and contain uppercase, lowercase, numbers, and special characters.

## Step 7: Access Quick Suite

Now you can access Quick Suite:

1. Navigate to <https://us-east-1.quicksight.aws.amazon.com> (replace `us-east-1` with your deployed region if different)
2. Enter your Quick Suite account name (e.g., `QuickSuiteStarterKit`)
3. You'll be redirected to [AWS IAM Identity Center](https://docs.aws.amazon.com/singlesignon/) login
4. Sign in with your admin user credentials

!!! success "You're Ready!"

    Your Quick Suite environment is now fully configured and ready to use!

## Step 8: Verify Deployment

Check your deployment:

```bash
uv run monitor account-summary
```

## Next Steps

### Adding More Users

To add users with different roles (Author Pro or Reader Pro):

1. Create the additional groups: `uv run manage-users setup-groups`
2. Map groups to Quick Suite roles: `uv run manage-users assign-groups-to-quick-suite`
3. Create users with appropriate groups

See the [User Management Runbook](operator-tools/user-management-runbook.md) for detailed instructions.

### Other Resources

- [Monitoring Runbook](operator-tools/monitoring-runbook.md) - Track usage
- [Architecture Details](https://builder.aws.com/content/33FWxLBkVVy9zWYOppQKWcj7UTz/accelerate-your-amazon-quick-suite-implementation-starter-kit-for-rapid-deployment) - Blog post
