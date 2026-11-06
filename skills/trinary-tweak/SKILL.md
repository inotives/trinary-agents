---
name: trinary-tweak
description: Iterate on small, ad hoc changes — typically UI polish — in a fast human-in-the-loop session — the human asks, the agent changes, the human checks and gives feedback, repeat. No interview, plan, or per-change review; one session record and handoff in trinary-workspace/tweak/. Use when the human wants to tweak, polish, or iterate on something interactively, asks for a tweak session, or wants to resume or wrap up one. For changes that need upfront decisions or acceptance checks, use trinary-rapid; for multi-task features, use trinary-agents.
---

# Trinary Tweak

Run an interactive session of small changes where the human checks every iteration. There is no interview, plan approval, or reviewer gate during the loop; the spec emerges from feedback. What the skill adds over plain chat is a durable session record, a checkpoint commit per kept change, a scope guard that escalates work that is not a tweak, and an end-of-session handoff. Keep the record in the target repository's root-level `trinary-workspace/tweak/` directory.

## Operating rules

- Work in the target project's repository root. Create or continue `<project-root>/trinary-workspace/`; do not put it under `docs/`, a home directory, or this skill's installation folder.
- Use ordinary Markdown and capabilities provided by the active agent harness. Do not require a specific agent runtime, vendor CLI, database, server, or network access.
- Keep the loop fast. Do not write to the record on every iteration; write once per kept or dropped change, and at wrap-up.
- Preserve existing files and work. Never overwrite an existing tweak session or backlog item, and never revert or commit edits that do not belong to the session.
- Never make commits on the repository's default branch during a session.
- A branch has at most one `Active` session. Continue it rather than starting another; a new session on the same branch starts only after the open one is wrapped up.
- When committing, stage only the files and hunks that belong to the checkpoint. Leave out OS metadata such as `.DS_Store`. Follow the repository's commit message convention; if none exists, use a short imperative subject that names the session ID, such as `TW-0001: tighten card spacing`.
- If `trinary-workspace/` is ignored by Git, commit none of its files; commit only implementation files, unless the human explicitly asks to commit specific workspace files.
- The human checking each iteration is not an independent review, and neither are the agent's own checks. Never describe a tweak session as independently reviewed unless a reviewer that did not make the changes reviewed them at wrap-up.
- Do not push, merge, or open a pull request unless the human explicitly asks.

## Scope guard

A tweak is a change the human can judge by looking at or trying it: layout, styling, copy, component structure, small interaction behavior, and similar local edits. Stop and recommend trinary-rapid or trinary-agents when a request needs any of:

- a new or changed data model, API, persistence, migration, or backend logic;
- authentication, authorization, security, or payment behavior;
- coordinated changes across several modules, or decisions that should be settled before coding;
- acceptance that depends on designed tests rather than the human's judgment.

State which condition applies; the human decides. If they choose to continue here, record the decision in Decisions and continue. If they choose another workflow:

1. Settle the change in progress first: ask whether to keep it, drop it, or carry it over. Keep and drop follow step 3. A carried-over change stays uncommitted, is logged under Changes as `— carried over` with its files, and is listed under Open items with the workflow it moves to.
2. Wrap up the session (step 4), then start the other workflow.

## Workflow

Each session lives in `trinary-workspace/tweak/TW-XXXX--<session-slug>/README.md`. See [Status reference](#status-reference).

### 1. Start the session

Before creating anything, including a branch, look for an open session: inspect `trinary-workspace/tweak/TW-*/README.md` for `status: Active` and note each one's `branch`. Check these cases in order and act on the first that applies. Sessions on other branches are mentioned only when no session is `Active` on the current branch. Only records present in the working tree are found; in a project that commits `trinary-workspace/` to Git, a session that exists only on another branch is not detected.

- **The human explicitly asks for a new session:** if a session is `Active` on the current branch, follow [Starting a new session while one is open](#starting-a-new-session-while-one-is-open); otherwise start a new session with the steps below.
- **Exactly one `Active` session on the current branch:** resume it automatically through [Resuming a session](#resuming-a-session), without asking first. Open the reply with `Continuing tweak session TW-XXXX (<title>)`, the last kept change, and any in-progress edits, then handle the request as the session's next change. The human can reply "start a new session"; see [Starting a new session while one is open](#starting-a-new-session-while-one-is-open).
- **`Active` sessions only on other branches:** name each session and its branch. If the worktree is clean, ask whether to switch to that branch and resume it, or start a new session here. If the worktree has uncommitted changes, do not offer the switch: say that switching would carry or block those changes, list them, leave moving them to the human, and offer a new session here. Never switch branches without the human's answer.
- **Several `Active` sessions on the current branch** (possible with sessions from 1.0.0): list each ID, title, and last change, and ask which to resume. Uncommitted session edits belong to the chosen session. Offer to wrap up the others (step 4) with no change in progress, and note that in their Handoffs.
- **No `Active` session:** start a new session with the steps below.

To start a new session:

1. Inspect the repository root, current branch, and worktree.
   - If the current branch is the default branch, or a branch that belongs to unrelated work, create a session branch following the repository's convention, or `tweak/<slug>` without one. Otherwise continue on the current branch.
   - If the worktree has uncommitted changes, do not stash, reset, or discard them. List those files under Decisions as pre-existing; they are excluded from Changes, checkpoints, and the handoff. If session edits must touch one of them, tell the human, and stage only the session's hunks when committing.
2. Inspect `trinary-workspace/`. If `README.md` is absent, create it to explain that the folder stores this project's workflow records, and record `Project name: <name>`; ask the human if the name cannot be identified confidently. If the README does not mention `tweak/`, add a line saying that `tweak/` holds tweak sessions (one record and handoff per folder).
3. Choose the next unused four-digit number by inspecting `tweak/TW-*/`, and create the session README from the [session template](#session-template). Record the current `HEAD` as `base_commit`. Name the session from the human's first request; update the title later if the focus shifts, but keep the folder name.
4. If the session starts from a backlog item, read it, set the session's `origin` to its ID, set the item's `status` to `promoted` and `promoted_to: TW-XXXX`, and quote its description in Focus. From then on the session README is canonical. For a promoted bug, the agent confirms the item's reproduction no longer reproduces before the human checks the fix.
5. Checkpoint commits are on by default. Turn them off only if the human asks, and record `checkpoints: off`.

Do not hold an interview. Start on the first request immediately.

#### Starting a new session while one is open

When the human asks for a new session while one is `Active` on the current branch, close the open one first:

1. If the open session has a change in progress, ask whether to keep it (close it as kept in that session, with its checkpoint) or drop it (revert it, as in step 3). It is never carried into the new session.
2. Choose the next unused TW number for the new session.
3. Wrap up the open session (step 4), or each of them if several are `Active` on the branch, naming the new session's ID in each Handoff.
4. Create the new session with that ID (steps 1–5 above), and link the closed session in Focus.

### 2. Iterate

For each request from the human:

1. Investigate just enough to make the change: read the relevant component, styles, and callers. Apply the scope guard.
2. Make the smallest edit that satisfies the request. Do not fix unrelated things along the way.
3. Hand back briefly: what changed, which files, and where to look (route, screen, component, or state to reproduce). If the harness can preview or screenshot the result, you may check it yourself first; that never replaces the human's check.
4. Wait for feedback. Feedback on the same change is another iteration of that change; repeat from step 2 and do not write to the record.

Run fast checks, such as a typecheck or lint on touched files, when they take seconds; leave full test suites for wrap-up.

Out-of-scope ideas or bugs noticed along the way go to the backlog (see [Backlog](#backlog)); mention them to the human and keep going.

### 3. Close each change

A change is **kept** when the human approves it or moves on to an unrelated request. If it is unclear whether the human is moving on or still refining, ask in one short line before starting the next request. Moving on counts as approval only for loop speed; the record notes how each change was kept.

A change is **dropped** when the human asks to discard it. Undo only the edits this change made:

- With checkpoints on, restore the change's hunks to the last checkpoint commit (`base_commit` if none yet).
- With checkpoints off, undo the change's own edits from what you know you changed, since there is no commit to restore from; earlier kept changes are also uncommitted and must stay.
- In both cases, never restore whole files when they also hold pre-existing edits, human edits, or uncommitted edits from other changes. If those overlap the change's edits, show the overlap and ask before reverting. Afterwards, confirm with the human that the result looks as it did before the change.

When a change closes, append one entry under Changes:

```markdown
### C1: Tighten card spacing — kept (approved)

- Request: "the cards feel cramped, give them more room"
- Iterations: 3 — tried 24px gap (too loose), 12px (too tight); settled on 16px with 20px padding.
- Result: Card grid uses `gap-4` and `p-5`; hover shadow unchanged.
- Files: `src/components/CardGrid.tsx`, `src/components/Card.tsx`
- Commit: abc1234
```

The status after the title is `kept (approved)`, `kept (moved on)`, `dropped`, or `carried over`. Record the final result, not every attempt; the Iterations line keeps the rejected alternatives in one sentence. For a dropped change, write why under Result. Write `Commit: none` for dropped and carried-over changes, and `Commit: at wrap-up` for kept changes while checkpoints are off.

With checkpoints on, commit each kept change's implementation hunks, then record the commit's short SHA in the entry. The session README and any backlog item changes are committed with the next checkpoint or at wrap-up, so record updates ride along with later work instead of needing commits of their own. Do not amend commits.

### 4. Wrap up

Wrap up when the human says the session is done, asks for a handoff, or switches to another workflow. Settle any change in progress first, as in step 3.

1. Run the project's relevant checks — lint, typecheck, and tests covering touched files — and record each command and result under Checks. Never claim a check ran without evidence. When a check fails, find out whether the session caused it, for example by running it against `base_commit` in a temporary worktree or by reading the failure; a failure in a pre-existing uncommitted file counts as pre-existing:
   - Fix failures the session caused and rerun the check. If a fix would change something the human approved, ask first.
   - Record pre-existing failures under Checks as pre-existing, and do not fix them in this session; offer to capture them as backlog items.
2. Review is not run by default. If the human asks for one, start a reviewer subagent that did not make the changes. Give it the session README and the diff since `base_commit`, excluding pre-existing changes. Ask it to check correctness, regressions, and anything that contradicts a kept change. Fix the findings the human agrees with, record the reviewer and findings under Review, and set `review: independent` and `reviewer`. Otherwise keep `review: human-iterated`.
3. Write the Handoff section: a two-to-four-sentence summary, the session's files changed since `base_commit` (excluding pre-existing changes, one line each), open items, backlog items captured or promoted, and how to continue.
4. Commit the remaining implementation fixes, plus all kept changes when checkpoints were off, leaving out pre-existing and carried-over hunks. Replace each `Commit: at wrap-up` with that commit's short SHA. Then set `status: Closed` and `closed_at`, and, unless the workspace is ignored, commit the session README and backlog item changes as the final record commit. Give the human the summary, the record's path, and any open items.

Requests after a session is closed start a new session; link the earlier one in Focus.

## Session template

Keep the frontmatter keys and section names; write `None` for sections that stay empty.

```markdown
---
id: TW-0001
title: Example tweak session
status: Active
branch: tweak/example
base_commit: 0000000
origin: null
started_at: 2026-01-01T00:00:00Z
closed_at: null
checkpoints: per-change
review: human-iterated
reviewer: null
---

# TW-0001: Example tweak session

Origin: [BL-0001](../../backlog/BL-0001--example-item.md), or `None` when the session did not start from a backlog item.

## Focus

One or two sentences on what the human is polishing, quoting their first request.

## Changes

Append one entry per kept, dropped, or carried-over change (see step 3).

## Decisions

- [YYYY-MM-DD] Pre-existing uncommitted files at start, scope-guard overrides, turned-off checkpoints, and decisions that span changes.

## Checks

- `command` — result, marking pre-existing failures. Filled at wrap-up.

## Review

- Not independently reviewed; each change was checked by the human. Replace with the reviewer, checks rerun, and findings when a wrap-up review ran.

## Open items

- Unfinished requests, carried-over changes, known rough edges, or `None`.

## Handoff

Written at wrap-up: summary, files changed since `base_commit`, backlog items captured or promoted, and how to continue.
```

## Backlog

Tweak sessions share the trinary-workspace backlog in `trinary-workspace/backlog/`, one file per item named `BL-XXXX--<item-title-slug>.md`. Choose the next unused four-digit number by inspecting `backlog/BL-*.md`. When creating `backlog/`, add a mention of it to the workspace README if it is not already described.

- Capture an item when the human asks to record an idea or bug, or when an out-of-scope idea, bug, or pre-existing check failure comes up during the session. Before creating one, check `open` and `discussing` items for the same idea or bug and append to it instead of duplicating. List captured IDs in the Handoff.
- `type` is `idea` for new behavior or `bug` for a defect in existing behavior. A defect in the change being iterated on is part of that change, not a backlog item.
- A session may start from an item when the human chooses it; see step 1.
- When the human decides not to pursue an item, set it to `dropped` and append the dated reason. Never delete backlog items.
- Item statuses: `open` (captured), `discussing` (being shaped), `promoted` (became the feature or session in `promoted_to`), `dropped` (not pursued; reason recorded). Write items from this template:

```markdown
---
id: BL-0001
title: Example item
type: idea
status: open
created_at: 2026-01-01T00:00:00Z
source: human request
promoted_to: null
---

# BL-0001: Example item

## Description

Describe the problem, opportunity, or defect in a few sentences.

## Reproduction

For `type: bug` only; remove this section for ideas.

- Steps to reproduce: [numbered steps, with environment or version]
- Expected: [what should happen]
- Actual: [what happens, with error output if any]

## Context and evidence

- Link the session, plan, or conversation it came from, and relevant repository findings.

## Discussion

- [YYYY-MM-DD] Record each discussion round, quoting the human where practical.

## Open questions

- List questions to settle, or write `None`.
```

## Resuming a session

Rebuild state from the session README and the repository, not from earlier chat context.

1. Read the README's `status` and confirm the current branch matches `branch`. If it is `Closed`, start a new session for new requests.
2. If it is `Active`, compare the last logged change with `git log` since `base_commit` and with `git status`, setting aside the pre-existing files listed in Decisions. With checkpoints on, uncommitted session edits after the last checkpoint belong to the change in progress. With checkpoints off, uncommitted edits also hold every kept change; match them against the files in the Changes entries, and treat the rest as the change in progress. A checkpoint commit with no matching entry under Changes is a kept change whose record update was interrupted; write its entry from the commit.
3. Tell the human what you found, starting with `Continuing tweak session TW-XXXX (<title>)`, then the last kept change and any in-progress edits, and continue iterating, or wrap up if they ask.

## Status reference

Tweak sessions have their own two statuses, separate from the plan statuses that trinary-agents and trinary-rapid share: `Active` (iterating) → `Closed` (wrap-up done and handoff written). A branch has at most one `Active` session at a time. There is no approval or acceptance status: the human approves each change as it happens, and the session record is the evidence. Likewise, `review: human-iterated` is tweak-only vocabulary for "checked by the human during the loop, not independently reviewed"; do not align either with rapid's values.
