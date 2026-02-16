# Development Guide

## Setting Up Your Development Environment

### Prerequisites

1. **Python 3.11+**
   ```bash
   python --version
   ```

2. **Node.js 18+**
   ```bash
   node --version
   npm --version
   ```

3. **Git**
   ```bash
   git --version
   ```

4. **OpenAI API Key**
   - Sign up at https://platform.openai.com/
   - Generate an API key
   - Keep it secure

---

## Backend Development

### Initial Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Backend

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Project Structure

```
backend/
├── app/
│   ├── api/           # API route handlers
│   ├── core/          # Configuration and settings
│   ├── models/        # Pydantic models
│   ├── services/      # Business logic
│   └── main.py        # Application entry point
└── tests/             # Test suite
```

### Adding New Endpoints

1. **Create route file** in `app/api/`
2. **Define Pydantic models** in `app/models/schemas.py`
3. **Implement business logic** in `app/services/`
4. **Register router** in `app/main.py`

Example:
```python
# app/api/my_endpoint.py
from fastapi import APIRouter
from app.models.schemas import MyRequest, MyResponse

router = APIRouter()

@router.post("/my-endpoint", response_model=MyResponse)
async def my_endpoint(request: MyRequest):
    return MyResponse(data="result")
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::TestHealthEndpoint::test_health_check
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

---

## Frontend Development

### Initial Setup

```bash
cd frontend

# Install dependencies
npm install
```

### Running the Frontend

```bash
# Development mode with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Project Structure

```
frontend/
├── src/
│   ├── components/    # React components
│   ├── services/      # API client
│   ├── styles/        # CSS styles
│   ├── App.jsx        # Main component
│   └── main.jsx       # Entry point
└── public/            # Static assets
```

### Adding New Components

1. **Create component file** in `src/components/`
2. **Import and use** in parent component

Example:
```jsx
// src/components/MyComponent.jsx
import React from 'react';

function MyComponent({ data }) {
  return (
    <div className="my-component">
      <h2>{data.title}</h2>
      <p>{data.description}</p>
    </div>
  );
}

export default MyComponent;
```

### Styling

- CSS modules in `src/styles/`
- Global styles in `src/styles/index.css`
- Component-specific styles in `src/styles/App.css`

### API Integration

Use the API service:
```javascript
import { sendMessage, uploadDocument } from './services/api';

// In your component
const response = await sendMessage('Hello');
```

---

## Environment Configuration

### Backend (.env)

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional
ENVIRONMENT=development
DEBUG=true
LLM_TEMPERATURE=0.7
CHUNK_SIZE=1000
```

### Frontend (vite.config.js)

```javascript
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

---

## Database Management

### Vector Store

The project uses FAISS for vector storage:

```python
# Location
data/vectors/faiss_index/

# Reset vector store
rm -rf data/vectors/faiss_index/
# Restart backend to recreate
```

### Document Storage

```python
# Location
data/uploads/

# Format: {document_id}_{filename}
# Example: abc123def456_mydoc.pdf
```

---

## Debugging

### Backend Debugging

1. **Enable debug logging**
   ```python
   # In app/main.py
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Use debugger**
   ```python
   import pdb; pdb.set_trace()
   ```

3. **View logs**
   ```bash
   # Backend logs show in terminal
   tail -f backend.log
   ```

### Frontend Debugging

1. **Browser DevTools**
   - Open with F12
   - Check Console for errors
   - Use Network tab for API calls

2. **React DevTools**
   - Install browser extension
   - Inspect component tree

3. **Add debugging**
   ```javascript
   console.log('Debug:', data);
   debugger;  // Pause execution
   ```

---

## Common Development Tasks

### Add Python Dependency

```bash
pip install package-name
pip freeze > requirements.txt
```

### Add Node Dependency

```bash
npm install package-name
# or for dev dependencies
npm install --save-dev package-name
```

### Update Documentation

1. Edit markdown files in `docs/`
2. Update README.md if needed
3. Regenerate API docs (automatic via FastAPI)

### Create Migration

For database migrations (future):
```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

---

## Performance Tips

### Backend

1. **Use async/await** for I/O operations
2. **Cache embeddings** when possible
3. **Batch document processing**
4. **Use connection pooling**

### Frontend

1. **Use React.memo** for expensive components
2. **Implement virtual scrolling** for long lists
3. **Lazy load** components
4. **Optimize images**

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Module Not Found

```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### CORS Issues

Check `backend/app/core/config.py`:
```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    # Add your frontend URL
]
```

---

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add my feature"

# Push to remote
git push origin feature/my-feature

# Create pull request on GitHub
```

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## Best Practices

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: Use ES6+ features
- **React**: Functional components with hooks
- **CSS**: Use BEM naming convention

### Documentation

- Document all public APIs
- Add docstrings to functions
- Keep README up to date
- Comment complex logic

### Testing

- Write tests for new features
- Maintain >80% coverage
- Test edge cases
- Mock external dependencies

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
