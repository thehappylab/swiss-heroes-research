# Google Calendar API Reference

Base URL: `https://www.googleapis.com/calendar/v3`

## Common Headers

```
Authorization: Bearer {TOKEN}
Content-Type: application/json
```

## Endpoints

### List calendars

```
GET /users/me/calendarList
```

### List events

```
GET /calendars/{calendarId}/events?timeMin={ISO}&timeMax={ISO}&singleEvents=true&orderBy=startTime
```

Use `primary` as calendarId for the user's main calendar.
Always set `singleEvents=true` to expand recurring events.

Key query params:
- `timeMin` / `timeMax` — ISO 8601 datetime with timezone (e.g. `2024-01-01T00:00:00Z`)
- `maxResults` — limit results
- `q` — free text search
- `pageToken` — pagination

### Get event

```
GET /calendars/{calendarId}/events/{eventId}
```

Key response fields:
- `summary` — title
- `start.dateTime` / `start.date` — start (dateTime for timed, date for all-day)
- `end.dateTime` / `end.date`
- `attendees[]` — `{ email, responseStatus, displayName }`
- `location`, `description`, `hangoutLink`
- `status` — confirmed, tentative, cancelled
- `organizer` — `{ email, displayName }`

### Create event

```
POST /calendars/primary/events
Body: {
  "summary": "Meeting title",
  "start": { "dateTime": "2024-06-01T10:00:00+02:00" },
  "end":   { "dateTime": "2024-06-01T11:00:00+02:00" },
  "attendees": [
    { "email": "person@example.com" }
  ],
  "description": "Optional notes",
  "location": "Office / Zoom link"
}
```

Add `sendUpdates=all` query param to send invitation emails.

### Update event

```
PATCH /calendars/{calendarId}/events/{eventId}?sendUpdates=all
Body: { fields to update }
```

### Delete event

```
DELETE /calendars/{calendarId}/events/{eventId}?sendUpdates=all
```

### Respond to invite (accept/decline/tentative)

```
PATCH /calendars/primary/events/{eventId}
Body: {
  "attendees": [
    { "email": "hello@thehappylab.com", "responseStatus": "accepted" }
  ]
}
```

responseStatus values: `accepted`, `declined`, `tentative`, `needsAction`.

### Free/busy query

```
POST /freeBusy
Body: {
  "timeMin": "...",
  "timeMax": "...",
  "items": [{ "id": "hello@thehappylab.com" }]
}
```
