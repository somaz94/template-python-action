# CLAUDE.md — YOUR_ACTION

A Python-based GitHub Action (Docker container action).

## Build & Test

```bash
make venv        # Create virtualenv
make test        # Unit tests with coverage
make coverage    # Generate HTML coverage report
make clean       # Remove artifacts
```

## Commit Guidelines

- Do not include `Co-Authored-By` lines in commit messages.
- Use Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `chore:`)
- Do not push to remote. Only commit. The user will push manually.

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
```

## Key Concepts

- **action.yml**: Defines inputs, outputs, and Docker entrypoint
- **config**: Reads `INPUT_*` environment variables set by GitHub Actions
- **output**: Writes to `GITHUB_OUTPUT` file for action outputs
- **Dockerfile**: Multi-stage build for minimal runtime image
- **Testing**: pytest with pytest-cov, 90%+ coverage threshold

## CI

- `ci.yml` — Unit tests (pytest), Docker build & dry-run, action integration test

## Language

- Communicate with the user in Korean.
- All documentation and code comments must be written in English.
