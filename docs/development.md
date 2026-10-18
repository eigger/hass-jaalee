# Jaalee Development Guide

Guidelines for testing, linting, and contributing to `hass-jaalee`.

## Prerequisites

- Python 3.13 or 3.14
- Virtual environment (`venv` or `uv`)

## Setup Development Environment

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install linting and test dependencies
pip install -r requirements_lint.txt
pip install -r requirements_test.txt
```

## Running Tests

```bash
# Run full test suite
pytest tests/components/jaalee/ -v

# Run with coverage
pytest tests/components/jaalee/ --cov=custom_components/jaalee
```

## Linting and Code Formatting

```bash
# Check code style with Ruff
ruff check .

# Check code formatting
ruff format --check .

# Auto-fix formatting and linting
ruff check . --fix
ruff format .
```
