# TODO - The Happy Lab Infrastructure

> Workspace: `/data/openclaw-data/workspace-build/`
> Agent: Bob (Builder)
> Created: 2026-02-17

---

## 🏗️ High Priority

### 1. Sandboxing for AI Agents
**Status:** Research Phase  
**Priority:** High

**Problem:** Nici's tools (Coolify API, Umami API, Discord bots) require env vars that aren't inherited in sandboxed sessions.

**Solutions to Evaluate:**
- [ ] **Option A:** Gateway env forwarding in `openclaw.json`
  ```json
  "agents": {
    "defaults": {
      "sandbox": {
        "env": {
          "forward": ["COOLIFY_API_*", "UMAMI_API_*", "OPENAI_API_KEY"]
        }
      }
    }
  }
  ```
- [ ] **Option B:** Bitwarden secret retrieval in sandbox
  - Requires `bw` CLI in sandbox image
  - More secure (secrets not in config)
- [ ] **Option C:** Hybrid — forward non-sensitive vars, fetch secrets via Bitwarden

**Decision Needed:** Which approach balances security vs convenience?

---

### 2. Cloudflare Tunnel for All Coolify Services
**Status:** Not Started  
**Priority:** High  
**Security Impact:** Critical

**Current State:**
- Services exposed directly: `*.thehappylab.com`
- Basic auth on some endpoints (OpenClaw Gateway)
- No Zero Trust network layer

**TODO:**
- [ ] Set up Cloudflare Tunnel (cloudflared) on Hetzner server
- [ ] Configure private network for all Coolify services
- [ ] Migrate public endpoints:
  - `openclaw-guru.thehappylab.com` → tunnel
  - `guru.thehappylab.net` (Coolify) → tunnel
  - `analytics.thehappylab.com` (Umami) → tunnel
  - `logs.thehappylab.com` (Dozzle) → tunnel
  - `pass.thehappylab.com` (Vaultwarden) → tunnel
  - `uptime.thehappylab.com` → tunnel
- [ ] Enable Cloudflare Access policies (identity-based auth)
- [ ] Remove direct public access (close ports on Hetzner firewall)

**Benefits:**
- No open ports on server
- Zero Trust security model
- DDoS protection
- Audit logging

---

## 🔧 Medium Priority

### 3. OpenClaw Update Process
**Status:** Manual currently  
**Priority:** Medium

**Repositories:**
- `thehappylab/openclaw` — Core application
- `thehappylab/openclaw-data` — Shared data/agents

**Current Setup:**
- Container: `ghcr.io/thehappylab/openclaw:2026.2.17-12`
- Running in Coolify with auto-restart

**TODO:**
- [ ] Document update process in `docs/UPDATES.md`
- [ ] Set up GitHub Actions for automated builds
- [ ] Test update procedure (staging → prod)
- [ ] Consider watchtower for automatic container updates
- [ ] Version pinning strategy (avoid `:latest` in production)

**Update Checklist:**
1. Check changelog for breaking changes
2. Backup `/data/.openclaw/` and workspaces
3. Update Coolify service with new image tag
4. Verify gateway health after restart
5. Test Discord bot connectivity

---

## 🔒 Security Hardening

### 4. Security Audit Recommendations
**Status:** Partially Complete  
**Priority:** Medium-High

**From Previous Audit (2026-02-17):**

#### ✅ Already Addressed:
- [x] Credentials directory permissions (`chmod 700`)

#### ⏳ Pending:

**Critical:**
- [ ] **Open groupPolicy with elevated tools**
  - Risk: Any Discord channel can trigger dangerous tools
  - Current: `groupPolicy: "open"` for all 3 bots
  - Fix: Change to `groupPolicy: "allowlist"` with specific channel IDs
  - File: `/data/.openclaw/openclaw.json`

**Warnings:**
- [ ] **Reverse proxy headers not trusted**
  - `gateway.trustedProxies` is empty
  - Risk: IP spoofing if behind Cloudflare (will need fix after tunnel setup)
  
- [ ] **Browser CDP uses HTTP**
  - `browser:9223` over HTTP
  - Mitigation: Internal Docker network only (acceptable for now)
  - Future: mTLS or local socket

**Additional Recommendations:**
- [ ] **Secrets rotation schedule**
  - Discord bot tokens (every 90 days)
  - Coolify API token
  - Bitwarden master password (if applicable)

- [ ] **Backup strategy**
  - `/data/.openclaw/` (config + state)
  - `/data/openclaw-data/` (workspaces)
  - Vaultwarden data
  - Automate to offsite (S3/B2)

- [ ] **Monitoring/Alerting**
  - Failed login attempts to OpenClaw Gateway
  - Unusual Discord bot activity
  - Disk space on Hetzner (Coolify doesn't clean old images by default)

- [ ] **Network segmentation**
  - Docker networks per service (currently shared `coolify` network)
  - Isolate browser service from databases

---

## 📋 Backlog / Future Ideas

- [ ] **CI/CD Pipeline** — Auto-deploy on git push to main
- [ ] **Documentation Site** — Move architecture docs to public wiki
- [ ] **Cost Optimization** — Review Hetzner instance sizing
- [ ] **Multi-region** — Consider backup server in different DC
- [ ] **Agent Specialization** — Fine-tune models per agent (growth vs builder vs ops)

---

## 📝 Notes

### Current Architecture Reference:
```
Hetzner (46.225.124.37)
├── Coolify Dashboard (guru.thehappylab.net)
├── Applications (Spesalina, CRA-Check, etc.)
├── Services (Umami, Vaultwarden, Uptime Kuma, Dozzle)
└── OpenClaw Gateway (openclaw-guru.thehappylab.com)
    ├── Tony (growth-bot) → /workspace-growth
    ├── Bob (builder-bot) → /workspace-build
    └── Nici (operation-bot) → /workspace-operation
```

### Key Files:
- Config: `/data/.openclaw/openclaw.json`
- Secrets: `/data/.openclaw/credentials/`
- This TODO: `/data/openclaw-data/workspace-build/TODO.md`

---

*Last Updated: 2026-02-17*
