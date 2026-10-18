---
id: T-0002
feature: IP-0001
title: Add cross-harness Google Drive backup skill
status: ready
depends_on: []
---

# T-0002: Add cross-harness Google Drive backup skill

Feature plan: [IP-0001](../../README.md)

## Scope

Add a standalone skill that backs up, verifies, and restores the project workflow directory using the active agent harness connected Google Drive tools.

## Out of scope

- S3, PostgreSQL, SQLite, DuckDB, or other destinations.
- Direct Drive API/CLI setup, continuous sync, scheduled backups, automatic deletion, or client-side encryption.

## Dependencies

None.

## Acceptance criteria

- The skill describes capability-based use of Google Drive connectors across Codex, Claude, OpenCode, and other compatible harnesses without depending on one harness tool names.
- Before making an archive, it checks for the required connector capabilities, authentication, and read access to the destination or its parent folder.
- If a check fails, it stops before creating the archive and suggests the specific connection, permission, or capability needed.
- It creates one timestamped ZIP snapshot with a manifest of relative paths, sizes, and SHA-256 checksums, uploads it to the dedicated Drive folder, fetches it back, and verifies it before reporting success.
- Restore validates archive integrity, checksums, and safe paths before extraction, and protects an existing workspace unless the user explicitly confirms replacement.
- It keeps prior snapshots and does not fall back to a CLI/API when the connector is unavailable.
- The repository README lists the new skill.

## Implementation notes

- Relevant new area: skills/trinary-workspace-backup/.
- Use the connected Drive tools exposed by the active harness. Do not assume Codex-specific tool names.
- The current Codex session exposes Drive profile, folder listing/search, upload, and fetch/download capabilities. Claude and OpenCode behavior must remain unverified unless checked in those harnesses.

## Handoffs

Append project-manager, worker, reviewer, and human-response records in the handoffs directory. Do not overwrite earlier handoffs.
