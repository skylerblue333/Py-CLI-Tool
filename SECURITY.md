# Security Policy

Sky Artifact CLI is a local engineering-beta inspection utility.

It reads only caller-supplied local regular files, caps inspected files at 64 MiB, performs no network access, does not execute shell commands, and does not load dynamic plugins or executable document formats. Inspected files are not modified.

The tool is not a malware scanner, secret detector, authenticity verifier, sandbox, or trust engine. A SHA-256 digest identifies bytes but does not establish who produced them. Use trusted signatures, provenance, SBOM, and format-specific validation where those controls are required.

Report vulnerabilities privately through GitHub security reporting when available. Do not publish private artifacts, credentials, or working exploit details in public issues.
