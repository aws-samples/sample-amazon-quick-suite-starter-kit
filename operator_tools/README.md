# Amazon Quick Suite Starter Kit Operator Tools

CLI tools for managing Amazon Quick Suite instances post-deployment.

## Documentation

See [Operator Tools Documentation](https://aws-samples.github.io/sample-amazon-quick-suite-starter-kit/operator-tools/) for usage guides.

## Development

```bash
make build     # Install dependencies
make format    # Format Python code
make lint      # Lint Python code
make validate  # Run all checks
```

## Available Tools

- `manage-users` - User and group management
- `monitor` - Usage monitoring

Run `uv run <tool> --help` for usage.

## Structure

- `src/` - CLI tool source code
- `pyproject.toml` - Python dependencies and configuration
