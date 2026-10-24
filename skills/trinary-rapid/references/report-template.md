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
