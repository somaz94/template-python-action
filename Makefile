.PHONY: test coverage clean help

VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

venv: $(VENV)/bin/activate ## Create virtualenv and install dev dependencies

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install pytest pytest-cov
	touch $(VENV)/bin/activate
	@echo ""
	@echo "Virtualenv created. To activate:"
	@echo "  source $(VENV)/bin/activate"

test: $(VENV)/bin/activate ## Run unit tests with coverage
	$(PYTEST) tests/ -v --cov=app --cov-report=term-missing

coverage: $(VENV)/bin/activate ## Generate HTML coverage report
	$(PYTEST) tests/ --cov=app --cov-report=term-missing --cov-report=html
	@echo "Open htmlcov/index.html in your browser"

check-gh: ## Verify gh CLI is installed and authenticated
	@command -v gh >/dev/null 2>&1 || { echo "gh CLI not found. Install: https://cli.github.com/"; exit 1; }
	@gh auth status >/dev/null 2>&1 || { echo "gh CLI not authenticated. Run: gh auth login"; exit 1; }

branch: check-gh ## Create a feature branch (usage: make branch name=feature-name)
	@test -n "$(name)" || { echo "Usage: make branch name=feature-name"; exit 1; }
	git switch main
	git pull origin main
	git switch -c feat/$(name)

pr: check-gh test ## Run tests, push, and create PR (usage: make pr title="feat: ...")
	@test -n "$(title)" || { echo 'Usage: make pr title="feat: add feature"'; exit 1; }
	git push -u origin $$(git branch --show-current)
	./scripts/create-pr.sh "$(title)"

clean: ## Remove venv, cache, and build artifacts
	rm -rf $(VENV) .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
