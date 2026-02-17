# Google Workspace Setup Guide

## Prerequisites

1. **Google Cloud Project** with these APIs enabled:
   - Gmail API
   - Google Calendar API
   - Google Drive API
   - Google Docs API
   - Google Sheets API
   - Google Slides API

2. **OAuth 2.0 Client ID** (Desktop application type)

No external Python dependencies required — the auth script uses only stdlib.

## Step-by-step Setup

### 1. Create OAuth 2.0 Client ID

In Google Cloud Console:
- Go to **APIs & Services → Credentials**
- Click **Create Credentials → OAuth client ID**
- Application type: **Desktop app**
- Name: e.g. `openclaw-workspace`
- Click **Create**
- Click **Download JSON** (saves as `client_secret_xxx.json`)

### 2. Configure OAuth Consent Screen

If not already done:
- Go to **APIs & Services → OAuth consent screen**
- User type: **Internal** (for Workspace accounts) or **External**
- Fill in app name, support email
- Add scopes (or skip — we request them at auth time)
- Add test users if using External type: `hello@thehappylab.com`

### 3. Run One-Time Authorization

```bash
python3 /data/openclaw-data/skills/google-workspace/scripts/gw-auth.py \
  --setup --client-secret /path/to/client_secret_xxx.json
```

This will:
1. Print an authorization URL
2. Open a local server on port 8085
3. After browser consent, capture the code and exchange for tokens
4. Save credentials to `/data/openclaw-data/secrets/google-oauth-credentials.json`

**If running headless (no browser):** Copy the printed URL, open it on any machine, complete consent. The redirect to `localhost:8085` will fail on the remote machine — in that case, copy the `code` parameter from the failed redirect URL and we can exchange it manually.

### 4. Test

```bash
TOKEN=$(python3 /data/openclaw-data/skills/google-workspace/scripts/gw-auth.py -s gmail)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/profile"
```

Should return `{ "emailAddress": "hello@thehappylab.com", ... }`.

## Credential Storage

### Option 1: Environment Variables (preferred)

Set these three env vars in your OpenClaw config or `.env`:

```
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REFRESH_TOKEN=1//your-refresh-token
```

The `--setup` flow prints the refresh token at the end. Copy it into your env.

### Option 2: Credentials File (fallback)

If env vars are not set, the script falls back to:
```
/data/openclaw-data/secrets/google-oauth-credentials.json
```

The `--setup` flow saves this file automatically. File permissions are set to `600`.

---

The refresh token doesn't expire unless revoked or unused for 6 months.
To re-authorize, run `--setup` again.
