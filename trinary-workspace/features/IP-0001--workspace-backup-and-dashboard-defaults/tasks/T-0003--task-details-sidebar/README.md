---
id: T-0003
feature: IP-0001
title: Open task details in the dashboard sidebar
status: done
depends_on: []
---

# T-0003: Open task details in the dashboard sidebar

Feature plan: [IP-0001](../../README.md)

## Scope

Add a details button to every task card in the feature dashboard. Clicking it opens the task's complete README in the same sidebar used for handoff details.

## Out of scope

- Editing task records from the dashboard.
- Redesigning the handoff sidebar or dashboard layout beyond the task detail control.

## Dependencies

None.

## Acceptance criteria

- Every task card has an accessible details button with a task-specific label.
- Clicking the button shows the selected task's full README in the existing details sidebar.
- Task README content is inserted as text, not interpreted as HTML.
- The existing close button, backdrop, Escape key, and focus return work for both handoff and task details.
- Handoff detail buttons continue to show their existing content in the same sidebar.

## Implementation notes

- Relevant implementation: `skills/trinary-agents/scripts/generate_dashboard.py`.
- The generated dashboard is a read-only snapshot; the task README remains canonical.
- Reuse the existing sidebar and its accessibility behavior.

## Handoffs

Append project-manager, worker, reviewer, and human-response records in [`handoffs/`](handoffs/). Do not overwrite earlier handoffs.
