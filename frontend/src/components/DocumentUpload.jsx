import React, { useState, useEffect } from 'react';
import { Upload, File, Trash2, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { uploadDocument, getDocuments, deleteDocument } from '../services/api';

function DocumentUpload({ documents, onDocumentUploaded }) {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(null);
  const [error, setError] = useState(null);
  const [documentList, setDocumentList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const response = await getDocuments();
      setDocumentList(response.documents);
    } catch (err) {
      console.error('Error loading documents:', err);
      setError('Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate file type
    const validTypes = ['.pdf', '.txt', '.docx', '.doc'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(fileExt)) {
      setError(`Invalid file type. Supported: ${validTypes.join(', ')}`);
      return;
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File too large. Maximum size: 10MB');
      return;
    }

    setUploading(true);
    setError(null);
    setUploadProgress({
      filename: file.name,
      status: 'uploading'
    });

    try {
      const response = await uploadDocument(file);
      
      setUploadProgress({
        filename: file.name,
        status: 'success',
        message: response.message
      });

      onDocumentUploaded(response);
      
      // Reload document list
      await loadDocuments();

      // Clear success message after 3 seconds
      setTimeout(() => {
        setUploadProgress(null);
      }, 3000);

    } catch (err) {
      console.error('Error uploading document:', err);
      setError(err.response?.data?.detail || 'Failed to upload document');
      setUploadProgress({
        filename: file.name,
        status: 'error'
      });
    } finally {
      setUploading(false);
      e.target.value = ''; // Reset file input
    }
  };

  const handleDelete = async (documentId, filename) => {
    if (!confirm(`Delete "${filename}"?`)) return;

    try {
      await deleteDocument(documentId);
      await loadDocuments();
    } catch (err) {
      console.error('Error deleting document:', err);
      setError('Failed to delete document');
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="document-upload">
      <div className="upload-section">
        <h2>📤 Upload Documents</h2>
        <p className="upload-description">
          Upload PDF, TXT, or DOCX files to chat with your documents
        </p>

        <label className="upload-button">
          <Upload size={24} />
          <span>{uploading ? 'Uploading...' : 'Choose File'}</span>
          <input
            type="file"
            onChange={handleFileUpload}
            disabled={uploading}
            accept=".pdf,.txt,.docx,.doc"
            style={{ display: 'none' }}
          />
        </label>

        {uploadProgress && (
          <div className={`upload-status ${uploadProgress.status}`}>
            {uploadProgress.status === 'uploading' && <Loader className="spinner" size={20} />}
            {uploadProgress.status === 'success' && <CheckCircle size={20} />}
            {uploadProgress.status === 'error' && <AlertCircle size={20} />}
            <span>{uploadProgress.filename}</span>
            {uploadProgress.message && <small>{uploadProgress.message}</small>}
          </div>
        )}

        {error && (
          <div className="error-message">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}
      </div>

      <div className="documents-section">
        <h2>📚 Uploaded Documents</h2>
        
        {loading ? (
          <div className="loading-state">
            <Loader className="spinner" size={32} />
            <p>Loading documents...</p>
          </div>
        ) : documentList.length === 0 ? (
          <div className="empty-documents">
            <File size={48} />
            <p>No documents uploaded yet</p>
          </div>
        ) : (
          <div className="documents-list">
            {documentList.map((doc) => (
              <div key={doc.document_id} className="document-item">
                <div className="document-icon">
                  <File size={24} />
                </div>
                <div className="document-info">
                  <h3>{doc.filename}</h3>
                  <div className="document-meta">
                    <span>{formatFileSize(doc.file_size)}</span>
                    <span>•</span>
                    <span>{new Date(doc.upload_date).toLocaleDateString()}</span>
                    {doc.chunks_count && (
                      <>
                        <span>•</span>
                        <span>{doc.chunks_count} chunks</span>
                      </>
                    )}
                  </div>
                </div>
                <button
                  className="delete-button"
                  onClick={() => handleDelete(doc.document_id, doc.filename)}
                  title="Delete document"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default DocumentUpload;
