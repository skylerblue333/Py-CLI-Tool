# Sky Artifact CLI

**Status: engineering beta.** A local-only Python CLI for bounded artifact inspection without network access or arbitrary code execution.

## Commands

- `health` — verifies the CLI entrypoint
- `version` — prints the current engineering-beta version
- `sha256 PATH` — streams a bounded local file and emits its SHA-256 digest
- `json-check PATH` — validates UTF-8 JSON and emits a small structural summary
- `text-stats PATH` — emits byte, character, line, and word counts for UTF-8 text

All output is compact JSON so the CLI can be consumed by scripts and CI pipelines.

## Safety boundary

Files must exist and be regular files. Inspection is capped at 64 MiB. The CLI does not make network calls, run shell commands, import plugins, deserialize executable formats, follow a remote URL, or modify inspected files.

## Run

```bash
python -m pip install -r requirements-dev.txt
pytest -q
python cli.py sha256 README.md
python cli.py json-check package.json
python cli.py text-stats README.md
```

Container:

```bash
docker build -t sky-artifact-cli .
docker run --rm sky-artifact-cli health
```

The runtime image executes as a non-root UID.

## SKYCOIN4444 integration

Use this as a small developer/CI utility for verifying local build artifacts, manifests, configuration JSON, documentation, or generated files. It should complement—not replace—format-specific validators, cryptographic signing, malware scanning, SBOM tooling, or provenance systems.

## Limitations

This repository is not a system-administration shell, malware scanner, secret scanner, package verifier, code-signing system, or remote artifact service. SHA-256 output proves only the bytes hashed by the caller; authenticity requires a separately trusted signature or provenance system.

See `SECURITY.md` and `CHANGELOG.md` for product boundaries.
