#!/usr/bin/env python3
"""
Startup script for Simplified SecureDoc AI FastAPI
"""
import uvicorn
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

if __name__ == "__main__":
    print("🚀 Starting SecureDoc AI FastAPI Server (Simplified)")
    print("📚 API Documentation: http://localhost:8001/docs")
    print("🔐 Authentication required for most endpoints")
    print("👥 Demo Users:")
    print("   - amer/demo123 (Regular user)")
    print("   - admin/admin123 (Admin user)") 
    print("   - viewer/view123 (Viewer user)")
    print("💡 Works without Azure configuration")
    print("-" * 50)
    
    uvicorn.run(
        "src.api.simple_main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )