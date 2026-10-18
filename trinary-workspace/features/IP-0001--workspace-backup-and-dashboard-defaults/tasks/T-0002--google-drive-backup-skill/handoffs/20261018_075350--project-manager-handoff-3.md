# Project-manager handoff: T-0002

- Task: [T-0002](../README.md)
- Role: project-manager
- Timestamp (UTC): 2026-10-18T07:53:50Z
- Recipient: worker
- Event: review outcome
- Outcome: Independent reviewer requested one workflow-order correction.

## Context passed

- Reviewer handoff: [reviewer handoff 1](20261018_081000--reviewer-handoff-1.md)
- Reviewer verdict: CHANGES_REQUESTED.
- Current status: changes_requested.

## Required change

The Backup workflow currently creates the dedicated Drive folder before building the ZIP. Change the order so the active agent:
1. Performs the existing read-only connector/authentication/folder preflight.
2. Builds and verifies the local archive.
3. Creates the dedicated folder if it is missing, immediately before upload.
4. Uploads the archive and continues fetch-back verification.

Do not create the Drive folder before the archive is ready. This avoids an empty folder if archive creation fails and keeps archive upload as the write-access check.

## Next action

Worker makes only this requested correction, runs focused checks, and appends a new worker handoff.
