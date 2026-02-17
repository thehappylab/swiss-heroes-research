# Gmail API Reference

Base URL: `https://gmail.googleapis.com/gmail/v1/users/{userId}`

Use `me` as userId when impersonating via service account.

## Common Headers

```
Authorization: Bearer {TOKEN}
Content-Type: application/json
```

## Endpoints

### List messages

```
GET /users/me/messages?q={query}&maxResults={n}
```

Query syntax follows Gmail search (e.g. `is:unread`, `from:x@y.com`, `subject:hello`, `newer_than:1d`).

Response: `{ messages: [{ id, threadId }], nextPageToken }` — IDs only, need separate GET for content.

### Get message

```
GET /users/me/messages/{id}?format=full
```

Formats: `minimal`, `full`, `raw`, `metadata`.

Key fields in response:
- `payload.headers[]` — From, To, Subject, Date
- `payload.parts[]` — body parts (check mimeType)
- `snippet` — short preview text
- `labelIds[]` — INBOX, UNREAD, SENT, etc.

To decode body: base64url decode `payload.body.data` or `payload.parts[].body.data`.

### Send message

```
POST /users/me/messages/send
Body: { "raw": "<base64url-encoded-RFC2822>" }
```

Build RFC2822:
```
From: hello@thehappylab.com
To: recipient@example.com
Subject: Your subject
Content-Type: text/plain; charset="UTF-8"

Body text here.
```

Then base64url-encode the entire string.

### Reply to message

Same as send, but include `In-Reply-To` and `References` headers with the original Message-ID, and set `threadId` in the JSON body.

### Modify labels

```
POST /users/me/messages/{id}/modify
Body: { "addLabelIds": ["STARRED"], "removeLabelIds": ["UNREAD"] }
```

### Trash / Untrash

```
POST /users/me/messages/{id}/trash
POST /users/me/messages/{id}/untrash
```

### List labels

```
GET /users/me/labels
```

### Batch operations

```
POST /users/me/messages/batchModify
Body: { "ids": ["id1","id2"], "addLabelIds": [...], "removeLabelIds": [...] }
```

## Common Gmail Search Operators

| Operator | Example |
|---|---|
| `is:unread` | Unread messages |
| `is:starred` | Starred messages |
| `from:` | `from:user@example.com` |
| `to:` | `to:user@example.com` |
| `subject:` | `subject:invoice` |
| `has:attachment` | Messages with attachments |
| `newer_than:` | `newer_than:2d` (2 days) |
| `older_than:` | `older_than:1w` (1 week) |
| `after:` / `before:` | `after:2024/01/01` |
| `label:` | `label:important` |
| `filename:` | `filename:pdf` |
