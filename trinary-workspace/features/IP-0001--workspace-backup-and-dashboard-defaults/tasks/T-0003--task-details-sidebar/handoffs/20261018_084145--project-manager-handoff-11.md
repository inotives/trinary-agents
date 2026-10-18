# Project Manager Handoff

- Task: T-0003 — Open task details in the dashboard sidebar
- Role: Project manager
- Timestamp: 2026-10-18T08:41:45Z
- Event: Human-reported display issue
- Recipient: Worker
- Outcome: Rework requested
- Summary: The completed task detail view displays `Owner: Completed`, which confuses a terminal task state with an owner. Omit the Owner metadata row when its value is `Completed`; keep owner information for active tasks. Preserve dashboard card semantics and other detail behavior.
- Next action: Implement the conditional task detail row, regenerate the dashboard, and append a worker handoff.
