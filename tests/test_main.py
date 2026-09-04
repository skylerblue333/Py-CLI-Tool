import hashlib
import json

from typer.testing import CliRunner

import cli
from cli import app

runner = CliRunner()


def test_health_and_version() -> None:
    health = runner.invoke(app, ["health"])
    assert health.exit_code == 0
    assert json.loads(health.stdout)["status"] == "ok"

    version = runner.invoke(app, ["version"])
    assert version.exit_code == 0
    assert json.loads(version.stdout)["version"] == "0.1.0"


def test_sha256(tmp_path) -> None:
    target = tmp_path / "artifact.txt"
    target.write_bytes(b"skycoin4444\n")
    result = runner.invoke(app, ["sha256", str(target)])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["sha256"] == hashlib.sha256(b"skycoin4444\n").hexdigest()
    assert payload["bytes"] == 12


def test_json_check_and_invalid_json(tmp_path) -> None:
    target = tmp_path / "manifest.json"
    target.write_text('{"b":2,"a":1}', encoding="utf-8")
    result = runner.invoke(app, ["json-check", str(target)])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["keys"] == ["a", "b"]

    broken = tmp_path / "broken.json"
    broken.write_text("{", encoding="utf-8")
    failure = runner.invoke(app, ["json-check", str(broken)])
    assert failure.exit_code != 0
    assert "invalid JSON" in failure.output


def test_json_check_rejects_nonstandard_constants(tmp_path) -> None:
    for token in ("NaN", "Infinity", "-Infinity"):
        target = tmp_path / f"bad-{token.replace('-', 'minus')}.json"
        target.write_text(f'{{"value":{token}}}', encoding="utf-8")
        result = runner.invoke(app, ["json-check", str(target)])
        assert result.exit_code != 0
        assert "invalid JSON" in result.output


def test_text_stats(tmp_path) -> None:
    target = tmp_path / "notes.txt"
    target.write_text("one two\nthree\n", encoding="utf-8")
    result = runner.invoke(app, ["text-stats", str(target)])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["lines"] == 2
    assert payload["words"] == 3
    assert payload["characters"] == 14


def test_read_limit_is_enforced_from_open_handle(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(cli, "MAX_FILE_BYTES", 8)
    target = tmp_path / "growing.txt"
    target.write_bytes(b"123456789")
    for command in ("sha256", "text-stats"):
        result = runner.invoke(app, [command, str(target)])
        assert result.exit_code != 0
        assert "64 MiB inspection limit" in result.output


def test_missing_file_rejected(tmp_path) -> None:
    result = runner.invoke(app, ["sha256", str(tmp_path / "missing")])
    assert result.exit_code != 0
    assert "existing file" in result.output
