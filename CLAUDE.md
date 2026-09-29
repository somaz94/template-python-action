# CLAUDE.md — YOUR_ACTION

A Python-based GitHub Action (Docker container action).

## Build & Test

```bash
make venv        # Create virtualenv
make test        # Unit tests with coverage
make coverage    # Generate HTML coverage report
make lint        # Lint with ruff (make lint-fix to auto-fix)
make format      # Format with ruff (make format-check to verify)
make ci          # Lint + format check + unit tests
make clean       # Remove artifacts
```

## Project Structure

```
app/
  main.py                    # Entry point with ActionRunner
  config.py                  # Load INPUT_* env vars (AppConfig dataclass)
  action.py                  # Core action logic
  output.py                  # GitHub Actions output helpers
tests/
  conftest.py                # Shared fixtures
  test_config.py
  test_action.py
  test_output.py
action.yml                   # Action metadata (inputs/outputs)
Dockerfile                   # Multi-stage build (python:3.14-slim)
requirements-dev.txt         # pytest, pytest-cov, ruff (pinned)
```

## Key Concepts

- **action.yml**: Defines inputs, outputs, and Docker entrypoint
- **config**: Reads `INPUT_*` environment variables set by GitHub Actions
- **output**: Writes to `GITHUB_OUTPUT` file for action outputs
- **Dockerfile**: Multi-stage build for minimal runtime image
- **Testing**: pytest with pytest-cov, 90%+ coverage threshold

## CI

- `ci.yml` — Lint (ruff) and unit tests (pytest), Docker build & dry-run, action integration test
