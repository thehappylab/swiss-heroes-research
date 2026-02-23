# MEMORY.md

## System Configuration

### OpenClaw Config Paths

- `/data/.openclaw/openclaw.json` — test-only, ephemeral changes
- `/data/openclaw-data/openclaw.base.json` — persistent configuration (persist changes here)

Source: Marcel reminded me on 2025-06-20

## Development Workflow (Feature → Production)

Standard process for implementing features:

1. **Get Task/Specification** - Read spec from Outline/Fizzy/GitHub
2. **Ask for Clarification** - If requirements are unclear
3. **Local Development** - Create feature branch, implement
4. **Playwright Tests** - Write e2e tests verifying the spec
5. **Local Verification** - Production build, e2e tests, click-through
6. **Create PR** - Push to GitHub, Coolify auto-builds preview
7. **Verify Preview** - Test deployed preview app
8. **Report to User** - Give preview URL, build status, migration info
9. **Wait for Approval** - User reviews and approves
10. **Merge & Deploy** - To production when approved

**Always include migration details if required.**

**Skill file:** `~/openclaw-data/workspace-build/skills/feature-dev-workflow/SKILL.md`
