# Project-manager handoff: T-0002

- Task: [T-0002](../README.md)
- Role: project-manager
- Timestamp (UTC): 2026-10-18T07:50:48Z
- Recipient: worker
- Event: dispatch
- Outcome: Add the approved cross-harness Google Drive workspace backup skill.

## Context passed

- Approved feature plan: [IP-0001](../../../README.md)
- Approved task README: [T-0002](../README.md)
- Approved baseline commit: cc7aea2
- Task 1 was independently reviewed and committed in f985766.
- User expects the skill to work in Codex, Claude, OpenCode, and similar harnesses when their Google Drive connector is enabled and appropriately authorized.
- The skill must check required connector capabilities, authentication, and destination or parent-folder read access before creating a local archive. If checks fail, stop and suggest the specific connection or permission needed.
- Keep Drive operations connector-only; do not use Google API/CLI fallback. Do not create probe files. An actual upload denial should produce a clear write-access suggestion.
- Follow the approved ZIP, manifest, verification, restore safety, retention, folder organization, and no-encryption decisions.
- Do not perform a real user backup or create/upload Drive content during this implementation task.

## Acceptance criteria

- Meet all T-0002 acceptance criteria.
- Keep the core skill harness-neutral and document its connector capability requirements and limitations.
- Add only supporting code/tests needed to make archive creation, validation, and safe restore reliable.

## Next action

Implement this task and write an append-only worker handoff in this task's handoffs directory. Do not change task status or commit.
