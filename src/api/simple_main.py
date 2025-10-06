#!/usr/bin/env python3
"""
Revised FastAPI Backend for SecureDoc AI Platform
"""
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import os, sys, logging

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.auth.simple_auth import auth_system, User, Token
from src.data_ingestion.storage_client import AzureStorageClient
from src.data_processing.document_processor import DocumentProcessor

# ----------------------------
# Logging configuration
# ----------------------------
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("securedoc-api")

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI(
    title="SecureDoc AI API",
    description="Document Intelligence Platform Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Minimal /ping endpoint
# ----------------------------
@app.get("/ping")
async def ping():
    """Simple test endpoint to check app is running"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# ----------------------------
# Health check (no dependencies)
# ----------------------------
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ----------------------------
# OAuth2 scheme
# ----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

# ----------------------------
# Lazy Azure clients
# ----------------------------
_storage_client = None
_doc_processor = None
_services_available = None

def get_storage_client():
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
    global _services_available
    if _services_available is None:
        get_storage_client()
        get_doc_processor()
    return _services_available if _services_available is not None else False

# ----------------------------
# Authentication endpoints
# ----------------------------
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

# ----------------------------
# Document endpoints (upload/list)
# ----------------------------
@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    if not are_services_available():
        raise HTTPException(status_code=503, detail="Azure services not configured")
    try:
        storage_client = get_storage_client()
        doc_processor = get_doc_processor()

        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        blob_url = storage_client.upload_file(temp_path, file.filename)
        sas_url = storage_client.generate_sas_url(file.filename)
        analysis_result = doc_processor.analyze_document(sas_url)

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
        logger.error(f"Document processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/documents/list")
async def list_documents(current_user: User = Depends(get_current_active_user)):
    if not are_services_available():
        return {"status": "success", "documents": [], "total_count": 0, "message": "Azure services not configured"}
    try:
        storage_client = get_storage_client()
        blobs = storage_client.list_blobs()
        documents = [{
            "name": b.name,
            "size_mb": round(b.size / (1024 * 1024), 2),
            "last_modified": b.last_modified.isoformat() if b.last_modified else None
        } for b in blobs]
        return {"status": "success", "documents": documents, "total_count": len(documents)}
    except Exception as e:
        logger.error(f"Listing documents failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")

# ----------------------------
# System health and metrics
# ----------------------------
@app.get("/system/health")
async def system_health():
    try:
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
        logger.error(f"System health check failed: {e}", exc_info=True)
        return {"status": "unhealthy", "error": str(e), "timestamp": datetime.utcnow().isoformat()}

@app.get("/system/metrics")
async def system_metrics(current_user: User = Depends(get_current_active_user)):
    try:
        if are_services_available():
            storage_client = get_storage_client()
            blobs = storage_client.list_blobs()
            total_size = sum(b.size for b in blobs)
            storage_info = {"total_documents": len(blobs), "total_size_mb": round(total_size / (1024*1024), 2)}
        else:
            storage_info = {"total_documents": 0, "total_size_mb": 0, "message": "Demo mode"}

        return {
            "storage_metrics": storage_info,
            "user_metrics": {"active_user": current_user.username, "role": "admin" if current_user.username=="admin" else "user", "login_time": datetime.utcnow().isoformat()},
            "system": {"users_count": len(auth_system.fake_users_db), "api_version": "1.0.0"}
        }
    except Exception as e:
        logger.error(f"Metrics endpoint failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

# ----------------------------
# Root endpoint
# ----------------------------
@app.get("/")
async def root():
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
