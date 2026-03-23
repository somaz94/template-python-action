import os
import sys

import pytest

# Add app directory to path so tests can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))


@pytest.fixture
def tmp_input_file(tmp_path):
    """Create a temporary input file with test content."""
    f = tmp_path / "input.txt"
    f.write_text("Hello World")
    return str(f)


@pytest.fixture
def tmp_output_file(tmp_path):
    """Return a temporary output file path."""
    return str(tmp_path / "output.txt")


@pytest.fixture
def github_output_file(tmp_path):
    """Create a temporary GITHUB_OUTPUT file and set the env var."""
    f = tmp_path / "github_output"
    f.write_text("")
    return str(f)


@pytest.fixture
def make_config():
    """Factory fixture to create AppConfig instances."""
    from config import AppConfig

    def _make(**kwargs):
        defaults = {
            "input_file": "",
            "output_file": "output.txt",
            "dry_run": False,
        }
        defaults.update(kwargs)
        return AppConfig(**defaults)

    return _make
