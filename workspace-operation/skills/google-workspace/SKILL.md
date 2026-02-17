---
name: google-workspace
description: >
  Manage Google Workspace for hello@thehappylab.com: Gmail (read, search, send, label, archive),
  Google Calendar (list events, create/update/delete events, accept/decline invites, check availability),
  and Google Drive with Docs, Sheets, Slides, and Presentations (search, read, create, edit, export).
  Use when the user asks to check email, read inbox, send an email, manage calendar, schedule meetings,
  find files in Drive, read or edit Google Docs/Sheets/Slides, or any Google Workspace task.
---

# Google Workspace

Manage Gmail, Calendar, and Drive for `hello@thehappylab.com` via Google REST APIs.

## Authentication

Get an access token using the OAuth2 helper (uses refresh token, no external dependencies):

```bash
TOKEN=$(python3 /data/openclaw-data/skills/google-workspace/scripts/gw-auth.py --scopes gmail,calendar,drive)
```

Scope shortcuts: `gmail`, `gmail.readonly`, `calendar`, `calendar.readonly`, `drive`, `drive.readonly`, `sheets`, `docs`, `slides`.

Request only the scopes needed for the task. Prefer read-only variants when not modifying data.

Credentials are read from env vars (preferred) or a file fallback:
- `GOOGLE_CLIENT_ID` — OAuth client ID
- `GOOGLE_CLIENT_SECRET` — OAuth client secret
- `GOOGLE_REFRESH_TOKEN` — refresh token from consent flow

If auth fails with missing credentials, read [setup.md](references/setup.md) for initial OAuth setup (one-time browser consent flow to obtain the refresh token).

## Quick Patterns

### Check inbox (unread)

```bash
TOKEN=$(python3 /data/openclaw-data/skills/google-workspace/scripts/gw-auth.py -s gmail.readonly)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages?q=is:unread&maxResults=10"
```

Then fetch each message by ID with `format=metadata` (for headers only) or `format=full`.

### Send an email

Build an RFC 2822 message, base64url-encode it, POST to `/users/me/messages/send`.

### List today's calendar events

```bash
TOKEN=$(python3 /data/openclaw-data/skills/google-workspace/scripts/gw-auth.py -s calendar.readonly)
TODAY=$(date -u +%Y-%m-%dT00:00:00Z)
TOMORROW=$(date -u -d "+1 day" +%Y-%m-%dT00:00:00Z)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=$TODAY&timeMax=$TOMORROW&singleEvents=true&orderBy=startTime"
```

### Search Drive files

```bash
TOKEN=$(python3 /data/openclaw-data/skills/google-workspace/scripts/gw-auth.py -s drive.readonly)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q=name+contains+'report'&fields=files(id,name,mimeType,webViewLink)"
```

### Read a Google Doc as text

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/{fileId}/export?mimeType=text/plain"
```

### Read a Google Sheet as CSV

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/drive/v3/files/{fileId}/export?mimeType=text/csv"
```

## API References

For full endpoint details, read the relevant reference file:

- **Gmail**: [references/gmail-api.md](references/gmail-api.md) — messages, labels, search operators, send/reply
- **Calendar**: [references/calendar-api.md](references/calendar-api.md) — events, invites, free/busy
- **Drive / Docs / Sheets / Slides**: [references/drive-api.md](references/drive-api.md) — files, export, read/write content

## Important Notes

- Always use `me` as the userId for Gmail (service account impersonates the user).
- Use `primary` as calendarId for the main calendar.
- For Gmail send: the `raw` field must be base64url-encoded (no padding, `+` → `-`, `/` → `_`).
- Calendar datetimes must include timezone offset or use UTC (`Z`).
- When listing messages, the response only contains IDs — fetch each message separately for content.
- Prefer `format=metadata` with `metadataHeaders=From,To,Subject,Date` when you only need headers.
- For Drive, Google-native files (Docs/Sheets/Slides) must use `/export`; binary files use `?alt=media`.
