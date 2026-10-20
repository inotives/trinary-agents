---
id: IP-0002
title: Dashboard Security and Local Assets
status: Accepted
branch: fix/dashboard-security-findings
created_at: 2026-10-20T06:16:04Z
---

# Dashboard Security and Local Assets

- Project: Trinary Agents
- Date: 2026-10-20

## Goal and success criteria

Address the security findings reported for the published Trinary Agents skill and keep generated dashboards usable without fetching third-party runtime assets. Preserve the dashboard's current information, layout, accessibility, and interactions.

Success means embedded task and handoff data cannot terminate the inline script; the dashboard generator has no runtime dependency on D3, Flaticon, Tailwind Browser, or a remote DaisyUI stylesheet; and the dashboard keeps its existing behavior with local styles and browser-native DOM/SVG code.

## Context

The skills.sh listing reports a low-severity Socket anomaly in `scripts/generate_dashboard.py`: task IDs in the dependency layout are inserted into executable JavaScript without HTML-safe JSON encoding. It also reports a medium Snyk W012 finding for external runtime libraries and an icon loaded from CDNs.

The generator already escapes its task and handoff JSON payloads before embedding them in the inline script. It does not apply that encoding to `dependency_layout`, which includes task IDs as object keys. Existing tests cover a script-tag payload in a task title, but not in a task ID used by the dependency layout.

The browser-side dashboard uses D3 for element creation, data joins, attributes, and event handling, plus a linear scale and sum for the cycle-time bar. Python already computes the dependency graph layout. The dashboard uses custom CSS and DaisyUI component classes; source inspection found no Tailwind utility classes, so the Tailwind Browser runtime appears unnecessary. Flaticon supplies only the refresh icon.

## Scope

- Add one HTML-safe JSON serialization path and use it for every data structure embedded in the inline script, including `dependency_layout`.
- Add regression coverage for a malicious task ID such as `</script><script>alert(1)</script>` and assert that it remains inert in the generated page while the dashboard data remains valid.
- Replace D3 selection, join, scale, and sum usage with browser-native DOM and SVG code while preserving the dependency diagram, accessible text equivalent, cycle-time visualization and keyboard details, kanban cards, handoff list, and detail drawer behavior.
- Replace the remote Flaticon image with an inline SVG refresh icon and preserve its accessible decorative status, color, animation, and reduced-motion behavior.
- Remove the unused Tailwind Browser CDN script.
- Store a pinned DaisyUI stylesheet with the skill and include it from the local asset at generation time, without adding a network fetch to the generated dashboard. Keep the generated dashboard self-contained.
- Update focused tests and the skill/README instructions that describe dashboard runtime assets or dependencies.
- Confirm the generated dashboard has no remote runtime scripts, stylesheets, images, module imports, or CSS imports.

## Non-goals

- Rewriting the generator from Python to Node.js.
- Changing task parsing, workflow statuses, dashboard layout, task ordering, or cycle-time definitions.
- Redesigning the dashboard or changing the project-manager, worker, and reviewer boundaries.
- Removing informational links that are not fetched during dashboard use, unless they misrepresent the resulting local implementation.
- Adding new runtime packages, build systems, or network requirements.

## Decisions and rationale

| Decision | Outcome |
| --- | --- |
| Embedded script data | Apply HTML-safe JSON encoding to every embedded data payload; task IDs enter the dependency-layout JSON and must be covered. |
| D3 | Replace it with browser-native DOM and SVG APIs. The layout is already computed in Python, and the browser-side D3 operations are limited to rendering, a linear scale, and summation. |
| Flaticon | Replace the single remote refresh image with inline SVG. |
| DaisyUI | Keep the existing component styling but vendor a pinned stylesheet locally and inline it into the generated dashboard so it remains one self-contained file. |
| Tailwind Browser | Remove its CDN script; inspected markup has no Tailwind utility classes and the dashboard has extensive custom CSS. |
| Task breakdown | Use two sequential, independently reviewed tasks: JSON/script hardening first, then local dashboard rendering assets. |
| Generator language | Keep Python and its standard-library implementation. |

## Proposed design

### Safe embedded data

Use a shared helper for JSON inserted into HTML script elements. It must preserve valid JavaScript-readable JSON while escaping characters that can alter HTML parsing, at least `&`, `<`, and `>`. Route task data, handoff data, and dependency layout through the same helper. Continue rendering untrusted task and handoff strings as text through safe DOM APIs.

### Local dashboard rendering

Replace D3 with small native helpers for element creation, text, attributes, and event listeners. Use `document.createElement` for HTML, `document.createElementNS` for SVG, and `textContent` for user-controlled values. Compute cycle-bar positions and widths from cumulative durations and the total duration. Keep the existing Python dependency layout and the current accessible SVG/text representations.

Place a pinned DaisyUI stylesheet in the skill's own assets and load it from the generator's location at generation time, embedding its contents in the generated HTML. Do not link the generated dashboard to the source skill directory, since dashboards are copied into project feature folders. Replace the Flaticon image with inline SVG and remove the Tailwind Browser script. The finished dashboard should make no third-party runtime requests.

## Acceptance checks

- [x] A task ID containing `</script><script>alert(1)</script>` remains inert in the generated page; embedded JSON can still be read by the dashboard.
- [x] Task, handoff, and dependency data all use the same HTML-safe JSON encoding path.
- [x] Focused generator tests pass, including existing layout, completion, cycle-time, handoff, accessibility, responsive, drawer, and refresh checks.
- [x] Generated HTML has no remote runtime `script`, `link`, `img`, module import, or CSS import; locally supplied DaisyUI CSS is embedded in the page.
- [x] D3 and Tailwind Browser are not loaded as runtime dependencies, and the refresh control uses inline SVG.
- [x] Focused tests and independent source review confirm the dependency map, task lanes, handoff timeline, cycle-time visualization, detail drawer, keyboard behavior, refresh toggle, and responsive scrolling are preserved.
- [x] Dashboard and skill documentation accurately describe the local asset behavior and requirements.
- [x] `git diff --check` passes across the feature branch.

## Human decisions and open questions

Decisions recorded from the human:

- Keep the generator in Python; no Node.js rewrite for now.
- Remove D3 and Flaticon from runtime use.
- Keep DaisyUI styling but move its stylesheet to a local asset.
- Remove the Tailwind Browser script, which appears unused.
- Split the work into two sequential, separately reviewed tasks, with JSON hardening first.
- Plan approval: The human approved IP-0002 on 2026-10-20.
- Task breakdown approval: The human approved T-0001 followed by T-0002 on 2026-10-20.

Open questions: None at draft time.

## Relevant repository findings

- Generator: `skills/trinary-agents/scripts/generate_dashboard.py`.
- Focused tests: `skills/trinary-agents/tests/test_generate_dashboard.py`.
- Before implementation, runtime URLs included DaisyUI CSS and Tailwind Browser from jsDelivr, D3 as a jsDelivr ES module, and the Flaticon refresh image.
- Dashboard markup already includes custom styles for its layout and much of its component presentation.
- The generated dashboard is written as a single feature-local `dashboard.html`; local DaisyUI styling must therefore be included in that output.
- Workflow documentation in `skills/trinary-agents/SKILL.md` and the project `README.md` currently describe the CDN-loaded assets and Python requirement.
- The existing workspace identifies the project as `Trinary Agents`.
- The current branch is `fix/dashboard-security-findings`; the worktree was clean when planning began.

## Task breakdown

The approved plan was committed before task folders were created. The task breakdown was separately approved and recorded above.

| Task | Outcome | Dependencies |
| --- | --- | --- |
| [T-0001 — Make embedded dashboard JSON script-safe](tasks/T-0001--script-safe-dashboard-json/README.md) | Encode all inline-script JSON consistently and add task-ID injection regression coverage. | None |
| [T-0002 — Remove dashboard CDN runtime dependencies](tasks/T-0002--local-dashboard-runtime-assets/README.md) | Replace D3 and Flaticon, remove Tailwind Browser, vendor and inline DaisyUI CSS, update tests and documentation, and verify dashboard behavior. | T-0001 |

## Final human acceptance

- Implementation commits: `75f2033` (approved plan), `32e335a` (approved task baseline), `4563f16` (script-safe JSON), and `17f24ff` (local runtime assets and native renderer).
- Acceptance evidence: `python3 -B -m unittest discover -s skills/trinary-agents/tests -p 'test_generate_dashboard.py'` passed (29 tests); `git diff --check main...HEAD` passed. Static inspection of the generated dashboard found 0 remote script sources, stylesheet links, image sources, external module imports, remote CSS URLs, or CSS imports; executable inline code has no D3 calls or CDN/Tailwind/Flaticon references. The local stylesheet is DaisyUI 5.7.50 and retains its MIT notice.
- Independent review: T-0001 approved in [`20261020_062041--reviewer-handoff-1.md`](tasks/T-0001--script-safe-dashboard-json/handoffs/20261020_062041--reviewer-handoff-1.md); T-0002 approved in [`20261020_062942--reviewer-handoff-1.md`](tasks/T-0002--local-dashboard-runtime-assets/handoffs/20261020_062942--reviewer-handoff-1.md). Both reviewers report the focused suite and `git diff --check` passed.
- Remaining limitations: No browser-based visual QA was run because no browser executable was available. The generated dashboard is about 1.20 MB, including the 1.14 MB vendored DaisyUI stylesheet.
- Human decision: Plan approved and final feature acceptance granted on 2026-10-20.
