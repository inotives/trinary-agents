---
id: T-0001
feature: IP-0001
title: Generate dashboards for single-task features
status: ready
depends_on: []
---

# T-0001: Generate dashboards for single-task features

Feature plan: [IP-0001](../../README.md)

## Scope

Make dashboard generation the default for every feature with at least one valid task README, including a single-task feature.

## Out of scope

- Dashboard redesign unrelated to the one-task behavior.
- Changing the no-task behavior or allowing overwrite of an unmarked dashboard.

## Dependencies

None.

## Acceptance criteria

- The dashboard generator produces dashboard.html for exactly one valid task.
- A feature with no valid task retains the current omission behavior.
- Existing safeguards against overwriting an unmarked dashboard remain.
- The Trinary Agents workflow instructions require a dashboard for one-task features and regeneration after relevant task or handoff updates.
- The focused dashboard tests pass.

## Implementation notes

- Relevant files: skills/trinary-agents/scripts/generate_dashboard.py, skills/trinary-agents/tests/test_generate_dashboard.py, and skills/trinary-agents/SKILL.md.
- Replace the existing single-task omission test with a generation assertion, while retaining the empty-feature and overwrite-protection coverage.

## Handoffs

Append project-manager, worker, reviewer, and human-response records in the handoffs directory. Do not overwrite earlier handoffs.
