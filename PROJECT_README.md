# 🤖 End-to-End LLM RAG Chatbot

A production-ready **Retrieval-Augmented Generation (RAG)** chatbot system built with modern technologies. This project demonstrates a complete end-to-end implementation of an intelligent document question-answering system.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎯 Core Capabilities
- **📄 Multi-Format Document Support** - Upload PDF, TXT, DOCX, DOC files
- **💬 Conversational AI** - Natural language question answering
- **🔍 Smart Retrieval** - Vector-based semantic search with FAISS
- **📚 Source Citations** - View source documents for each answer
- **🎨 Modern UI** - Clean, responsive React interface
- **🐳 Docker Ready** - Full containerization support
- **🧪 Tested** - Comprehensive unit and integration tests

### 🏗️ Architecture Highlights
- **Backend**: FastAPI with async support
- **Frontend**: React with Vite
- **Vector DB**: FAISS for efficient similarity search
- **Embeddings**: HuggingFace sentence-transformers
- **LLM**: OpenAI GPT-3.5 Turbo
- **Framework**: LangChain for RAG orchestration

---

## 📁 Project Structure

```
webapp/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   ├── chat.py        # Chat endpoints
│   │   │   ├── documents.py   # Document management
│   │   │   └── health.py      # Health checks
│   │   ├── core/              # Core configuration
│   │   │   └── config.py      # Settings management
│   │   ├── models/            # Pydantic models
│   │   │   └── schemas.py     # Request/response schemas
│   │   ├── services/          # Business logic
│   │   │   └── rag_service.py # RAG implementation
│   │   └── main.py            # App entry point
│   ├── tests/                 # Unit tests
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Backend container
│
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── DocumentUpload.jsx
│   │   │   └── Header.jsx
│   │   ├── services/         # API client
│   │   │   └── api.js
│   │   ├── styles/           # CSS styles
│   │   ├── App.jsx           # Main app component
│   │   └── main.jsx          # Entry point
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   └── Dockerfile            # Frontend container
│
├── data/                      # Data storage
│   ├── uploads/              # Uploaded documents
│   └── vectors/              # Vector database
│
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
│   ├── dev.sh                # Development startup
│   └── deploy.sh             # Production deployment
│
├── docker-compose.yml         # Docker orchestration
├── .env.example              # Environment template
└── README.md                 # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Docker** (optional, for containerized deployment)

### Option 1: Development Setup

1. **Clone and navigate to project**
   ```bash
   cd /home/user/webapp
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Start backend**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Start frontend** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

### Option 2: Docker Deployment

1. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Option 3: Quick Start Script

```bash
chmod +x scripts/dev.sh
./scripts/dev.sh
```

---

## 📖 Usage Guide

### 1. Upload Documents

1. Navigate to the **Documents** tab
2. Click **Choose File**
3. Select a PDF, TXT, or DOCX file (max 10MB)
4. Wait for processing to complete

### 2. Chat with Your Documents

1. Switch to the **Chat** tab
2. Type your question in the input field
3. Press Enter or click Send
4. View the AI-generated answer with source citations

### 3. Example Questions

After uploading a document, try questions like:
- "What is the main topic of this document?"
- "Summarize the key points"
- "What does the document say about [specific topic]?"
- "Explain [concept] mentioned in the document"

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `EMBEDDING_MODEL` | HuggingFace embedding model | `all-MiniLM-L6-v2` |
| `LLM_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `LLM_TEMPERATURE` | LLM temperature (0-2) | `0.7` |
| `CHUNK_SIZE` | Text chunk size | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap | `200` |
| `TOP_K_RESULTS` | Top K retrieved chunks | `4` |
| `MAX_UPLOAD_SIZE` | Max file size (bytes) | `10485760` (10MB) |

### Customizing the RAG System

Edit `backend/app/core/config.py` to modify:
- Chunk size and overlap for text splitting
- Number of retrieved documents (Top K)
- LLM model and parameters
- Vector database configuration

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v --cov=app
```

### Test Coverage

```bash
pytest tests/ --cov=app --cov-report=html
# View coverage report in htmlcov/index.html
```

---

## 🏗️ Technical Architecture

### Backend Stack

- **FastAPI**: Modern async web framework
- **LangChain**: RAG orchestration framework
- **FAISS**: Vector similarity search
- **HuggingFace**: Embedding models
- **OpenAI**: GPT-3.5 Turbo for generation
- **Pydantic**: Data validation

### Frontend Stack

- **React 18**: UI framework
- **Vite**: Build tool
- **Axios**: HTTP client
- **React Markdown**: Markdown rendering
- **Lucide React**: Icon library

### RAG Pipeline

1. **Document Ingestion**
   - Upload → Parse → Split into chunks
   - Generate embeddings → Store in vector DB

2. **Query Processing**
   - User question → Generate embedding
   - Semantic search → Retrieve top K chunks
   - Construct prompt with context
   - LLM generates answer → Return with sources

---

## 📊 API Documentation

### Health Check
```http
GET /api/health
```

### Send Chat Message
```http
POST /api/chat
Content-Type: application/json

{
  "message": "What is this document about?",
  "conversation_id": "optional-id",
  "use_rag": true,
  "max_tokens": 500,
  "temperature": 0.7
}
```

### Upload Document
```http
POST /api/documents/upload
Content-Type: multipart/form-data

file: <binary>
```

### List Documents
```http
GET /api/documents
```

### Delete Document
```http
DELETE /api/documents/{document_id}
```

Full API documentation available at: http://localhost:8000/api/docs

---

## 🚢 Deployment

### Docker Production Deployment

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Production Deployment

1. **Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   # Serve the dist/ folder with nginx or similar
   ```

---

## 🔒 Security Considerations

- ✅ API key stored in environment variables
- ✅ File upload validation (type and size)
- ✅ CORS configuration
- ✅ Input sanitization
- ⚠️ Consider adding authentication for production
- ⚠️ Implement rate limiting for production use

---

## 🐛 Troubleshooting

### Common Issues

**"OPENAI_API_KEY not set"**
- Ensure .env file exists and contains valid API key
- Restart the backend server after setting the key

**"No documents processed yet"**
- Upload at least one document before chatting
- Check backend logs for processing errors

**Frontend can't connect to backend**
- Verify backend is running on port 8000
- Check CORS settings in backend/app/core/config.py

**Document upload fails**
- Ensure file size < 10MB
- Check file format (PDF, TXT, DOCX only)
- Verify sufficient disk space

---

## 🛣️ Roadmap

- [ ] Add conversation memory and history
- [ ] Support for multiple vector databases (Pinecone, Chroma)
- [ ] Local LLM support (LLaMA, Mistral)
- [ ] Multi-user authentication
- [ ] Advanced document management
- [ ] Export conversation history
- [ ] Support for more file formats
- [ ] Real-time streaming responses

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Abdullah Naveed**

---

## 🙏 Acknowledgments

- LangChain for RAG framework
- OpenAI for GPT models
- HuggingFace for embeddings
- FastAPI and React communities

---

## 📞 Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review [API Documentation](http://localhost:8000/api/docs)
3. Open an issue on GitHub

---

**Built with ❤️ using LangChain, FastAPI, and React**
