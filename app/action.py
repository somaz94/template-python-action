from config import AppConfig


def run(config: AppConfig) -> str:
    """Execute the action logic and return the result.

    Replace this with your action's core functionality.
    """
    if config.input_file:
        return process_file(config.input_file)

    return "Hello from YOUR_ACTION!"


def process_file(file_path: str) -> str:
    """Process the input file and return the result.

    TODO: Replace with your actual file processing logic.
    """
    with open(file_path) as f:
        content = f.read()
    return content
