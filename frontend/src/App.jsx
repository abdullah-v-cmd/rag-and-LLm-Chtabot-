import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import DocumentUpload from './components/DocumentUpload';
import Header from './components/Header';
import './styles/App.css';

function App() {
  const [documents, setDocuments] = useState([]);
  const [activeTab, setActiveTab] = useState('chat');

  const handleDocumentUploaded = (doc) => {
    setDocuments(prev => [doc, ...prev]);
  };

  return (
    <div className="app">
      <Header />
      
      <div className="container">
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            💬 Chat
          </button>
          <button 
            className={`tab ${activeTab === 'documents' ? 'active' : ''}`}
            onClick={() => setActiveTab('documents')}
          >
            📄 Documents
          </button>
        </div>

        <div className="content">
          {activeTab === 'chat' && (
            <ChatInterface documentsCount={documents.length} />
          )}
          
          {activeTab === 'documents' && (
            <DocumentUpload 
              documents={documents}
              onDocumentUploaded={handleDocumentUploaded}
            />
          )}
        </div>
      </div>

      <footer className="footer">
        <p>Powered by LangChain, FastAPI, and React | End-to-End LLM RAG System</p>
      </footer>
    </div>
  );
}

export default App;
