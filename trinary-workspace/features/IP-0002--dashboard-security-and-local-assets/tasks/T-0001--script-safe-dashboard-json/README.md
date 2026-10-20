---
id: T-0001
feature: IP-0002
title: Make embedded dashboard JSON script-safe
status: ready
depends_on: []
---

# T-0001: Make embedded dashboard JSON script-safe

Feature plan: [IP-0002](../../README.md)

## Scope

Use a shared HTML-safe JSON serializer for all data embedded in the dashboard's inline script, including task data, handoffs, and dependency layout. Add regression coverage for a task ID containing a script-closing payload and verify the emitted JSON remains usable by the dashboard.

## Out of scope

- Replacing D3 or other dashboard assets.
- Changing task ID validation or dashboard behavior.
- Rewriting the generator in another language.

## Dependencies

None.

## Acceptance criteria

- [ ] Every JSON value embedded in the inline script uses the same HTML-safe serialization path.
- [ ] A malicious task ID such as `</script><script>alert(1)</script>` does not terminate the inline script or create an executable element.
- [ ] Regression coverage confirms the encoded task and dependency data remains valid when read by the dashboard.
- [ ] Existing focused generator tests pass.
- [ ] `git diff --check` passes.

## Implementation notes

- Generator: `skills/trinary-agents/scripts/generate_dashboard.py`.
- Focused tests: `skills/trinary-agents/tests/test_generate_dashboard.py`.
- Task IDs are included as keys in `dependency_layout`; existing script-safety coverage exercises a task title but not this path.

## Handoffs

Append project-manager, worker, reviewer, and human-response records in [`handoffs/`](handoffs/). Do not overwrite earlier handoffs.
