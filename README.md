# rag-and-LLm-Chtabot-
# 📄 Simple RAG Chatbot using LangChain

This project demonstrates a **basic Retrieval-Augmented Generation (RAG) chatbot** built using **LangChain**, **FAISS**, **Hugging Face embeddings**, and **OpenAI GPT-3.5**. The chatbot can answer questions by retrieving relevant information from a **PDF document**.

---

## 🧠 What This Project Does

* Loads a PDF file
* Splits the document into smaller text chunks
* Converts text chunks into vector embeddings
* Stores embeddings in a FAISS vector database
* Uses an LLM (GPT-3.5) to answer questions based on retrieved content

This is a **foundational RAG implementation**, ideal for beginners learning how RAG works.

---

## 🛠️ Tech Stack

| Component       | Library                              |
| --------------- | ------------------------------------ |
| Language        | Python                               |
| Document Loader | langchain_community.document_loaders |
| Text Splitter   | RecursiveCharacterTextSplitter       |
| Embeddings      | HuggingFaceEmbeddings                |
| Vector Database | FAISS                                |
| LLM             | OpenAI GPT-3.5 Turbo                 |
| Framework       | LangChain                            |

---

## 📁 Project Files

```
project/
│
├── sodapdf-converted.pdf   # Input PDF document
├── rag_chatbot.py          # Main RAG code
├── faiss_index/            # Saved vector database
└── README.md
```

---

## ⚙️ Installation

Install required dependencies:

```bash
pip install langchain langchain-community langchain-openai
pip install sentence-transformers faiss-cpu pypdf
```

---

## 📥 How the Code Works

### 1️⃣ Load PDF Document

```python
loader = PyPDFLoader("D:/Rag and LLm/sodapdf-converted.pdf")
doc = loader.load()
```

Loads the PDF and converts it into LangChain documents.

---

### 2️⃣ Split Text into Chunks

```python
text = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=200
)
documents = text.split_documents(doc)
```

Splits the document into overlapping chunks to improve retrieval accuracy.

---

### 3️⃣ Create Embeddings

```python
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

Converts text chunks into numerical vectors for semantic search.

---

### 4️⃣ Store Vectors in FAISS

```python
db = FAISS.from_documents(documents, embedding)
db.save_local("faiss_index")
```

Stores embeddings locally for fast similarity search.

---

### 5️⃣ Initialize Language Model

```python
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0
)
```

Uses OpenAI GPT-3.5 for generating accurate answers.

---

### 6️⃣ Create RAG Chain

```python
retriever = db.as_retriever()

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)
```

Connects retrieval with the LLM.

---

### 7️⃣ Ask a Question

```python
query = "What is RAG chatbot?"
result = qa(query)
print("Answer:", result["result"])
```

The chatbot retrieves relevant content from the PDF and generates an answer.

---

## 🧪 Example Query

```
What is RAG chatbot?
```

**Output:**

* AI-generated answer based on PDF content
* Grounded in retrieved document chunks

---

## 🚀 Future Improvements

* Add conversation memory
* Support multiple PDFs
* Add FastAPI backend
* Add source citations in UI
* Switch to local LLaMA / Mistral

---

## ⚠️ Notes

* Make sure your OpenAI API key is set:

```bash
setx OPENAI_API_KEY "your_api_key"
```

* This project is for **learning purposes**.

---

## 👤 Author

*Abdullah Naveed**

---

## ⭐ License

MIT License
