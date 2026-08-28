import React from 'react';
import { MessageSquare } from 'lucide-react';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <MessageSquare size={32} />
          <h1>LLM RAG Chatbot</h1>
        </div>
        <p className="subtitle">Intelligent Document Question Answering</p>
      </div>
    </header>
  );
}

export default Header;
