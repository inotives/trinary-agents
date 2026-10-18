---
id: IP-0002
title: Dashboard Security and Offline Assets
status: Awaiting Human Acceptance
branch: fix/dashboard-security-audit
created_at: 2026-10-18T13:26:35Z
---

# Dashboard Security and Offline Assets

## Goal

Address the two medium-severity findings from the skills.sh audit of
`skills/trinary-agents/scripts/generate_dashboard.py`:

1. Prevent task-derived JSON from escaping the generated executable script.
2. Remove runtime requests to third-party CDNs from generated dashboards.

Generated dashboards remain standalone, read-only workflow snapshots that work
when opened offline.

## Context and repository findings

- `render_html` already escapes task and handoff JSON for safe placement inside
  an HTML script element, but inserts `dependency_layout` without that escaping.
- The generated page loads DaisyUI, Tailwind's browser runtime, D3, and a refresh
  icon from third-party URLs.
- Dashboard generation currently requires only Python 3's standard library.
- The existing test suite checks embedded task data and dashboard behavior in
  `skills/trinary-agents/tests/test_generate_dashboard.py`.
- The skill documentation says the workflow does not require network access,
  while describing online dashboard CDNs; generated dashboards should meet the
  same offline expectation as the workflow.

## Scope

- Apply safe script-element JSON encoding consistently to every JSON value
  embedded in the generated page, including `dependency_layout`.
- Keep the dashboard's current visual design and behavior while removing
  runtime network requests. Store pinned local copies of required third-party
  runtime assets beside the skill and embed them into each generated HTML page.
- Record each vendored asset's exact upstream version, source, and license in
  the asset folder. Replace the remote refresh icon with an inline SVG so no
  unverified icon URL remains.
- Add focused regression checks for script injection and for generated pages
  containing no external runtime asset URLs.
- Update the skill documentation to describe the offline, self-contained
  dashboard and its vendored assets.

## Non-goals

- Broader security review of the skill or the generated task content.
- Changing the dashboard's layout, features, or task semantics.
- Adding an asset update command, package manager, or Python dependency.
- Removing the dashboard's existing visualizations or replacing the UI with a
  new design.

## Decisions

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-10-18 | Keep generated dashboards self-contained and offline-capable. | The user approved removing runtime CDN access and asked to keep downloaded assets in the project's asset folder. |
| 2026-10-18 | Vendor pinned runtime assets with source and license records, then embed them in generated HTML. | This keeps the existing dashboard behavior while removing URL-based runtime dependencies. |
| 2026-10-18 | Escape the dependency layout JSON in the same way as task and handoff JSON. | This closes the unescaped script-element insertion identified by the audit. |

## Proposed implementation

Keep the fix within the dashboard generator, its adjacent assets, its focused
tests, and the skill instructions. Vendor only the runtime libraries needed by
the current page, using official package sources and licenses. The generated
page must not load assets from a remote URL or depend on a separately installed
package. The asset record must make future version and license review possible.

For all serialized values embedded into the HTML script, encode characters that
could terminate or alter script parsing. Retain safe text rendering for task
and handoff details.

## Acceptance checks

- [x] A task-derived `</script>` sequence in JSON data is emitted in escaped
  form and cannot create a new script element.
- [x] `dependency_layout`, task data, and handoff data remain parseable JSON in
  the generated dashboard.
- [x] Generated dashboards contain no external runtime stylesheet, script,
  image, or import URL and work without network access.
- [x] Existing dashboard content, task interactions, dependency graph,
  cycle-time display, handoff details, refresh controls, and responsive layout
  remain available.
- [x] Vendored assets have pinned versions and source/license records.
- [x] Focused dashboard tests pass, and the skill instructions match the
  generated-page behavior.

## Human decisions and open questions

- The user chose a self-contained dashboard and requested that downloaded
  assets be stored in the project's asset folder.
- On 2026-10-18, the user explicitly approved this feature plan.
- No unresolved human decisions.

## Task breakdown

1. [T-0001: Escape dashboard embedded JSON](tasks/T-0001--escape-dashboard-embedded-json/README.md) — no dependencies.
2. [T-0002: Vendor and embed dashboard assets](tasks/T-0002--vendor-and-embed-dashboard-assets/README.md) — depends on T-0001.

The JSON escaping fix is isolated first. Asset embedding and the generated-page
network check follow it because both tasks update the generator and dashboard
tests.

Task breakdown approved by the user on 2026-10-18. T-0001 is ready and T-0002
remains queued until T-0001 is done.

## Final human acceptance

- Evidence: T-0001 and T-0002 passed independent review. Regenerated the
  dashboard with the repository-local generator. The focused command
  `python3 -B -m unittest discover -s skills/trinary-agents/tests -p test_generate_dashboard.py`
  passed all 28 tests. Structural scan of the generated `dashboard.html`
  found zero CDN URLs, remote resource tags, remote CSS imports, or remote
  module imports. `git diff --cached --check` passed before the T-0002 commit
  (`1ff9ef4`). The browser policy prevented local-file visual inspection.
- Decision: Awaiting explicit human acceptance.
- Decision: Pending explicit human acceptance.
