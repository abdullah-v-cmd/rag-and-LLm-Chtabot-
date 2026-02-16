"""
Document management API endpoints.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import hashlib
import logging
from datetime import datetime
from typing import List

from app.models.schemas import DocumentUploadResponse, DocumentListResponse, DocumentInfo
from app.services.rag_service import rag_service
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Supported file types
SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.doc'}


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document for RAG.
    
    Supported formats: PDF, TXT, DOCX, DOC
    Max file size: 10MB
    """
    try:
        # Validate file extension
        file_path = Path(file.filename)
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
            )
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Validate file size
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / (1024*1024):.1f}MB"
            )
        
        # Generate document ID
        document_id = hashlib.sha256(
            f"{file.filename}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # Save file
        save_path = settings.UPLOAD_DIR / f"{document_id}_{file.filename}"
        with open(save_path, 'wb') as f:
            f.write(content)
        
        logger.info(f"Saved document: {save_path}")
        
        # Process document with RAG
        result = rag_service.process_document(save_path, document_id)
        
        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename,
            file_size=file_size,
            processed=result['success'],
            chunks_created=result.get('chunks_created'),
            message="Document uploaded and processed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("", response_model=DocumentListResponse)
async def list_documents():
    """List all uploaded documents."""
    try:
        documents = []
        upload_dir = settings.UPLOAD_DIR
        
        for file_path in upload_dir.glob("*"):
            if file_path.is_file():
                # Extract document ID from filename
                filename_parts = file_path.name.split('_', 1)
                document_id = filename_parts[0] if len(filename_parts) > 1 else "unknown"
                original_name = filename_parts[1] if len(filename_parts) > 1 else file_path.name
                
                stat = file_path.stat()
                documents.append(DocumentInfo(
                    document_id=document_id,
                    filename=original_name,
                    file_size=stat.st_size,
                    upload_date=datetime.fromtimestamp(stat.st_ctime),
                    processed=True
                ))
        
        return DocumentListResponse(
            documents=sorted(documents, key=lambda x: x.upload_date, reverse=True),
            total=len(documents)
        )
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving document list")


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document by ID."""
    try:
        upload_dir = settings.UPLOAD_DIR
        deleted = False
        
        for file_path in upload_dir.glob(f"{document_id}_*"):
            file_path.unlink()
            deleted = True
            logger.info(f"Deleted document: {file_path}")
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {"message": "Document deleted successfully", "document_id": document_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Error deleting document")
