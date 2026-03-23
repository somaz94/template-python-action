import os
import sys

from config import AppConfig
from action import run
from output import set_output, log_info, log_error


class ActionRunner:
    """Main runner for the GitHub Action."""

    def __init__(self, config: AppConfig):
        self.config = config

    def print_configuration(self) -> None:
        """Print action configuration."""
        print("=" * 50)
        print("  YOUR_ACTION")
        print("=" * 50)
        print(f"  • Input File: {self.config.input_file or '(none)'}")
        print(f"  • Output File: {self.config.output_file}")
        print(f"  • Dry Run: {self.config.dry_run}")
        print("-" * 50)

    def execute(self) -> None:
        """Run the action logic and handle outputs."""
        result = run(self.config)

        if self.config.dry_run:
            log_info(f"[DRY RUN] Result: {result}")
        else:
            output_path = self.config.output_file
            with open(output_path, "w") as f:
                f.write(result)
            log_info(f"Output written to {output_path}")
            set_output("output_file", output_path)

        set_output("result", result)


def main():
    """Entry point for the action."""
    try:
        config = AppConfig.from_env()
        config.validate()

        runner = ActionRunner(config)
        runner.print_configuration()
        runner.execute()

    except ValueError as e:
        log_error(str(e))
        sys.exit(1)
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
