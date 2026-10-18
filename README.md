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

## Optional Supporting Skills and Tools

The core workflow works with ordinary Markdown and the repository tools already
available in the active harness. These optional capabilities can help with
specific steps; use them when available rather than treating them as
requirements:

| Workflow step | Optional capability | How it can help |
| --- | --- | --- |
| Clarify and record a plan | `grill-with-docs` | Interview for missing decisions and capture useful decision records. |
| Interview without separate records | `grill-me` or another grilling skill | Ask focused questions until the feature plan is ready for review. |
| Clarify domain language | `domain-modeling` or related domain skills | Agree on terms and boundaries before decomposing the work. |
| Explore a larger codebase | `context-mode` | Search and summarize repository context without loading large files into the conversation. |
| Navigate symbols and call paths | CodeGraph | Locate relevant code relationships when the repository has an index. |
| Shape module boundaries | `codebase-design` | Review interfaces and identify focused implementation seams. |
| Implement and review tasks independently | The active harness's agent delegation feature | Assign worker and reviewer roles to different agents. Independent delegation is needed to perform the independent review gate. |

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
