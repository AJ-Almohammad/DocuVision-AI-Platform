#!/usr/bin/env python3
"""
Simplified FastAPI Backend for SecureDoc AI Platform
"""
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.auth.simple_auth import auth_system, User, Token, UserInDB
from src.data_ingestion.storage_client import AzureStorageClient
from src.data_processing.document_processor import DocumentProcessor
import logging

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

# CRITICAL: Ultra-simple health check MUST be first endpoint
# Azure startup probe needs instant response with ZERO dependencies
# This endpoint has no auth, no Azure services, no logging - just returns JSON
@app.get("/health")
async def health_check():
    """Immediate health check with zero dependencies for Azure startup probe"""
    return {"status": "healthy"}

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

# # ISSUE: Initializing Azure clients at module import time blocks startup
# # This causes Azure health probes to timeout before the app can respond
# try:
#     storage_client = AzureStorageClient()
#     doc_processor = DocumentProcessor()
#     services_available = True
# except Exception as e:
#     logger.warning(f"Azure services not available: {e}")
#     services_available = False

# FIXED: Use lazy initialization - clients are created only when first needed
# This prevents blocking the app startup
_storage_client = None
_doc_processor = None
_services_available = None

def get_storage_client():
    """Lazy initialization of storage client"""
    global _storage_client, _services_available
    if _storage_client is None:
        try:
            _storage_client = AzureStorageClient()
            _services_available = True
        except Exception as e:
            logger.warning(f"Azure Storage not available: {e}")
            _services_available = False
    return _storage_client

def get_doc_processor():
    """Lazy initialization of document processor"""
    global _doc_processor, _services_available
    if _doc_processor is None:
        try:
            _doc_processor = DocumentProcessor()
            _services_available = True
        except Exception as e:
            logger.warning(f"Document Processor not available: {e}")
            _services_available = False
    return _doc_processor

def are_services_available():
    """Check if Azure services are available"""
    global _services_available
    if _services_available is None:
        # Try to initialize to check availability
        get_storage_client()
        get_doc_processor()
    return _services_available if _services_available is not None else False

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

@app.get("/users")
async def get_all_users(current_user: User = Depends(get_current_active_user)):
    """Get list of all users (admin only)"""
    if current_user.username != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    users = []
    for username, user_data in auth_system.fake_users_db.items():
        users.append({
            "username": user_data["username"],
            "email": user_data["email"],
            "full_name": user_data["full_name"]
        })
    return {"users": users}

# Document processing endpoints
@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload and process a document"""
    # FIXED: Check services availability lazily
    if not are_services_available():
        raise HTTPException(status_code=503, detail="Azure services not configured")
    
    try:
        # FIXED: Get clients lazily
        storage_client = get_storage_client()
        doc_processor = get_doc_processor()
        
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
    # FIXED: Check services availability lazily
    if not are_services_available():
        return {
            "status": "success",
            "documents": [],
            "total_count": 0,
            "message": "Azure services not configured - demo mode"
        }
    
    try:
        # FIXED: Get client lazily
        storage_client = get_storage_client()
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

# System monitoring endpoints
@app.get("/system/health")
async def system_health():
    """Check system health with Azure service status"""
    try:
        # FIXED: Get clients lazily and handle None case
        storage_client = get_storage_client()
        doc_processor = get_doc_processor()
        services_available = are_services_available()
        
        storage_healthy = storage_client.test_connection() if storage_client and services_available else False
        ai_healthy = doc_processor.test_connection() if doc_processor and services_available else False
        
        return {
            "status": "healthy" if (storage_healthy and ai_healthy) or not services_available else "degraded",
            "services": {
                "azure_storage": "healthy" if storage_healthy else "unavailable",
                "document_intelligence": "healthy" if ai_healthy else "unavailable",
                "authentication": "healthy"
            },
            "mode": "demo" if not services_available else "production",
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
        # FIXED: Check and get services lazily
        if are_services_available():
            storage_client = get_storage_client()
            blobs = storage_client.list_blobs()
            total_size = sum(blob.size for blob in blobs)
            storage_info = {
                "total_documents": len(blobs),
                "total_size_mb": round(total_size / (1024 * 1024), 2),
            }
        else:
            storage_info = {
                "total_documents": 0,
                "total_size_mb": 0,
                "message": "Demo mode - Azure services not configured"
            }
        
        return {
            "storage_metrics": storage_info,
            "user_metrics": {
                "active_user": current_user.username,
                "role": "admin" if current_user.username == "admin" else "user",
                "login_time": datetime.utcnow().isoformat()
            },
            "system": {
                "users_count": len(auth_system.fake_users_db),
                "api_version": "1.0.0"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

# Demo endpoints (work without Azure)
@app.get("/demo/documents")
async def get_demo_documents(current_user: User = Depends(get_current_active_user)):
    """Get demo documents list"""
    demo_docs = [
        {"name": "sample_technical_report.pdf", "size_mb": 2.1, "type": "PDF"},
        {"name": "professional_technical_report.pdf", "size_mb": 4.5, "type": "PDF"},
        {"name": "compliance_certificate.pdf", "size_mb": 1.8, "type": "PDF"}
    ]
    return {
        "status": "success",
        "documents": demo_docs,
        "message": "Demo data - Azure services not required"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to SecureDoc AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational",
        "authentication": "JWT Bearer Token",
        "demo_users": [
            {"username": "amer", "password": "demo123", "role": "user"},
            {"username": "admin", "password": "admin123", "role": "admin"},
            {"username": "viewer", "password": "view123", "role": "viewer"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)