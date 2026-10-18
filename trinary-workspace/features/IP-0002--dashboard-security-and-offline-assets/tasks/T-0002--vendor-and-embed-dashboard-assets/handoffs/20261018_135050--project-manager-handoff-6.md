# Project-manager handoff: T-0002

- Task: [T-0002: Vendor and embed dashboard assets](../README.md)
- Role: project-manager
- Timestamp (UTC): 2026-10-18T13:50:50Z
- Recipient: worker
- Event: changes requested
- Outcome: Document that skill installations must include the vendored dashboard assets alongside the generator.

## Context passed

- Reviewer verdict: `CHANGES_REQUESTED` for a documentation gap. The generator
  resolves `assets/dashboard/` relative to its `scripts/` directory, but the
  skill instructions do not explicitly require deployments to preserve that
  folder.
- The generated dashboard now embeds the assets and has no external runtime
  requests; the prior stale artifact finding is resolved.
- Add a concise installation note in `skills/trinary-agents/SKILL.md`: when
  deploying/copying the skill, keep `assets/dashboard/` alongside `scripts/`;
  installing only `SKILL.md` and scripts is insufficient for regeneration.
- Do not change task status.

## Evidence

- Reviewer handoff: [`20261018_135013--reviewer-handoff-2.md`](20261018_135013--reviewer-handoff-2.md)
- Current generated HTML embeds assets. T-0002 implementation and 28 focused
  tests otherwise meet acceptance; visual browser inspection remains
  unavailable under the file-URL policy.

## Next action

Update the skill instructions, rerun the focused checks, and return the task
for independent review.
