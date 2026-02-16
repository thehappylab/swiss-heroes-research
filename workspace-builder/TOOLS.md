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
