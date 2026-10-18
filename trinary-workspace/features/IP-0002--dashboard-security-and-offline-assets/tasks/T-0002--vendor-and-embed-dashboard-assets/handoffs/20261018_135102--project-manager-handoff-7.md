# Project-manager handoff: T-0002

- Task: [T-0002: Vendor and embed dashboard assets](../README.md)
- Role: project-manager
- Timestamp (UTC): 2026-10-18T13:51:02Z
- Recipient: worker
- Event: rework dispatch
- Outcome: Clarify that installations must keep the vendored asset folder with the skill to support dashboard regeneration.

## Context passed

- Update `skills/trinary-agents/SKILL.md` to state that the full skill bundle
  must be installed/copied, including `assets/dashboard/` alongside
  `scripts/`. A deployment containing only the instructions and generator will
  not have the files needed to generate a dashboard.
- This clarification is within the approved scope: asset files are stored
  beside the skill, and instructions describe how dashboard generation works.
- The project-manager has already regenerated the dashboard after task status
  changes using the repository-local generator.
- Rerun the focused suite and `git diff --check`, append a worker rework
  handoff, and do not change task status.

## Evidence

- Reviewer finding: [`20261018_135013--reviewer-handoff-2.md`](20261018_135013--reviewer-handoff-2.md)
- The current dashboard embeds assets and has zero remote runtime requests.

## Next action

Return the clarified documentation and verification evidence for independent
review.
