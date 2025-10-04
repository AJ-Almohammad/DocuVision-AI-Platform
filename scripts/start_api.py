#!/usr/bin/env python3
"""
Startup script for SecureDoc AI FastAPI
"""
import uvicorn
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == "__main__":
    print("🚀 Starting SecureDoc AI FastAPI Server")
    print("📚 API Documentation: http://localhost:8001/docs")
    print("🔐 Authentication required for most endpoints")
    print("💡 Default users: amer/demo123 or admin/admin123")
    print("-" * 50)
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8001,  # Changed from 8000 to 8001
        reload=True,
        log_level="info"
    )