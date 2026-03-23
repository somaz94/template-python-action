import pytest
from config import AppConfig


class TestAppConfig:
    def test_default_values(self):
        config = AppConfig()
        assert config.input_file == ""
        assert config.output_file == "output.txt"
        assert config.dry_run is False

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("INPUT_INPUT_FILE", "test.txt")
        monkeypatch.setenv("INPUT_OUTPUT_FILE", "result.txt")
        monkeypatch.setenv("INPUT_DRY_RUN", "true")

        config = AppConfig.from_env()

        assert config.input_file == "test.txt"
        assert config.output_file == "result.txt"
        assert config.dry_run is True

    def test_from_env_defaults(self, monkeypatch):
        for var in ["INPUT_INPUT_FILE", "INPUT_OUTPUT_FILE", "INPUT_DRY_RUN"]:
            monkeypatch.delenv(var, raising=False)

        config = AppConfig.from_env()
        assert config.input_file == ""
        assert config.output_file == "output.txt"
        assert config.dry_run is False

    def test_validate_missing_output_file(self):
        config = AppConfig(output_file="")
        with pytest.raises(ValueError, match="output_file is required"):
            config.validate()

    def test_validate_success(self):
        config = AppConfig()
        config.validate()  # Should not raise
