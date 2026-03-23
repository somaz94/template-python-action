# template-python-action

A GitHub template repository for building Python-based GitHub Actions (Docker container actions) with automated CI/CD workflows.

<br/>

## What's Included

| Category | Files | Description |
|----------|-------|-------------|
| **Action** | `action.yml` | Action metadata with example inputs/outputs |
| **Docker** | `Dockerfile`, `.dockerignore` | Multi-stage build (python:3.14-slim) |
| **Python Code** | `app/` | Entry point, action logic, config loader, output helpers |
| **Build** | `Makefile` | test, coverage, clean |
| **CI/CD** | `.github/workflows/` | CI (test + Docker + action test), release, changelog, contributors |
| **Config** | `.github/dependabot.yml` | Weekly dependency updates (Docker + Actions + pip) |
| **Docs** | `CLAUDE.md`, `docs/` | Project guidelines and development guide |

<br/>

## Quick Start

<br/>

### 1. Create from Template

Click **"Use this template"** on GitHub, or:

```bash
gh repo create my-action --template somaz94/template-python-action --public --clone
cd my-action
```

<br/>

### 2. Replace Placeholders

| Placeholder | Replace With | Example |
|-------------|-------------|---------|
| `YOUR_USERNAME` | Your GitHub username | `somaz94` |
| `YOUR_ACTION` | Your repository name | `my-awesome-action` |
| `YOUR_GITLAB_GROUP` | Your GitLab group (for mirror) | `backup6695808` |

Quick replace:

```bash
# macOS
find . -type f -not -path './.git/*' -exec sed -i '' \
  -e 's/YOUR_USERNAME/somaz94/g' \
  -e 's/YOUR_ACTION/my-awesome-action/g' \
  -e 's/YOUR_GITLAB_GROUP/backup6695808/g' {} +

# Linux
find . -type f -not -path './.git/*' -exec sed -i \
  -e 's/YOUR_USERNAME/somaz94/g' \
  -e 's/YOUR_ACTION/my-awesome-action/g' \
  -e 's/YOUR_GITLAB_GROUP/backup6695808/g' {} +
```

<br/>

### 3. Build & Test

```bash
make venv     # Create virtualenv
make test     # Run unit tests with coverage

# Docker test
docker build -t myaction:local .
docker run --rm -e INPUT_DRY_RUN=true myaction:local
```

<br/>

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point with ActionRunner
│   ├── config.py            # Load INPUT_* env vars (AppConfig)
│   ├── action.py            # Core action logic (replace this)
│   └── output.py            # GitHub Actions output helpers
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── test_config.py
│   ├── test_action.py
│   └── test_output.py
├── .github/
│   ├── workflows/
│   │   ├── ci.yml               # CI: test, Docker build, action test
│   │   ├── release.yml          # GitHub release + major tag update
│   │   ├── changelog-generator.yml
│   │   ├── contributors.yml
│   │   ├── dependabot-auto-merge.yml
│   │   ├── stale-issues.yml
│   │   ├── issue-greeting.yml
│   │   └── gitlab-mirror.yml
│   ├── dependabot.yml
│   └── release.yml              # Release note categories
├── scripts/
│   └── create-pr.sh             # Auto-generate PR body
├── action.yml                   # Action metadata (inputs/outputs)
├── Dockerfile                   # Multi-stage build
├── .dockerignore
├── .gitattributes
├── .gitignore
├── .coveragerc
├── Makefile
├── CLAUDE.md
├── LICENSE
├── docs/
│   └── DEVELOPMENT.md
└── README.md
```

<br/>

## How It Works

### Action Flow

```
GitHub Actions runner
  → Docker build (Dockerfile)
    → Reads INPUT_* env vars (app/config.py)
    → Executes action logic (app/action.py)
    → Writes GITHUB_OUTPUT (app/output.py)
```

### Key Files to Modify

1. **`action.yml`** — Define your inputs, outputs, and branding
2. **`app/config.py`** — Add fields for your inputs
3. **`app/action.py`** — Replace with your action logic
4. **`Dockerfile`** — Add runtime dependencies (e.g., `git`, `curl`)

<br/>

## Makefile Targets

```bash
make help            # Show all targets
make venv            # Create virtualenv and install dev dependencies
make test            # Run unit tests with coverage
make coverage        # Generate HTML coverage report
make branch name=x   # Create feature branch feat/x
make pr title="..."  # Test → push → create PR
make clean           # Remove venv, cache, and artifacts
```

<br/>

## CI/CD Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| `ci.yml` | push (main), PR, dispatch | Unit tests → Docker build & dry-run → Action integration test |
| `release.yml` | tag push `v*` | GitHub release + major tag update (v1) |
| `changelog-generator.yml` | after release, PR merge | Auto-generate CHANGELOG.md |
| `contributors.yml` | after changelog | Auto-generate CONTRIBUTORS.md |
| `dependabot-auto-merge.yml` | dependabot PR | Auto-merge minor/patch updates |
| `stale-issues.yml` | daily cron | Auto-close stale issues (30d + 7d) |
| `issue-greeting.yml` | issue opened | Welcome message |
| `gitlab-mirror.yml` | push to main | Mirror to GitLab |

<br/>

### Workflow Chain

```
tag push v* → Create release + update major tag (v1)
                └→ Generate changelog
                      └→ Generate Contributors
```

<br/>

## GitHub Secrets Required

| Secret | Usage |
|--------|-------|
| `PAT_TOKEN` | Release, major tag update, contributors (cross-repo access) |
| `GITLAB_TOKEN` | GitLab mirror (optional) |

> `GITHUB_TOKEN` is automatically provided by GitHub Actions.

<br/>

## Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

The release workflow automatically:
1. Creates a GitHub release with generated notes
2. Updates the major version tag (`v1` → points to `v1.0.0`)

Users reference your action as:

```yaml
- uses: YOUR_USERNAME/YOUR_ACTION@v1
```

<br/>

## Key Differences from Go Action Template

| | `template-go-action` | `template-python-action` |
|---|---|---|
| Language | Go | Python |
| Docker base | golang:alpine → alpine | python:3.14-slim |
| Config | `internal/config/` (Go structs) | `app/config.py` (dataclass) |
| Testing | `go test` | `pytest` with `pytest-cov` |
| Build | `make build` (binary) | No build step (interpreted) |
| Dependabot | Docker + Actions + Go modules | Docker + Actions + pip |

<br/>

## Conventions

- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `chore:`)
- **paths-ignore**: CI skips `.github/workflows/**` and `**/*.md` changes

<br/>

## License

See [LICENSE](LICENSE) — replace with your chosen license.
