# TOOLS.md - Local Notes

Skills define how tools work. This file stores local specifics.

## What Goes Here

- Repo layout and service ownership notes
- Deployment and rollback checklist details
- Test commands, environments, and release conventions

## Startup Build Conventions

- Prefer iterative slices over big-bang rewrites.
- Keep acceptance criteria explicit for each milestone.
- Add tests for critical user-facing flows.
- **New projects:** Always keep source code in a subfolder of the workspace (`/data/openclaw-data/workspace-builder/code/<project-name>/`). Do not clone or scaffold outside the workspace.

## Sub-Agent Timeouts

Default `runTimeoutSeconds` is too short for heavy tasks. Always set it explicitly:

- **Light tasks** (search, read, check): default (~300s)
- **Medium tasks** (code changes, single PR): `runTimeoutSeconds: 600`
- **Heavy tasks** (scaffold + deploy + verify): `runTimeoutSeconds: 1200`

Never rely on the default for anything involving builds, deployments, or multi-step workflows.

## Sub-Agent Task Prompts

When spawning sub-agents, always include this instruction in the task:

> Work silently. Do not narrate each step or tool call. Only report a concise summary when done: what was built, what changed, and any issues.

Sub-agents that stream their thinking into the channel are unreadable. Keep output to a final summary only.
