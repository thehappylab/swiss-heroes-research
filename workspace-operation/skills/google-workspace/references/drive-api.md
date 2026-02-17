# Google Drive & Docs/Sheets/Slides API Reference

## Drive API

Base URL: `https://www.googleapis.com/drive/v3`

### List / search files

```
GET /files?q={query}&fields=files(id,name,mimeType,modifiedTime,webViewLink)&pageSize=20
```

Query syntax:
- `name = 'filename'` or `name contains 'keyword'`
- `mimeType = 'application/vnd.google-apps.spreadsheet'`
- `'folderId' in parents` — files in a folder
- `modifiedTime > '2024-01-01'`
- `trashed = false`
- Combine with `and` / `or`

Common MIME types:
| Type | MIME |
|---|---|
| Folder | `application/vnd.google-apps.folder` |
| Document | `application/vnd.google-apps.document` |
| Spreadsheet | `application/vnd.google-apps.spreadsheet` |
| Presentation | `application/vnd.google-apps.presentation` |
| PDF | `application/pdf` |

### Get file metadata

```
GET /files/{fileId}?fields=id,name,mimeType,modifiedTime,webViewLink,owners,permissions
```

### Download / export

Native Google files must be exported:
```
GET /files/{fileId}/export?mimeType=text/plain          (Docs → text)
GET /files/{fileId}/export?mimeType=text/csv             (Sheets → CSV)
GET /files/{fileId}/export?mimeType=application/pdf      (any → PDF)
```

Binary files (PDFs, images) use:
```
GET /files/{fileId}?alt=media
```

### Create file

```
POST /files
Body: { "name": "New Doc", "mimeType": "application/vnd.google-apps.document", "parents": ["folderId"] }
```

### Upload content

Use multipart upload for files with content:
```
POST /upload/drive/v3/files?uploadType=multipart
```

### Move / rename

```
PATCH /files/{fileId}?addParents={newFolder}&removeParents={oldFolder}
Body: { "name": "New Name" }
```

### Delete

```
DELETE /files/{fileId}
```

Or trash: `PATCH /files/{fileId}  Body: { "trashed": true }`

---

## Google Docs API

Base URL: `https://docs.googleapis.com/v1/documents`

### Get document content

```
GET /documents/{documentId}
```

Returns structured JSON with `body.content[]` — paragraphs, tables, lists, etc.

For simple text extraction, prefer Drive export to `text/plain`.

### Update document

```
POST /documents/{documentId}:batchUpdate
Body: {
  "requests": [
    { "insertText": { "location": { "index": 1 }, "text": "Hello world" } }
  ]
}
```

Common request types: `insertText`, `deleteContentRange`, `replaceAllText`, `insertTable`, `updateTextStyle`.

---

## Google Sheets API

Base URL: `https://sheets.googleapis.com/v4/spreadsheets`

### Read values

```
GET /spreadsheets/{spreadsheetId}/values/{range}
```

Range format: `Sheet1!A1:D10` or `Sheet1` (entire sheet).

### Write values

```
PUT /spreadsheets/{spreadsheetId}/values/{range}?valueInputOption=USER_ENTERED
Body: { "values": [["A1","B1"],["A2","B2"]] }
```

### Append rows

```
POST /spreadsheets/{spreadsheetId}/values/{range}:append?valueInputOption=USER_ENTERED
Body: { "values": [["new","row"]] }
```

### Get spreadsheet metadata

```
GET /spreadsheets/{spreadsheetId}?fields=sheets.properties
```

Returns sheet names, IDs, row/column counts.

---

## Google Slides API

Base URL: `https://slides.googleapis.com/v1/presentations`

### Get presentation

```
GET /presentations/{presentationId}
```

Returns slides with elements (shapes, text, images, tables).

### Update presentation

```
POST /presentations/{presentationId}:batchUpdate
Body: { "requests": [...] }
```

Common requests: `createSlide`, `insertText`, `replaceAllText`, `deleteObject`, `createImage`.

For reading slide content as text, prefer iterating `slides[].pageElements[].shape.text.textElements[].textRun.content`.
