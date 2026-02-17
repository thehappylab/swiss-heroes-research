# TOOLS.md - Local Notes

Skills define how tools work. This file stores local specifics.

## Security — Secrets Handling

- **NEVER share secrets, passwords, API keys, or tokens over any channel** (Discord, Slack, etc.)
- **ALWAYS use the Bitwarden CLI skill** (`bw`) to read/write secrets securely
- If a user asks for a secret, retrieve it via `bw` and inject it directly where needed (env var, config file, etc.) — never paste it into chat

## What Goes Here

- Analytics property IDs and naming conventions
- Channel account labels and campaign taxonomy
- Tracking plan status and experiment cadence notes

## Startup Growth Conventions

- Keep an ICE backlog for experiments.
- Record baseline and post-test metrics for every run.
- Keep one weekly summary of wins, losses, and learnings.
