---
id: T-0002
feature: IP-0002
title: Remove dashboard CDN runtime dependencies
status: done
depends_on:
  - T-0001
---

# T-0002: Remove dashboard CDN runtime dependencies

Feature plan: [IP-0002](../../README.md)

## Scope

Replace D3 rendering and calculations with browser-native DOM/SVG code, preserving the current dependency map, accessible text equivalent, cycle-time visualization and keyboard details, task lanes, handoff list, and detail drawer behavior. Replace the Flaticon image with inline SVG. Remove the unused Tailwind Browser script. Store a pinned DaisyUI stylesheet with the skill and embed it in generated HTML so the dashboard remains self-contained and makes no third-party runtime requests. Update focused tests and dashboard documentation.

## Out of scope

- The script-safe JSON change owned by T-0001.
- A Node.js rewrite or new build system/runtime dependency.
- Unrelated dashboard layout or workflow changes.

## Dependencies

- [T-0001](../T-0001--script-safe-dashboard-json/README.md) — make embedded dashboard JSON script-safe before changing the rendering template.

## Acceptance criteria

- [ ] Dashboard rendering uses browser-native DOM and SVG APIs and does not import or call D3.
- [ ] The refresh icon is inline SVG; no Flaticon image is loaded.
- [ ] The Tailwind Browser script is removed.
- [ ] DaisyUI styling is supplied locally and embedded in generated HTML; generated pages make no third-party runtime requests.
- [ ] Existing dashboard content, responsive layout, accessibility, cycle-time interactions, detail drawer, and auto-refresh behavior are preserved.
- [ ] Focused generator tests pass, including checks for the absence of remote runtime assets.
- [ ] Skill and project documentation describe the local asset behavior accurately.
- [ ] `git diff --check` passes.

## Implementation notes

- Generator: `skills/trinary-agents/scripts/generate_dashboard.py`.
- Focused tests: `skills/trinary-agents/tests/test_generate_dashboard.py`.
- Skill documentation: `skills/trinary-agents/SKILL.md`.
- Project documentation: `README.md`.
- Python already computes dependency layout. D3 is used for selections/data joins, DOM/SVG rendering, and cycle-time scale/sum operations.
- The generated page is written as one feature-local `dashboard.html`; load the local DaisyUI asset during generation and inline it rather than creating a runtime URL back to the installed skill.

## Handoffs

Append project-manager, worker, reviewer, and human-response records in [`handoffs/`](handoffs/). Do not overwrite earlier handoffs.
