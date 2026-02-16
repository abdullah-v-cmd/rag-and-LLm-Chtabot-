# API Documentation

## Overview

The LLM RAG Chatbot API provides endpoints for document management and conversational AI with Retrieval-Augmented Generation.

**Base URL**: `http://localhost:8000/api`

**Interactive Docs**: `http://localhost:8000/api/docs`

---

## Authentication

Currently, the API does not require authentication. For production use, consider implementing:
- API keys
- OAuth 2.0
- JWT tokens

---

## Endpoints

### Health Check

**GET** `/health`

Check the health status of the API and its dependencies.

**Response**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "services": {
    "api": true,
    "embeddings": true,
    "vector_store": true,
    "llm": true
  }
}
```

---

### Chat

**POST** `/chat`

Send a message and receive an AI-generated response with RAG.

**Request Body**
```json
{
  "message": "What is this document about?",
  "conversation_id": "abc123",
  "use_rag": true,
  "max_tokens": 500,
  "temperature": 0.7
}
```

**Parameters**
- `message` (string, required): User's question
- `conversation_id` (string, optional): ID for conversation context
- `use_rag` (boolean, optional): Whether to use RAG (default: true)
- `max_tokens` (integer, optional): Max response tokens (50-2000, default: 500)
- `temperature` (float, optional): LLM temperature (0.0-2.0, default: 0.7)

**Response**
```json
{
  "message": "This document discusses...",
  "conversation_id": "abc123",
  "sources": [
    {
      "content": "Relevant text excerpt...",
      "metadata": {
        "document_id": "doc123",
        "source": "document.pdf",
        "page": 1
      }
    }
  ],
  "metadata": {
    "used_rag": true,
    "model": "gpt-3.5-turbo"
  }
}
```

**Error Responses**
- `400`: Invalid request (missing message, invalid parameters)
- `500`: Server error (LLM unavailable, no documents)

---

### Upload Document

**POST** `/documents/upload`

Upload a document for RAG processing.

**Request**
- Content-Type: `multipart/form-data`
- Body: `file` (binary)

**Supported Formats**
- PDF (.pdf)
- Text (.txt)
- Word (.docx, .doc)

**Constraints**
- Max file size: 10MB
- One file per request

**Response**
```json
{
  "document_id": "abc123def456",
  "filename": "example.pdf",
  "file_size": 1048576,
  "processed": true,
  "chunks_created": 42,
  "message": "Document uploaded and processed successfully"
}
```

**Error Responses**
- `400`: Invalid file type or size exceeded
- `500`: Processing error

---

### List Documents

**GET** `/documents`

Get a list of all uploaded documents.

**Response**
```json
{
  "documents": [
    {
      "document_id": "abc123",
      "filename": "example.pdf",
      "file_size": 1048576,
      "upload_date": "2024-01-15T10:30:00.000Z",
      "processed": true,
      "chunks_count": 42
    }
  ],
  "total": 1
}
```

---

### Delete Document

**DELETE** `/documents/{document_id}`

Delete a document by its ID.

**Path Parameters**
- `document_id` (string): Document identifier

**Response**
```json
{
  "message": "Document deleted successfully",
  "document_id": "abc123"
}
```

**Error Responses**
- `404`: Document not found
- `500`: Deletion error

---

## Error Handling

All error responses follow this format:

```json
{
  "detail": "Error message",
  "status": "error",
  "error_code": "SPECIFIC_ERROR_CODE"
}
```

**Common Error Codes**
- `INVALID_FILE_TYPE`: Unsupported file format
- `FILE_TOO_LARGE`: File exceeds size limit
- `NO_DOCUMENTS`: No documents available for RAG
- `LLM_UNAVAILABLE`: LLM service unavailable
- `INVALID_PARAMETERS`: Request parameters invalid

---

## Rate Limiting

Current implementation: **60 requests per minute**

Exceeded rate limits return:
- Status: `429 Too Many Requests`
- Body: `{"detail": "Rate limit exceeded"}`

---

## Examples

### Python

```python
import requests

API_BASE = "http://localhost:8000/api"

# Upload document
with open("document.pdf", "rb") as f:
    response = requests.post(
        f"{API_BASE}/documents/upload",
        files={"file": f}
    )
    print(response.json())

# Chat
response = requests.post(
    f"{API_BASE}/chat",
    json={
        "message": "What is the main topic?",
        "use_rag": True
    }
)
print(response.json())
```

### JavaScript

```javascript
// Upload document
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('/api/documents/upload', {
  method: 'POST',
  body: formData
});
const uploadData = await uploadResponse.json();

// Chat
const chatResponse = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'What is the main topic?',
    use_rag: true
  })
});
const chatData = await chatResponse.json();
```

### cURL

```bash
# Upload document
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@document.pdf"

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the main topic?",
    "use_rag": true
  }'
```

---

## WebSocket Support (Future)

Real-time streaming responses will be available via WebSocket in a future release:

```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws/chat');
ws.send(JSON.stringify({ message: 'Hello' }));
ws.onmessage = (event) => {
  console.log('Received:', event.data);
};
```
