"""
RAG (Retrieval-Augmented Generation) service for document processing and question answering.
"""
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
from datetime import datetime

from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from app.core.config import settings

logger = logging.getLogger(__name__)


class RAGService:
    """Service for handling RAG operations."""
    
    def __init__(self):
        """Initialize RAG service."""
        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize embeddings, vector store, and LLM."""
        try:
            # Initialize embeddings
            logger.info(f"Initializing embeddings with model: {settings.EMBEDDING_MODEL}")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            # Initialize LLM
            if settings.OPENAI_API_KEY:
                logger.info(f"Initializing LLM: {settings.LLM_MODEL}")
                self.llm = ChatOpenAI(
                    model_name=settings.LLM_MODEL,
                    temperature=settings.LLM_TEMPERATURE,
                    openai_api_key=settings.OPENAI_API_KEY
                )
            else:
                logger.warning("OPENAI_API_KEY not set. LLM functionality will be limited.")
            
            # Load existing vector store if available
            self._load_vector_store()
            
        except Exception as e:
            logger.error(f"Error initializing RAG components: {e}")
            raise
    
    def _load_vector_store(self):
        """Load existing vector store from disk."""
        vector_store_path = settings.VECTOR_DB_DIR / "faiss_index"
        if vector_store_path.exists():
            try:
                logger.info("Loading existing vector store...")
                self.vector_store = FAISS.load_local(
                    str(vector_store_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Vector store loaded successfully")
            except Exception as e:
                logger.warning(f"Could not load existing vector store: {e}")
                self.vector_store = None
    
    def _save_vector_store(self):
        """Save vector store to disk."""
        if self.vector_store:
            try:
                vector_store_path = settings.VECTOR_DB_DIR / "faiss_index"
                self.vector_store.save_local(str(vector_store_path))
                logger.info("Vector store saved successfully")
            except Exception as e:
                logger.error(f"Error saving vector store: {e}")
    
    def load_document(self, file_path: Path) -> List[Any]:
        """Load document based on file type."""
        suffix = file_path.suffix.lower()
        
        loaders = {
            '.pdf': PyPDFLoader,
            '.txt': TextLoader,
            '.docx': Docx2txtLoader,
            '.doc': Docx2txtLoader
        }
        
        loader_class = loaders.get(suffix)
        if not loader_class:
            raise ValueError(f"Unsupported file type: {suffix}")
        
        logger.info(f"Loading document: {file_path}")
        loader = loader_class(str(file_path))
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} pages/sections")
        
        return documents
    
    def process_document(self, file_path: Path, document_id: str) -> Dict[str, Any]:
        """Process a document and add to vector store."""
        try:
            # Load document
            documents = self.load_document(file_path)
            
            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
            )
            chunks = text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunks)} chunks from document")
            
            # Add metadata
            for chunk in chunks:
                chunk.metadata.update({
                    'document_id': document_id,
                    'source': file_path.name,
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            # Add to vector store
            if self.vector_store is None:
                logger.info("Creating new vector store")
                self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            else:
                logger.info("Adding to existing vector store")
                self.vector_store.add_documents(chunks)
            
            # Save vector store
            self._save_vector_store()
            
            return {
                'success': True,
                'chunks_created': len(chunks),
                'document_id': document_id
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise
    
    def query(
        self,
        question: str,
        conversation_id: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Query the RAG system with a question."""
        try:
            if not self.llm:
                raise ValueError("LLM not initialized. Please set OPENAI_API_KEY.")
            
            if not self.vector_store:
                raise ValueError("No documents have been processed yet.")
            
            # Create custom prompt
            prompt_template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            Context:
            {context}
            
            Question: {question}
            
            Answer:"""
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Create retrieval chain
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": settings.TOP_K_RESULTS}
            )
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT}
            )
            
            # Execute query
            result = qa_chain.invoke({"query": question})
            
            # Format sources
            sources = []
            for doc in result.get('source_documents', []):
                sources.append({
                    'content': doc.page_content[:200] + "...",
                    'metadata': doc.metadata
                })
            
            return {
                'answer': result['result'],
                'sources': sources,
                'conversation_id': conversation_id or self._generate_conversation_id()
            }
            
        except Exception as e:
            logger.error(f"Error during query: {e}")
            raise
    
    @staticmethod
    def _generate_conversation_id() -> str:
        """Generate a unique conversation ID."""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()


# Singleton instance
rag_service = RAGService()
