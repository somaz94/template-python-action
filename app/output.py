import os


def set_output(name: str, value: str) -> None:
    """Write a key-value pair to GITHUB_OUTPUT for use in subsequent steps.

    Handles both single-line and multiline values using heredoc syntax.
    """
    github_output = os.getenv("GITHUB_OUTPUT")
    if not github_output:
        return

    with open(github_output, "a") as f:
        if "\n" in value:
            f.write(f"{name}<<EOF\n{value}\nEOF\n")
        else:
            f.write(f"{name}={value}\n")


def log_info(message: str) -> None:
    """Print an info message."""
    print(message)


def log_warning(message: str) -> None:
    """Print a warning in GitHub Actions format."""
    print(f"::warning::{message}")


def log_error(message: str) -> None:
    """Print an error in GitHub Actions format."""
    print(f"::error::{message}")
