# Changelog

All notable changes to the `trinary-rapid` skill. Versions follow
[Semantic Versioning](https://semver.org/); each release's section is used as
its GitHub Release notes.

## 1.0.0

### Added

- Initial release of `trinary-rapid`, a lightweight companion to
  `trinary-agents` for small features: branch, an interview capped at two
  rounds, one plan approval, implementation by the main agent with optional
  subagents, one independent review, and a templated report.
- Records live in `trinary-workspace/rapid/RF-XXXX--<slug>/` as `README.md`
  (the plan), `report.md`, and `report.html`, with plan statuses `Draft`,
  `Approved`, `Implementing`, and `Reported`.
- Fixed plan and report templates, also shipped as
  `references/plan-template.md` and `references/report-template.md`. The
  report opens with a `RESULT:` line and records acceptance check results,
  changes, findings, review, pending issues, and completed steps.
- An escalation rule that recommends a full trinary-agents feature plan for
  multi-module work, more than about five steps, or questions still open
  after the second interview round.
- A resume rule for `Implementing` rapid features based on the step checklist
  and `git status`/`git diff`.
- Shared backlog integration: out-of-scope pending issues become `BL-XXXX`
  items, and a rapid feature may start from a backlog item.
- Self-verified or skipped reviews are reported as "Not independently
  reviewed."
