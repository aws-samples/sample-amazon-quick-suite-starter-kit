.PHONY: build format lint validate

build:
	@echo "Building Python package..."
	uv sync --all-extras
	@echo "Generating requirements.txt for deployment..."
	uv export --no-hashes --format requirements-txt --output-file src/requirements.txt

format:
	@echo "Formatting Python code..."
	uv run ruff format src/

lint:
	@echo "Linting Python code..."
	uv run ruff check src/ --fix

validate: format lint build
	@echo "✓ All checks passed!"
