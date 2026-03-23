# Development

Guide for building, testing, and contributing to this GitHub Action.

<br/>

## Prerequisites

- Python 3.13+
- Docker
- Make

<br/>

## Setup

```bash
make venv            # Create virtualenv and install dev dependencies
source venv/bin/activate
```

<br/>

## Testing

```bash
make test            # Run unit tests with coverage
make coverage        # Generate HTML coverage report → htmlcov/index.html
```

<br/>

## Workflow

```bash
make check-gh        # Verify gh CLI is installed and authenticated
make branch name=feature-name   # Create feature branch from main
make pr title="feat: add feature"   # Test → push → create PR
```

<br/>

## Docker

Build and test the Docker image locally:

```bash
# Build
docker build -t myaction:local .

# Run (dry-run mode)
docker run --rm \
  -e INPUT_OUTPUT_FILE="output.txt" \
  -e INPUT_DRY_RUN="true" \
  myaction:local
```

<br/>

## Action Testing

Test the action locally using [act](https://github.com/nektos/act) or by pushing to a branch and using `uses: ./`:

```yaml
- name: Test Local Action
  uses: ./
  with:
    output_file: output.txt
    dry_run: 'true'
```

<br/>

## CI/CD Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| `ci.yml` | push (main), PR, dispatch | Unit tests → Docker build → Action integration test |
| `release.yml` | tag push `v*` | GitHub release + major tag update (v1) |
| `changelog-generator.yml` | after release, PR merge | Auto-generate CHANGELOG.md |
| `contributors.yml` | after changelog | Auto-generate CONTRIBUTORS.md |
| `stale-issues.yml` | daily cron | Auto-close stale issues |
| `dependabot-auto-merge.yml` | PR (dependabot) | Auto-merge minor/patch updates |
| `issue-greeting.yml` | issue opened | Welcome message |

### Workflow Chain

```
tag push v* → Create release + update major tag (v1)
                └→ Generate changelog
                      └→ Generate Contributors
```

<br/>

## Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

The release workflow automatically:
1. Creates a GitHub release with notes
2. Updates the major version tag (e.g., `v1` → points to `v1.0.0`)

Users can then reference the action as `uses: YOUR_USERNAME/YOUR_ACTION@v1`.

<br/>

## Conventions

- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `chore:`)
- **paths-ignore**: CI skips `.github/workflows/**` and `**/*.md` changes
- **Testing**: pytest with 90%+ coverage threshold
