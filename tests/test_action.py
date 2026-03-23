from action import run, process_file
from config import AppConfig


class TestRun:
    def test_default_message(self, make_config):
        config = make_config()
        result = run(config)
        assert result == "Hello from YOUR_ACTION!"

    def test_with_input_file(self, make_config, tmp_input_file):
        config = make_config(input_file=tmp_input_file)
        result = run(config)
        assert result == "Hello World"


class TestProcessFile:
    def test_reads_file_content(self, tmp_input_file):
        result = process_file(tmp_input_file)
        assert result == "Hello World"
