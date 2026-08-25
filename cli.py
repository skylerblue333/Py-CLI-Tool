from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import typer

app = typer.Typer(no_args_is_help=True, help="Inspect local artifacts without network access.")
MAX_FILE_BYTES = 64 * 1024 * 1024
CHUNK_BYTES = 1024 * 1024


def require_file(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise typer.BadParameter("path must reference an existing file")
    size = resolved.stat().st_size
    if size > MAX_FILE_BYTES:
        raise typer.BadParameter("file exceeds 64 MiB inspection limit")
    return resolved


def emit(payload: dict[str, Any]) -> None:
    typer.echo(json.dumps(payload, separators=(",", ":"), ensure_ascii=False))


@app.command()
def health() -> None:
    """Verify the CLI entrypoint."""
    emit({"status": "ok", "service": "sky-artifact-cli"})


@app.command()
def version() -> None:
    """Print the engineering-beta version."""
    emit({"name": "sky-artifact-cli", "version": "0.1.0"})


@app.command("sha256")
def sha256_command(path: Path) -> None:
    """Calculate a SHA-256 digest for a bounded local file."""
    target = require_file(path)
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        while chunk := handle.read(CHUNK_BYTES):
            digest.update(chunk)
    emit({"path": str(target), "bytes": target.stat().st_size, "sha256": digest.hexdigest()})


@app.command("json-check")
def json_check(path: Path) -> None:
    """Validate JSON and emit a small structural summary."""
    target = require_file(path)
    try:
        value = json.loads(target.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        raise typer.BadParameter("file is not valid UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"invalid JSON at line {exc.lineno} column {exc.colno}") from exc

    summary: dict[str, Any] = {
        "path": str(target),
        "valid": True,
        "type": type(value).__name__,
    }
    if isinstance(value, dict):
        summary["keys"] = sorted(str(key) for key in value.keys())[:100]
        summary["keyCount"] = len(value)
    elif isinstance(value, list):
        summary["items"] = len(value)
    emit(summary)


@app.command("text-stats")
def text_stats(path: Path) -> None:
    """Report bounded UTF-8 text line, word, character, and byte counts."""
    target = require_file(path)
    try:
        text = target.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise typer.BadParameter("file is not valid UTF-8 text") from exc
    emit(
        {
            "path": str(target),
            "bytes": target.stat().st_size,
            "characters": len(text),
            "lines": len(text.splitlines()),
            "words": len(text.split()),
        }
    )


if __name__ == "__main__":
    app()
