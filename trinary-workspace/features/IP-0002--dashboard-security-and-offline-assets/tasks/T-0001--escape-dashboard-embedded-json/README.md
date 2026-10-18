---
id: T-0001
feature: IP-0002
title: Escape dashboard embedded JSON
status: done
depends_on: []
---

# T-0001: Escape dashboard embedded JSON

Feature plan: [IP-0002](../../README.md)

## Scope

Make JSON embedded inside the generated dashboard's executable script safe from
HTML script-element termination, including the `dependency_layout` value
derived from task IDs. Add a focused regression check for malicious task-derived
text.

## Out of scope

- Removing remote dashboard assets; that is T-0002.
- Changing dashboard behavior, layout, or task parsing rules.

## Dependencies

- None.

## Acceptance criteria

- [ ] Every JSON value embedded in the generated script is encoded so
  task-derived `</script>` cannot terminate the script element.
- [ ] Regression coverage proves the raw terminator is absent while the
  embedded task and dependency JSON remain parseable.
- [ ] Existing task and handoff text rendering continues to use text-safe DOM
  APIs.

## Implementation notes

- Relevant implementation: `skills/trinary-agents/scripts/generate_dashboard.py`.
- Relevant tests: `skills/trinary-agents/tests/test_generate_dashboard.py`.
- Reuse the escaping behavior already applied to task and handoff JSON so the
  serialized script data has one consistent safety rule.

## Handoffs

Append project-manager, worker, reviewer, and human-response records in
[`handoffs/`](handoffs/). Do not overwrite earlier handoffs.
