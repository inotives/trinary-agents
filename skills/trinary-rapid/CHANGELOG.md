# Changelog

All notable changes to the `trinary-rapid` skill. Versions follow
[Semantic Versioning](https://semver.org/); each release's section is used as
its GitHub Release notes.

## 1.0.0

### Added

- Initial release of `trinary-rapid`, a lightweight companion to
  `trinary-agents` for small features: branch, an interview capped at two
  rounds, one plan approval, implementation by the main agent with optional
  subagents, one independent review, a templated report, and a final human
  acceptance.
- Records live in `trinary-workspace/rapid/RF-XXXX--<slug>/` as `README.md`
  (the plan), `report.md`, and `report.html`, with the trinary-agents feature
  plan statuses `Draft`, `Approved`, `Implementing`,
  `Awaiting Human Acceptance`, and `Accepted`. The report's `status` mirrors
  the plan's.
- Fixed plan and report templates, also shipped as
  `references/plan-template.md` and `references/report-template.md`. The
  report opens with a `RESULT:` line and records acceptance check results,
  changes, findings, review, pending issues, and completed steps.
- An escalation rule that recommends a full trinary-agents feature plan for
  multi-module work, more than about five steps, or questions still open
  after the second interview round.
- After the report, the plan's passed acceptance checks are ticked and the
  plan, report, rendered report, new backlog items, and workspace README
  changes are committed with the implementation.
- A final human acceptance step: only explicit human acceptance sets
  `Accepted`, re-renders the report, and records an acceptance commit;
  requested changes return the plan to `Implementing`. When
  `trinary-workspace/` is ignored by Git, nothing is committed for it and it
  is never force-added.
- Resume rules for every plan status; `Implementing` rapid features resume
  from the step checklist and `git status`/`git diff`.
- Pending issues carry a Type `<bug|idea>:<low|medium|high>`, such as
  `bug:high`, shown as a badge coloured by severity.
- Shared backlog integration: out-of-scope pending issues become `BL-XXXX`
  items, and a rapid feature may start from a backlog item.
- Self-verified or skipped reviews are reported as "Not independently
  reviewed."
- `scripts/render_report.py` (Python 3 standard library only) validates
  `report.md` against the template and renders `report.html` with the
  `RESULT:` badge, every report section, and the plan's goal, scope, and
  decisions. It names every missing or invalid item and writes nothing when
  validation fails, and never overwrites a `report.html` it did not generate.
- The rendered page embeds the pinned DaisyUI 5.7.50 stylesheet and its MIT
  license notice from `assets/report/` and makes no network requests.
- The report uses the trinary-agents dashboard palette from
  `assets/report/report-theme.css`, with dark and light themes and a header
  toggle button that remembers the viewer's choice.
- `references/report.md` documents the renderer's checks, layout, and
  Markdown subset; `tests/test_render_report.py` covers it.
