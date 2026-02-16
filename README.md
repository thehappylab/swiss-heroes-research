# openclaw-data

Configuration and workspace seed data for a multi-agent OpenClaw setup.

This repository stores:
- a central runtime configuration in `openclaw.json`
- workspace-specific identity/behavior documents for agent personas

## Repository Layout

```text
openclaw-data/
├── openclaw.json
├── workspace-builder/
│   ├── AGENTS.md
│   ├── BOOTSTRAP.md
│   ├── IDENTITY.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   └── USER.md
└── workspace-growth/
    ├── AGENTS.md
    ├── BOOTSTRAP.md
    ├── IDENTITY.md
    ├── SOUL.md
    ├── TOOLS.md
    └── USER.md
```

## What `openclaw.json` Configures

The `openclaw.json` file defines four major areas:

- `agents`: available agent profiles and their workspaces
- `tools`: globally enabled tools (for example agent-to-agent and web search)
- `channels`: channel credentials (here: Discord bot accounts)
- `bindings`: routing rules from incoming channel/account -> agent

### Current Agent Definitions

Configured agents:

- `growth` (default): workspace `/data/workspace-growth`
- `builder`: workspace `/data/workspace-builder`
- `admin`: workspace `/data/workspace-admin`

Note: this repository currently includes `workspace-growth` and `workspace-builder` directories. If you use the `admin` agent, ensure `/data/workspace-admin` exists in your runtime environment.

### Tool Configuration

- `agentToAgent.enabled: true`
- `agentToAgent.allow: ["growth", "builder", "admin"]`
- `web.search.enabled: true`
- `web.search.provider: "brave"`
- `web.search.apiKey` is read from environment variable `BRAVE_WEBSEARCH_API_KEY`

### Channel and Binding Configuration

Discord accounts configured:

- `growth-bot` -> token from `DISCORD_GROWTH_BOT_TOKEN`
- `builder-bot` -> token from `DISCORD_BUILDER_BOT_TOKEN`
- `admin-bot` -> token from `DISCORD_ADMIN_BOT_TOKEN`

Bindings route messages by channel + account:

- `discord/growth-bot` -> `growth`
- `discord/builder-bot` -> `builder`
- `discord/admin-bot` -> `admin`

## Environment Variables

Set these before starting your OpenClaw runtime:

- `BRAVE_WEBSEARCH_API_KEY`
- `DISCORD_GROWTH_BOT_TOKEN`
- `DISCORD_BUILDER_BOT_TOKEN`
- `DISCORD_ADMIN_BOT_TOKEN`

## Workspace Document Purpose

Each workspace contains role-specific operating documents:

- `BOOTSTRAP.md`: first-run initialization instructions (typically delete after onboarding)
- `IDENTITY.md`: role identity (name, vibe, role)
- `SOUL.md`: operating principles and boundaries
- `USER.md`: user/collaborator context and communication preferences
- `TOOLS.md`: local operational notes and conventions
- `AGENTS.md`: recurring session workflow, memory rules, and safety expectations

## Typical Update Workflow

1. Update `openclaw.json` for agents/tools/channels/bindings.
2. Keep each workspace docs set aligned with the persona and operating style.
3. Ensure required environment variables are present in deployment.
4. Validate that each configured workspace path exists in the runtime container/host.

## Security Notes

- Do not commit real API keys or Discord bot tokens.
- Keep secret values injected via environment variables only.
- Review channel bindings before deploying to avoid misrouting messages.

## License

No license file is currently present in this repository. Add one if distribution or reuse terms are needed.
