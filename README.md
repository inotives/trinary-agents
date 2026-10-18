<p align="center">
  <img src="assets/trinary-agents.svg" alt="Trinary Agents mark" width="150">
</p>

<h1 align="center">trinary-agents</h1>

<p align="center">
  An agent-harness-agnostic workflow for planning and delivering feature work.
</p>

<p align="center">
  Human-approved plans, dependency-aware tasks, independent review, and durable Markdown handoffs.
</p>

<p align="center">
  <a href="skills/">Skills</a>
  ·
  <a href="LICENSE.md">MIT License</a>
</p>

---

## What This Repository Contains

`trinary-agents` is a focused home for skills and supporting tools for a
project-manager, worker, and reviewer workflow. The core workflow uses ordinary
Markdown files so plans, tasks, and handoffs remain readable across agent
harnesses. It aims to work with Codex, Claude, Pi, OpenCode, and other agents
that provide delegation capabilities.

Harness-specific discovery or installation instructions can be added alongside
the core skills without making those integrations requirements of the workflow.

## Why This Project Exists

I created [AgentRig](https://github.com/inotives/agent-rig) to scaffold and run
multi-agent workflows using configurable agent profiles. It defaults to SQLite
for workflow state and also supports Markdown storage.

Even with that tooling, I found the initial setup could feel difficult, and
ad-hoc tasks could feel disconnected from the ongoing workflow. That experience
led me to express the tri-agent workflow as portable skills with plain Markdown
plans, task records, and handoff logs. The goal is to make the workflow easier
to start and keep its activity visible in the project, without requiring a
dedicated runtime or database.

## Skill Model

Each skill lives in its own directory and can be copied independently:

```text
skills/
└── <skill-name>/
    ├── SKILL.md          # purpose, trigger, workflow, requirements, limits
    ├── scripts/          # optional supporting tools
    └── tests/            # optional checks for supporting tools
```

`SKILL.md` is the source of truth for each skill. Add scripts and tests only
when a skill needs them; keep the core instructions portable and document any
runtime assumptions at the skill that introduces them.

## Skills

| Skill | What it does |
| --- | --- |
| [Trinary Agents](skills/trinary-agents/SKILL.md) | Plan feature work, track dependencies, coordinate implementation and independent review, and preserve decisions in Markdown handoffs. |
| [Trinary Workspace Backup](skills/trinary-workspace-backup/SKILL.md) | Back up, verify, and restore `trinary-workspace/` through a connected Google Drive integration. |

To install Trinary Agents for Codex in your project, run this from the project
root:

```sh
npx skills add inotives/trinary-agents --skill trinary-agents --agent codex
```

## How the Workflow Works

![Trinary Agents workflow from human-approved plan through project manager, worker, independent reviewer, Markdown task records, and the optional monitoring dashboard](assets/trinary-agents-workflow.svg)

For any feature with one or more valid task READMEs, the skill generates a
read-only dashboard for monitoring task status, dependencies, progress, and
handoff activity. Task READMEs remain the source of truth. Each task card has a
top-right details button that opens the full task README in the same sidebar
used for handoff details.
Dashboard generation requires Python 3 and uses only the standard library; no
Python packages need to be installed. On macOS, check with `python3 --version`.
If the command is unavailable, install Python 3 using the macOS installer from
[python.org](https://www.python.org/downloads/macos/), then open a new terminal
and verify the command again.

## Trinary Agents UI Dashboard

![Trinary Agents task dashboard showing completion, dependency map, task lanes, and handoff activity](assets/trinary-agents-dashboard-ui.png)

## Optional Supporting Skills and Tools

The core workflow works with ordinary Markdown and the repository tools already
available in the active harness. Its feature-planning interview is built into
the Trinary Agents skill; no separate grilling skill is required. These optional
capabilities can help with other steps when available:

| Workflow step | Optional capability | How it can help |
| --- | --- | --- |
| Explore a larger codebase | `context-mode` | Search and summarize repository context without loading large files into the conversation. |
| Navigate symbols and call paths | CodeGraph | Locate relevant code relationships when the repository has an index. |
| Implement and review tasks independently | The active harness's agent delegation feature | Assign worker and reviewer roles to different agents. Independent delegation is needed to perform the independent review gate. |

Sub-agents usually start with little or no repository context. Without
`context-mode` and CodeGraph, they may scan broad parts of the codebase again for
each assigned task, increasing setup time and token use. When available,
`context-mode` can retrieve focused repository context and CodeGraph can surface
relevant symbols and call paths, reducing repeated exploration and saving
tokens. CodeGraph is most useful when the repository has an index.

If an optional search or planning skill is unavailable, use the repository's
normal search, file-reading, and interview workflow. If the harness cannot
delegate an independent reviewer, follow the capability boundary in the core
skill and ask the human how to proceed.

## Workflow Records

The Trinary Agents workflow stores feature plans, task briefs, and handoffs in
a `trinary-workspace/` directory at the target project's repository root. The
skill's `SKILL.md` defines its structure and rules.

## Development Principles

- Keep the smallest complete implementation.
- Keep the core workflow independent of any one agent harness.
- Prefer ordinary Markdown and existing platform capabilities over new services or dependencies.
- Keep each skill independently understandable and copyable.
- Document capability limits and never claim checks that were not run.

## License

This project is licensed under the [MIT License](LICENSE.md).
