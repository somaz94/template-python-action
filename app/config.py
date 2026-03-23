import os
from dataclasses import dataclass, field


@dataclass
class AppConfig:
    """Configuration loaded from environment variables set by GitHub Actions."""

    input_file: str = ""
    output_file: str = "output.txt"
    dry_run: bool = False

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create configuration from INPUT_* environment variables."""
        return cls(
            input_file=os.getenv("INPUT_INPUT_FILE", ""),
            output_file=os.getenv("INPUT_OUTPUT_FILE", "output.txt"),
            dry_run=os.getenv("INPUT_DRY_RUN", "false").lower() == "true",
        )

    def validate(self) -> None:
        """Validate configuration values."""
        if not self.output_file:
            raise ValueError("output_file is required")
