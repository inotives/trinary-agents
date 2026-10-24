# Project guidance

## About this project

`trinary-agents` is a focused collection of skills for coordinating agent teams
through human-approved feature plans, dependency-aware tasks, implementation,
independent review, and durable Markdown handoffs. The core workflow is designed
to work across agent harnesses such as Codex, Claude, Pi, and OpenCode. Keep its
instructions independent of any one vendor, CLI, or runtime.

The skills are:

- [`skills/trinary-agents/SKILL.md`](skills/trinary-agents/SKILL.md): the core
  project-manager, worker, and reviewer workflow. Its optional dashboard
  generator and tests are in `skills/trinary-agents/scripts/` and
  `skills/trinary-agents/tests/`.
- [`skills/trinary-rapid/SKILL.md`](skills/trinary-rapid/SKILL.md): a
  lightweight companion for small features with one plan approval, one
  review, a templated report, and human acceptance. Its report renderer and
  tests are in `skills/trinary-rapid/scripts/` and
  `skills/trinary-rapid/tests/`; the report theme and pinned stylesheet are in
  `skills/trinary-rapid/assets/report/`.
- [`skills/trinary-workspace-backup/SKILL.md`](skills/trinary-workspace-backup/SKILL.md):
  backs up and restores `trinary-workspace/` through a connected Google Drive
  integration.

The README describes the project layout and principles, and
[`docs/skill-releases.md`](docs/skill-releases.md) the release process.

## Working in this repository

- Read the relevant skill and supporting files before changing them.
- When changing a skill, increment its `VERSION` using SemVer. Pull requests
  that change skill files must include that bump; GitHub enforces this with
  the `validate-version-bumps` status check. Describe user-facing changes
  under a matching `## <version>` heading in the skill's `CHANGELOG.md`; that
  section becomes the release notes.
- Keep each skill self-contained, easy to copy, and clear about its trigger,
  workflow, requirements, and limitations.
- When adding a skill, also add it to the publish matrix and `test-skills`
  job in `.github/workflows/publish-skills.yml`, the `SKILLS` tuple in
  `.github/scripts/validate_skill_versions.py`, `docs/skill-releases.md`, and
  the README skills table and install examples.
- Run a skill's tests with
  `python3 -m unittest discover -s skills/<skill>/tests`.
- Keep `trinary-rapid` statuses and conventions aligned with
  `trinary-agents`; change both deliberately when one changes.
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
