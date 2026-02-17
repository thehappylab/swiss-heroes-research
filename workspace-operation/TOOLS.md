# TOOLS.md - Local Notes

Use this file for operation-specific details and conventions.

## Security — Secrets Handling

- **NEVER share secrets, passwords, API keys, or tokens over any channel** (Discord, Slack, etc.)
- **ALWAYS use the Bitwarden CLI skill** (`bw`) to read/write secrets securely
- If a user asks for a secret, retrieve it via `bw` and inject it directly where needed (env var, config file, etc.) — never paste it into chat

## What Goes Here

- Email inboxes, labels, and triage rules
- Finance systems, report links, and close checklist
- Customer success playbooks and escalation paths
- Team role map and handoff templates

## Working Conventions

- Keep a daily operating checklist.
- Track each item with owner, due date, and status.
- Summarize risks and blockers at end of day.
