#!/usr/bin/env python3
"""
FastAPI Backend for SecureDoc AI Platform
"""
from datetime import datetime, timedelta  # Add this import
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.auth.authentication import auth_system, User, Token, UserInDB
from src.data_ingestion.storage_client import AzureStorageClient
from src.data_processing.document_processor import DocumentProcessor
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="SecureDoc AI API",
    description="Document Intelligence Platform Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = auth_system.verify_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Initialize services
storage_client = AzureStorageClient()
doc_processor = DocumentProcessor()

# Authentication endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_system.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_system.access_token_expire_minutes)
    access_token = auth_system.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Document processing endpoints
@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload and process a document"""
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Upload to Azure Storage
        blob_url = storage_client.upload_file(temp_path, file.filename)
        
        # Generate SAS URL for processing
        sas_url = storage_client.generate_sas_url(file.filename)
        
        # Process with AI
        analysis_result = doc_processor.analyze_document(sas_url)
        
        # Clean up temp file
        os.remove(temp_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "blob_url": blob_url,
            "analysis": {
                "pages_processed": len(analysis_result['pages']),
                "tables_found": len(analysis_result['tables']),
                "content_preview": analysis_result['content'][:200] + "..." if len(analysis_result['content']) > 200 else analysis_result['content'],
                "processing_time": "completed"
            },
            "user": current_user.username
        }
        
    except Exception as e:
        logger.error(f"Document processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/documents/list")
async def list_documents(current_user: User = Depends(get_current_active_user)):
    """List all documents in storage"""
    try:
        blobs = storage_client.list_blobs()
        documents = []
        for blob in blobs:
            documents.append({
                "name": blob.name,
                "size_mb": round(blob.size / (1024 * 1024), 2),
                "last_modified": blob.last_modified.isoformat() if blob.last_modified else None
            })
        return {
            "status": "success",
            "documents": documents,
            "total_count": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")

@app.get("/documents/analyze/{document_name}")
async def analyze_document(
    document_name: str,
    current_user: User = Depends(get_current_active_user)
):
    """Analyze a specific document"""
    try:
        sas_url = storage_client.generate_sas_url(document_name)
        analysis_result = doc_processor.analyze_document(sas_url)
        
        return {
            "status": "success",
            "document": document_name,
            "analysis": analysis_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# System monitoring endpoints
@app.get("/system/health")
async def system_health():
    """Check system health"""
    try:
        storage_healthy = storage_client.test_connection()
        ai_healthy = doc_processor.test_connection()
        
        return {
            "status": "healthy" if storage_healthy and ai_healthy else "degraded",
            "services": {
                "azure_storage": "healthy" if storage_healthy else "unhealthy",
                "document_intelligence": "healthy" if ai_healthy else "unhealthy"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

@app.get("/system/metrics")
async def system_metrics(current_user: User = Depends(get_current_active_user)):
    """Get system metrics"""
    try:
        blobs = storage_client.list_blobs()
        total_size = sum(blob.size for blob in blobs)
        
        return {
            "storage_metrics": {
                "total_documents": len(blobs),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "file_types": {}
            },
            "user_metrics": {
                "active_user": current_user.username,
                "role": "admin" if current_user.username == "admin" else "user"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to SecureDoc AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)