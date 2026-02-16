import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader, AlertCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { sendMessage } from '../services/api';

function ChatInterface({ documentsCount }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    if (documentsCount === 0) {
      setError('Please upload at least one document before chatting.');
      return;
    }

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await sendMessage(input);
      
      const assistantMessage = {
        role: 'assistant',
        content: response.message,
        sources: response.sources,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.response?.data?.detail || 'Failed to send message. Please try again.');
      
      // Remove user message if request failed
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <MessageSquare size={48} />
            <h3>Start a Conversation</h3>
            <p>Upload documents and ask questions about their content.</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
                {msg.sources && msg.sources.length > 0 && (
                  <details className="sources">
                    <summary>📚 Sources ({msg.sources.length})</summary>
                    <div className="sources-list">
                      {msg.sources.map((source, sidx) => (
                        <div key={sidx} className="source-item">
                          <p className="source-content">{source.content}</p>
                          <small className="source-meta">
                            {source.metadata.source} - Page {source.metadata.page || 'N/A'}
                          </small>
                        </div>
                      ))}
                    </div>
                  </details>
                )}
              </div>
              <span className="message-time">
                {msg.timestamp.toLocaleTimeString()}
              </span>
            </div>
          ))
        )}
        
        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <Loader className="spinner" size={20} />
              <span>Thinking...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="error-banner">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={documentsCount > 0 ? "Ask a question about your documents..." : "Upload documents first..."}
          className="message-input"
          disabled={loading || documentsCount === 0}
        />
        <button 
          type="submit" 
          className="send-button"
          disabled={loading || !input.trim() || documentsCount === 0}
        >
          <Send size={20} />
        </button>
      </form>
    </div>
  );
}

const MessageSquare = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
  </svg>
);

export default ChatInterface;
