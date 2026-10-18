# Project guidance

## About this project

`trinary-agents` is a focused collection of skills for coordinating agent teams
through human-approved feature plans, dependency-aware tasks, implementation,
independent review, and durable Markdown handoffs. The core workflow is designed
to work across agent harnesses such as Codex, Claude, Pi, and OpenCode. Keep its
instructions independent of any one vendor, CLI, or runtime.

The first skill is [`skills/trinary-agents/SKILL.md`](skills/trinary-agents/SKILL.md).
Its optional dashboard generator and tests are in
`skills/trinary-agents/scripts/` and `skills/trinary-agents/tests/`. The README
describes the project layout and principles.

## Working in this repository

- Read the relevant skill and supporting files before changing them.
- Keep each skill self-contained, easy to copy, and clear about its trigger,
  workflow, requirements, and limitations.
- Prefer ordinary Markdown and existing platform capabilities. Do not add a
  harness-specific dependency to the core workflow; document optional adapters
  separately.
- Preserve the project-manager, worker, and independent-review boundaries in
  workflow changes. Do not claim independent review when the same agent did the
  implementation.
- Update affected documentation and focused checks when behavior changes. Run
  only checks relevant to the change, and report exactly what ran.
- Keep changes scoped to the request. Do not commit, push, or publish unless
  explicitly asked.
