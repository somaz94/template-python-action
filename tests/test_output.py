import os

from output import set_output, log_warning, log_error


class TestSetOutput:
    def test_single_line(self, github_output_file, monkeypatch):
        monkeypatch.setenv("GITHUB_OUTPUT", github_output_file)

        set_output("result", "success")

        with open(github_output_file) as f:
            content = f.read()
        assert content == "result=success\n"

    def test_multiline(self, github_output_file, monkeypatch):
        monkeypatch.setenv("GITHUB_OUTPUT", github_output_file)

        set_output("data", "line1\nline2")

        with open(github_output_file) as f:
            content = f.read()
        assert "data<<EOF" in content
        assert "line1\nline2" in content
        assert content.endswith("EOF\n")

    def test_no_github_output(self, monkeypatch):
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        # Should not raise
        set_output("key", "value")


class TestLogging:
    def test_log_warning(self, capsys):
        log_warning("test warning")
        assert capsys.readouterr().out == "::warning::test warning\n"

    def test_log_error(self, capsys):
        log_error("test error")
        assert capsys.readouterr().out == "::error::test error\n"
