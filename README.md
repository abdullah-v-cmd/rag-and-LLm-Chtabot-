# RAG Chatbot — LangChain + FAISS

A foundational Retrieval-Augmented Generation (RAG) chatbot that loads documents, creates semantic embeddings, retrieves relevant context, and generates grounded answers with an LLM.

## ✨ Pipeline
`Document → Chunking → Embeddings → FAISS → Retrieval → LLM → Answer`

## 🛠️ Stack
- Python
- LangChain
- Hugging Face Sentence Transformers
- FAISS
- OpenAI-compatible chat model
- PyPDF

## 🚀 Setup

```bash
git clone https://github.com/abdullah-v-cmd/rag-and-LLm-Chtabot-.git
cd rag-and-LLm-Chtabot-
pip install langchain langchain-community langchain-openai sentence-transformers faiss-cpu pypdf
```

Configure your model API key, then run the main Python application in the repository.

## 🎯 Learning Outcomes
- Document ingestion and chunking
- Semantic embeddings
- Vector similarity search
- Retrieval-augmented prompting
- Source-grounded LLM responses

## 🔮 Next Steps
- Hybrid search
- Reranking
- Conversation memory
- Multi-document ingestion
- FastAPI deployment

## 👤 Author
**Abdullah Naveed**

## 📄 License
Educational project.
