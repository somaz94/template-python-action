import os

import main
import pytest
from main import ActionRunner

DEFAULT_RESULT = "Hello from YOUR_ACTION!"


@pytest.fixture(autouse=True)
def clean_inputs(monkeypatch):
    for key in (
        "INPUT_INPUT_FILE",
        "INPUT_OUTPUT_FILE",
        "INPUT_DRY_RUN",
        "GITHUB_OUTPUT",
    ):
        monkeypatch.delenv(key, raising=False)


def read(path):
    with open(path) as f:
        return f.read()


class TestPrintConfiguration:
    def test_defaults(self, make_config, capsys):
        ActionRunner(make_config()).print_configuration()

        out = capsys.readouterr().out
        assert "Input File: (none)" in out
        assert "Output File: output.txt" in out
        assert "Dry Run: False" in out


class TestExecute:
    def test_writes_output_file(
        self, make_config, tmp_output_file, github_output_file, monkeypatch
    ):
        monkeypatch.setenv("GITHUB_OUTPUT", github_output_file)

        ActionRunner(make_config(output_file=tmp_output_file)).execute()

        assert read(tmp_output_file) == DEFAULT_RESULT
        outputs = read(github_output_file)
        assert f"output_file={tmp_output_file}\n" in outputs
        assert f"result={DEFAULT_RESULT}\n" in outputs

    def test_dry_run_skips_the_file(
        self, make_config, tmp_output_file, github_output_file, monkeypatch, capsys
    ):
        monkeypatch.setenv("GITHUB_OUTPUT", github_output_file)

        ActionRunner(make_config(output_file=tmp_output_file, dry_run=True)).execute()

        assert not os.path.exists(tmp_output_file)
        assert f"[DRY RUN] Result: {DEFAULT_RESULT}" in capsys.readouterr().out
        outputs = read(github_output_file)
        assert "output_file=" not in outputs
        assert f"result={DEFAULT_RESULT}\n" in outputs


class TestMain:
    def test_success(self, tmp_input_file, tmp_output_file, monkeypatch):
        monkeypatch.setenv("INPUT_INPUT_FILE", tmp_input_file)
        monkeypatch.setenv("INPUT_OUTPUT_FILE", tmp_output_file)

        main.main()

        assert read(tmp_output_file) == "Hello World"

    def test_invalid_config_exits_1(self, monkeypatch, capsys):
        monkeypatch.setenv("INPUT_OUTPUT_FILE", "")

        with pytest.raises(SystemExit) as exc:
            main.main()

        assert exc.value.code == 1
        assert "::error::output_file is required" in capsys.readouterr().out

    def test_unexpected_error_exits_1(self, monkeypatch, capsys):
        def boom(config):
            raise RuntimeError("boom")

        monkeypatch.setattr(main, "run", boom)

        with pytest.raises(SystemExit) as exc:
            main.main()

        assert exc.value.code == 1
        assert "::error::Unexpected error: boom" in capsys.readouterr().out
