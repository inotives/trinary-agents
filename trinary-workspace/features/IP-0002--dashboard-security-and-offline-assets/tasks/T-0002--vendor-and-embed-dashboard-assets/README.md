---
id: T-0002
feature: IP-0002
title: Vendor and embed dashboard assets
status: queued
depends_on: [T-0001]
---

# T-0002: Vendor and embed dashboard assets

Feature plan: [IP-0002](../../README.md)

## Scope

Remove all runtime CDN requests from generated dashboards while preserving the
current UI and interactions. Store the required pinned runtime assets beside
the skill, embed them in generated `dashboard.html` files, and record each
asset's upstream source and license. Replace the remote refresh icon with an
inline SVG. Add regression coverage and update the skill documentation to
describe the self-contained dashboard.

## Out of scope

- Refreshing vendored assets after this task or adding an update tool.
- Redesigning dashboard layout or behavior.
- Adding Python or JavaScript package dependencies for dashboard generation.

## Dependencies

- [T-0001](../T-0001--escape-dashboard-embedded-json/README.md) — embedded
  dashboard JSON is script-safe before the asset work is integrated.

## Acceptance criteria

- [ ] Required runtime assets have pinned versions and source/license records
  in the skill's asset folder.
- [ ] Generated dashboards embed their styles and scripts and make no external
  runtime stylesheet, script, image, or module request.
- [ ] The generated dashboard opens and works without network access.
- [ ] Existing graph, cycle-time, task detail, handoff detail, refresh,
  responsive, and accessibility behavior remains available.
- [ ] Regression coverage checks for the absence of external runtime URLs and
  the presence of locally embedded assets.
- [ ] `skills/trinary-agents/SKILL.md` accurately documents the self-contained
  generated dashboard.

## Implementation notes

- Generator: `skills/trinary-agents/scripts/generate_dashboard.py`.
- Assets should live with the skill so copied installations remain complete.
- Dashboard tests: `skills/trinary-agents/tests/test_generate_dashboard.py`.
- Verify upstream asset provenance and redistribution terms before adding the
  files. Avoid retaining the remote Flaticon icon; draw its simple refresh mark
  as inline SVG.

## Handoffs

Append project-manager, worker, reviewer, and human-response records in
[`handoffs/`](handoffs/). Do not overwrite earlier handoffs.
