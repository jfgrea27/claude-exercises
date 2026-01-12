# List available commands
default:
    @just --list

# Install dependencies
install:
    uv sync --extra dev

# Run the development server
serve:
    uvicorn books_api.server:app --reload --app-dir books-api/src

# Run the MCP server
mcp:
    mcp run books-mcp/src/books_mcp/server.py

# Run tests
test *ARGS:
    pytest {{ARGS}}

# Run tests with coverage (fails if below 80%)
test-cov:
    pytest --cov=books-api/src/books_api --cov-report=term-missing --cov-fail-under=80

# Lint code
lint:
    ruff check .

# Format code
fmt:
    ruff format .
    ruff check --fix .

# Type check
typecheck:
    mypy books-api

# Run all checks (lint, typecheck, test with coverage)
check: lint typecheck test-cov
