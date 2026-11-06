# Changelog

All notable changes to the `trinary-tweak` skill. Versions follow
[Semantic Versioning](https://semver.org/); each release's section is used as
its GitHub Release notes.

## 1.0.0

### Added

- Initial release of `trinary-tweak`, a companion to `trinary-agents` and
  `trinary-rapid` for interactive sessions of small changes, such as UI
  polish: the human asks, the agent changes, the human checks and gives
  feedback, repeat. No interview, plan approval, or per-change review.
- One record per session in `trinary-workspace/tweak/TW-XXXX--<slug>/README.md`,
  written once per kept, dropped, or carried-over change rather than per
  iteration, with the request, iterations tried, result, files, and checkpoint
  commit.
- Checkpoint commits per kept change by default, never on the default branch,
  so any approved state can be restored; the human can turn them off.
- Safe handling of the human's work: uncommitted files present at session
  start are recorded and excluded from checkpoints and the handoff, and a
  dropped change is undone hunk by hunk, with or without checkpoints.
- A scope guard that recommends trinary-rapid or trinary-agents for data
  model, API, backend, security, or multi-module work, or acceptance that
  needs designed tests, and settles the change in progress before switching.
- A wrap-up that runs the project's checks, separates session-caused failures
  from pre-existing ones, writes a handoff, optionally runs one independent
  review on request, and moves the session from `Active` to `Closed`. Sessions
  are recorded as `review: human-iterated` unless an independent reviewer ran.
  With checkpoints off, kept changes are committed together at wrap-up.
- Shares the trinary-workspace backlog, with its own copy of the item
  template; a session can start from a backlog item and promote it
  (`promoted_to: TW-XXXX`). Active sessions can be resumed from their record
  and the repository.
