# Changelog

All notable changes to the `trinary-agents` skill. Versions follow
[Semantic Versioning](https://semver.org/); each release's section is used as
its GitHub Release notes.

## 1.1.1

### Added

- Backlog items have a `type` of `idea` or `bug`. Bug items record
  reproduction steps and expected versus actual behavior, and backlog reviews
  show each item's type.
- Promoted bugs use a narrower plan interview, may be a single-task IP, and
  must include an acceptance check that fails before the fix and passes after
  it. Bug-fix branches default to `fix/<slug>`.
- Guidance on when a bug is a backlog item versus a reviewer finding or a
  blocker.
- The dashboard generator warns when a task's `feature` does not match its
  feature README `id`.

### Changed

- The backlog item template's `Idea` section is now `Description`.
- Creating `backlog/` adds a mention of it to an existing workspace README
  that does not describe the backlog.

### Fixed

- `partial` worker outcomes are limited to two redispatches per task before
  the blocker process, so the loop cannot repeat indefinitely.

## 1.1.0

### Added

- **Backlog.** `trinary-workspace/backlog/BL-XXXX--<slug>.md` items capture
  ideas, worker and reviewer follow-ups, and acceptance limitations. Items are
  discussed with the human and promoted into a new feature plan (recorded as
  the plan's `origin`) or dropped; they are never deleted.
- `Follow-ups` section in worker and reviewer handoffs for out-of-scope ideas;
  required changes stay in reviewer findings.
- Feature README template with fixed sections, including `origin`, plan
  approval, and human acceptance.
- "Resuming a feature" procedure that rebuilds state from task records,
  handoffs, and git history, including plans still in `Draft` or awaiting
  acceptance.
- Handling for `partial` and `blocked` worker outcomes.
- Reviewers rerun the checks that prove acceptance criteria and record which
  checks they ran versus relied on from the worker.
- Default commit message convention when the repository has none.
- `references/dashboard.md` with the full dashboard description.
- Dashboard generator rejects task statuses not in the status table.

### Changed

- A failed third rework round and a task that needs a plan change now go
  through the `blocked` process, pausing the whole feature until the human
  decides.
- Feature plan returns to `Implementing` when the human requests changes at
  acceptance; step 4 sets `Implementing` on the first dispatch.
- Promoting a backlog item starts at step 1, on a branch that contains the item.
- Checkpoint commits include backlog items captured at that point.
- `queued` now means "dependencies not yet done"; the project-manager's
  status-only rule applies once a task is dispatched.
- SKILL.md dashboard section reduced to when and how to generate it; layout
  details moved to the reference file.

### Fixed

- `blocked` tasks appear in the dashboard's Project manager lane, as
  documented, instead of the Reviewer lane.
- The dashboard embeds the same DaisyUI stylesheet it validates.
- Stale dashboard test that had silently stopped checking for `innerHTML`.

### Removed

- Unused bundled Tailwind Browser and D3 files, their license notices, and a
  duplicate DaisyUI copy (about 1.7 MB).
- Undocumented `needs_human` and `waiting_human` dashboard statuses.
