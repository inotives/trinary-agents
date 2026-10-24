# Report renderer reference

`scripts/render_report.py` validates a rapid feature's `report.md` and renders
it, together with the plan, as a read-only `report.html`. The workflow in
[`SKILL.md`](../SKILL.md) works without it: when Python 3 is unavailable,
`report.md` is the deliverable. This file describes what the renderer checks
and produces; agents running the workflow only need step 8 of `SKILL.md`.

```text
python3 <skill-dir>/scripts/render_report.py trinary-workspace/rapid/RF-XXXX--<slug>
```

## Requirements

Rendering requires Python 3 and uses only the standard library; no packages
need to be installed. Check availability with `python3 --version`.

The DaisyUI 5.7.50 stylesheet in `assets/report/` is embedded into each
rendered page with its license notice. The page has no scripts, links, images,
or other resource references and makes no network requests. The only
`http://` strings in the page are the standard SVG/XLink XML namespace
identifiers inside the stylesheet's inline `data:` images.

## Inputs

- `report.md` in the given folder, written from
  [`report-template.md`](report-template.md).
- `README.md` in the same folder: the plan, written from
  [`plan-template.md`](plan-template.md). Its `## Goal`, `## Scope`, and
  `## Decisions` sections are embedded in the page.
- Project display name: `Project name: <name>` in the README of the nearest
  enclosing `trinary-workspace/` directory. A missing README, missing line, or
  placeholder value (`<name>`, `Project`, `TBD`, `unknown`, `TODO`) is an
  error; ask the human for the name.

## Validation

The renderer collects every problem, prints each one by name, exits with
status 1, and writes nothing. Fix `report.md` (or the plan or workspace
README) and rerun. Usage errors exit with status 2.

Report frontmatter:

- All eight keys are present: `id`, `title`, `status`, `branch`,
  `plan_approved_at`, `reported_at`, `review`, `reviewer`. Only `reviewer` may
  be empty or `null`; keys may not repeat. Extra keys are ignored.
- `id` matches `RF-XXXX` and equals the plan's `id`.
- `status` is `Reported`.
- `review` is `independent`, `self-verified`, or `skipped`.
- `reviewer` names the reviewer when `review: independent`, and is `null`
  when `review` is `self-verified` or `skipped`. In those two cases the
  `## Review` section must contain `Not independently reviewed.`

Report sections:

- Exactly these `##` headings, each once, in this order: Outcome, Acceptance
  checks, Changes, Findings, Review, Pending issues, Steps completed. Any
  other `##` heading is rejected; `###` and deeper headings inside a section
  are allowed. No section may be empty (write `None`).
- The first non-empty line under `## Outcome` is exactly `RESULT: DELIVERED`,
  `RESULT: PARTIAL`, or `RESULT: NOT_DELIVERED`.
- `## Acceptance checks` contains one table with the header
  `| Check | Command / method | Result | Evidence |`, at least one row, four
  cells per row, and Result `passed`, `failed`, or `not run`.
- The result agrees with the checks: `DELIVERED` requires every check
  `passed`; when no check passed the result must be `NOT_DELIVERED`.
- `## Pending issues` contains one table with the header
  `| Issue | Severity | Backlog |` and at least one row. Severity is `high`,
  `medium`, or `low`; Backlog is a `BL-XXXX` ID or `-`. With no pending
  issues the table has the single row `| None | - | - |`.

Plan: frontmatter `id` and `title`, and the `## Goal`, `## Scope`, and
`## Decisions` sections, are required.

An existing `report.html` without the renderer's marker comment, or a
symlinked `report.html`, is never overwritten. The page is written to a
temporary file in the folder and then moved into place.

The rules that follow the committed template but await human confirmation —
report status `Reported`, the `| None | - | - |` row, and severities
`high`/`medium`/`low` — are module constants (`REPORT_STATUSES`,
`NO_ISSUES_ROW`, `ISSUE_SEVERITIES`) at the top of the script.

## Layout

- Title `Trinary-RAPID Report :: <Project Name> :: RF-XXXX <title>`.
- Header card with the feature ID and title, a large colored `RESULT:` badge
  (green `DELIVERED`, amber `PARTIAL`, red `NOT_DELIVERED`), `Not
  independently reviewed.` when review was not independent, and the branch,
  plan approval time, report time, review, reviewer, and status.
- A collapsed `Plan:` section holding the plan's Goal, Scope, and Decisions.
- One card per report section, in template order. Acceptance check results
  and pending issue severities are shown as badges.
- The DaisyUI license notice as an HTML comment at the end of the page.

## Markdown subset

All Markdown-sourced text, including frontmatter values, is HTML-escaped.
The renderer understands only:

- Headings (`###` and deeper inside a section).
- Paragraphs; consecutive lines join into one paragraph.
- Bullet (`-`, `*`, `+`) and numbered (`1.`) lists. Indented items are shown
  indented; unindented continuation lines join the previous item.
- Task-list items `- [ ]` and `- [x]`, shown as disabled checkboxes.
- Pipe tables with a `| --- |` separator row; `\|` escapes a pipe in a cell.
- Inline code in backticks.
- Fenced code blocks (```` ``` ```` or `~~~`), shown preformatted.
- Links `[text](target)` are shown as text followed by the target in
  parentheses; they are not clickable.

Everything else, such as emphasis, images, and raw HTML, appears as escaped
literal text. Content before the first `##` heading (the `#` title and the
plan link) is not rendered.
