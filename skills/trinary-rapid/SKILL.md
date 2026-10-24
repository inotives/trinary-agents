---
name: trinary-rapid
description: Deliver a small, well-bounded feature or fix fast with a predictable outcome — a short interview (at most two rounds), one plan approval, implementation by the main agent with optional subagents, one independent review, and a templated report rendered to HTML, kept in trinary-workspace/rapid/. Use when the human asks for a rapid or lightweight trinary feature, wants something done quickly without per-task handoffs, or wants to resume a rapid feature. For multi-module work, more than about five steps, or a dependency-tracked PM/worker/reviewer loop, use the full trinary-agents workflow instead.
---

# Trinary Rapid

Deliver a small feature as one approved plan, one implementation pass, one independent review, and one report. Predictability comes from a decision-complete interview and acceptance checks agreed up front, not from per-task handoffs. Keep the durable record in the target repository's root-level `trinary-workspace/rapid/` directory.

## Operating rules

- Work in the target project's repository root. Create or continue `<project-root>/trinary-workspace/`; do not put it under `docs/`, a home directory, or this skill's installation folder.
- Use ordinary Markdown and capabilities provided by the active agent harness. Do not require a specific agent runtime, vendor CLI, database, server, or network access. Python 3 is optional and used only to render the HTML report.
- Preserve existing files and work. Inspect before creating or changing anything. Never overwrite an existing rapid feature or backlog item.
- One rapid feature per folder. Its `README.md` is the plan and is canonical for scope, decisions, acceptance checks, and progress. There are no task folders, handoff files, or dashboards. Implementation changes the project's actual source, tests, configuration, and documentation.
- When committing, stage only the files that belong to the checkpoint. Leave out OS metadata such as `.DS_Store`. Follow the repository's commit message convention; if none exists, use a short imperative subject that names the rapid feature ID, such as `RF-0001: approve plan`.
- Never report self-verified work as independently reviewed.
- Do not push, merge, or open a pull request unless the human explicitly asks.

## Workflow

Each rapid feature lives in `trinary-workspace/rapid/RF-XXXX--<feature-title-slug>/` and holds `README.md` (the plan, status, and step checklist), `report.md`, and `report.html`. See [Status reference](#status-reference).

### 1. Start on a feature branch

Inspect the repository root, current branch, worktree, and branch naming convention. Start a dedicated branch before writing the plan; if the current branch already is the intended branch, continue there. If existing changes make branch ownership unclear, preserve them and ask the human how to proceed; do not stash, reset, discard, or silently move unrelated work. Without a convention, use `feat/<slug>`, or `fix/<slug>` for a bug fix. Do not reuse a branch name already in use.

### 2. Interview the human (at most two rounds)

If the feature starts from a backlog item, read it first and seed the interview with its description, reproduction, context, discussion, and open questions; do not re-ask what it settles.

Investigate the relevant code before and during the interview: read applicable `AGENTS.md` and project guidance, inspect the worktree, and find the modules, callers, tests, and configuration the change may touch. Finding facts is the agent's job; ask the human only for choices or context they own, and never repeat a question already answered.

Build a working decision tree of the choices that shape the feature and which depend on earlier answers. The frontier is the set of material decisions whose prerequisites are settled. Ask the frontier's independent questions together as one numbered round. Keep each question to one decision, give a recommendation with a short reason, and word it so "yes" accepts the recommendation. Wait for the answers, update the tree, and recalculate the frontier. Cover goal and success, scope and non-goals, key behavior, constraints, failure cases, and acceptance checks. Stop after two rounds by default; a third round happens only if the human asks for it.

### 3. Check whether rapid fits

Recommend a full trinary-agents feature plan instead when the change spans many modules, the plan needs more than about five steps, or material questions remain open after round 2. State which condition applies and why; the human decides. If they choose trinary-agents, stop without creating a rapid folder and summarize the interview findings for that workflow. If they choose rapid anyway, record the decision, and any open question as an explicit assumption, in the plan's Decisions.

### 4. Write the plan

Inspect `trinary-workspace/` first. If `README.md` is absent, create it to explain that the folder stores this project's workflow records, and record `Project name: <name>`; if the name cannot be identified confidently, ask the human. If the README does not mention `rapid/`, add a line saying that `rapid/` holds rapid features (plan, report, and rendered report per folder).

Choose the next unused four-digit number by inspecting `rapid/RF-*/`, create `trinary-workspace/rapid/RF-XXXX--<feature-title-slug>/README.md`, and write it from this template. Keep the frontmatter keys and section names, replace example values, and write `None` for sections that do not apply. Quote the human's answers in Context or Decisions where practical.

```markdown
---
id: RF-0001
title: Example rapid feature
status: Draft
branch: feat/example-rapid-feature
created_at: 2026-01-01T00:00:00Z
origin: null
---

# RF-0001: Example rapid feature

Origin: [BL-0001](../../backlog/BL-0001--example-idea.md), or `None` when the feature did not start from a backlog item.

## Goal

State the outcome and how success is recognized.

## Context

Summarize the request, quoting the human where practical, and the relevant repository findings.

## Scope

- List what this feature delivers.

## Non-goals

- List explicit exclusions.

## Decisions

- [YYYY-MM-DD] Decision, rationale, and who made it. Record delegated steps here.

## Acceptance checks

- [ ] State each check, with a command where possible.

## Steps

- [ ] 1. Describe a small, verifiable step. When done, tick it and add a one-line note: what changed, checks run.

## Plan approval

- Record the human's explicit approval and its UTC timestamp.
```

Steps are small, verifiable, and ordered. Each acceptance check states how it is verified, with a command where possible. The plan stays `Draft` until approved.

### 5. Get approval and commit the plan

Present the plan for review. This is the only approval gate: there are no per-step approvals and no separate acceptance step. Do not change project files until the human explicitly approves. Record the approval with its UTC timestamp under Plan approval, set `status: Approved`, and commit the plan (and the promoted backlog item, if any) on the feature branch. If `trinary-workspace/` is ignored by Git, do not force-add it; tell the human and record that in Decisions.

If the approved plan must change materially later, stop, explain the change, update the plan, and get approval again before continuing; record the change in Decisions and the new approval under Plan approval.

### 6. Implement

Set `status: Implementing`. The main agent implements by default. Use subagents only for steps that are independent and can run in parallel, or for heavy reading; record each delegated step and who did it in Decisions, and fold the subagent's result into that step's note. Do not create handoff files.

Work through Steps in order. After each step, tick it and add a one-line note: what changed and which checks ran, for example `- [x] 2. Add config parser — added src/config.py; ran pytest tests/test_config.py (passed)`. Never claim a check ran without evidence. Out-of-scope ideas and bugs found along the way go to Pending issues in the report, not into the current scope.

### 7. Run one independent review

Review is on by default. When implementation is done, start a reviewer subagent that did not implement any part of the work. Give it the plan, the diff since the plan commit including untracked files (`git status`), and the acceptance checks. Ask it to check correctness, scope, acceptance checks, and regressions, to run the checks itself where practical, and to report which checks it ran versus relied on, with concrete findings.

Fix in-scope findings, rerun the affected checks, and update the step notes. Findings that are not fixed go to Pending issues. Run one review; a second only if the human asks.

If the harness cannot delegate to an independent reviewer, tell the human, verify the work yourself, set `review: self-verified`, and write `Not independently reviewed.` in the Review section. If the human explicitly asks to skip review, set `review: skipped` and write the same sentence. In both cases, never describe the work as independently reviewed.

When the review is done, record in the plan's Decisions who reviewed and when, or that the work was self-verified or the review was skipped.

### 8. Write and render the report

Write `report.md` in the rapid feature folder from this template. Keep the frontmatter keys, section names, order, and table columns exactly; a renderer validates them.

```markdown
---
id: RF-0001
title: Example rapid feature
status: Reported
branch: feat/example-rapid-feature
plan_approved_at: 2026-01-01T00:00:00Z
reported_at: 2026-01-01T00:00:00Z
review: independent
reviewer: reviewer subagent
---

# RF-0001: Example rapid feature report

Plan: [README.md](README.md)

## Outcome

RESULT: DELIVERED

Summarize what was delivered and how it meets the goal in two or three sentences. Use `RESULT: DELIVERED` only when every acceptance check passed; otherwise use `RESULT: NOT_DELIVERED` when the goal is not met or no acceptance check passed, and `RESULT: PARTIAL` in every other case, and say why.

## Acceptance checks

| Check | Command / method | Result | Evidence |
| --- | --- | --- | --- |
| Copy each acceptance check from the plan | `command` or manual method | passed | Output summary or file reference |

## Changes

- `path/to/file` — One-line description of the change.

## Findings

- Record discoveries, risks, and decisions made during implementation, or write `None`.

## Review

- Reviewer: name the reviewing subagent when `review: independent`. When `review` is `self-verified` or `skipped`, write `Not independently reviewed.` and the reason, and set `reviewer: null`.
- Checks rerun: list the checks the reviewer ran itself.
- Findings: list each finding and how it was resolved, or write `None`.

## Pending issues

| Issue | Severity | Backlog |
| --- | --- | --- |
| Describe each unresolved or out-of-scope issue | medium | BL-0001 |

## Steps completed

- [x] 1. Copy the plan's Steps checklist with its notes.
```

- The first line of Outcome is exactly `RESULT: DELIVERED`, `RESULT: PARTIAL`, or `RESULT: NOT_DELIVERED`. Use `DELIVERED` only when every acceptance check passed. Use `NOT_DELIVERED` when the goal is not met or no acceptance check passed, and `PARTIAL` otherwise.
- Acceptance checks has one row per plan check; Result is `passed`, `failed`, or `not run`.
- Changes lists every changed file with a one-line description.
- `review` is `independent`, `self-verified`, or `skipped`; `reviewer` names the reviewing subagent when `review: independent`, and is `null` when `review` is `self-verified` or `skipped`.
- Pending issues uses severity `high`, `medium`, or `low`. Capture each out-of-scope issue as a backlog item and put its ID in Backlog; write `-` for issues not captured. With no pending issues, keep the table with a single row `| None | - | - |`.
- Steps completed copies the plan's checklist with its notes.

Render the HTML report with the skill's renderer:

```text
python3 <skill-dir>/scripts/render_report.py trinary-workspace/rapid/RF-XXXX--<slug>
```

Resolve `<skill-dir>` as the directory that contains this `SKILL.md`, not the project root; harnesses install skills in different locations (for example `.claude/skills/trinary-rapid/` or `.agents/skills/trinary-rapid/`). The renderer writes `report.html` beside `report.md`, embedding its stylesheet and the plan's goal, scope, and decisions; it makes no network requests. If it refuses because a frontmatter key, section, or `RESULT:` line is missing, fix `report.md` and rerun. If Python 3 is unavailable, tell the human and continue: `report.md` is the deliverable.

### 9. Finish

Set the plan's `status: Reported` and commit the implementation, plan, `report.md`, `report.html`, and any new backlog items together. If `trinary-workspace/` is ignored by Git, do not force-add it: commit only the implementation files and tell the human where the plan and report are. Give the human the outcome line, the report paths, and the pending issues. The report ends the flow. Later changes are a new rapid feature or follow-up run. Do not push or merge unless asked.

## Backlog

Rapid features share the trinary-workspace backlog in `trinary-workspace/backlog/`, one file per item: `BL-XXXX--<item-title-slug>.md`. Choose the next unused four-digit number by inspecting `backlog/BL-*.md`. When creating `backlog/`, add a mention of it to the workspace README if it is not already described.

- Capture an item when the human asks to record an idea or bug, or when the report lists an out-of-scope pending issue. Before creating one, check `open` and `discussing` items for the same idea or bug and append to it instead of duplicating.
- `type` is `idea` for new behavior or `bug` for a defect in existing behavior. A bug within the current scope is fixed or reported in the report, not captured.
- A rapid feature may start from a backlog item when the human chooses it. Set the plan's `origin` to the item's ID, set the item's `status` to `promoted` and `promoted_to: RF-XXXX`. From then on the plan is canonical. A promoted bug needs an acceptance check that fails before the fix and passes after it.
- When the human decides not to pursue an item, set it to `dropped` and append the dated reason. Never delete backlog items.
- Item statuses: `open` (captured), `discussing` (being shaped), `promoted` (became the feature in `promoted_to`), `dropped` (not pursued; reason recorded). Write items from this template:

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

- Link the report, plan, or conversation it came from, and relevant repository findings.

## Discussion

- [YYYY-MM-DD] Record each discussion round, quoting the human where practical.

## Open questions

- List questions to settle before or during the interview, or write `None`.
```

## Resuming a rapid feature

Rebuild state from the plan and the repository, not from earlier chat context.

1. Read the plan's `status` and confirm the current branch matches its `branch`. If it is `Draft`, resume the interview or approval. If it is `Approved`, start step 6. If it is `Reported`, the flow is finished; treat new requests as a new rapid feature or follow-up run.
2. If it is `Implementing`, read the Steps checklist and inspect `git status` and `git diff` (and `git log` since the plan commit).
3. Report what you found to the human: ticked steps, uncommitted changes, and any step that looks partially done. Verify partial work from the diff rather than guessing; finish or correct it, then continue from the first unticked step. If every step is ticked, continue with step 7 if no review is recorded in Decisions, otherwise with step 8; if `report.md` exists, re-validate and re-render it.

## Status reference

`Draft` (interviewing and writing the plan) → `Approved` (human approved; plan committed) → `Implementing` (steps and review in progress) → `Reported` (report written and committed with the implementation). The agent sets each status in the plan's frontmatter; only explicit human approval moves `Draft` to `Approved`.
