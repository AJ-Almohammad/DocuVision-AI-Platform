#!/usr/bin/env python3
"""
Test client for SecureDoc AI FastAPI
"""
import requests
import json

##API_BASE_URL = "http://localhost:8000"
API_BASE_URL = "http://localhost:8001"  # Changed from 8000 to 8001

def test_api():
    print("🧪 Testing SecureDoc AI FastAPI Backend")
    print("=" * 50)
    
    # Test without authentication
    print("\n1. Testing public endpoints...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
        
        response = requests.get(f"{API_BASE_URL}/system/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Public endpoints failed: {e}")
        return
    
    # Test authentication
    print("\n2. Testing authentication...")
    try:
        login_data = {
            "username": "amer",
            "password": "demo123"
        }
        response = requests.post(f"{API_BASE_URL}/token", data=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✅ Authentication successful - Token received")
            
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test protected endpoints
            print("\n3. Testing protected endpoints...")
            
            # Get user info
            response = requests.get(f"{API_BASE_URL}/users/me", headers=headers)
            print(f"✅ User info: {response.status_code} - {response.json()}")
            
            # List documents
            response = requests.get(f"{API_BASE_URL}/documents/list", headers=headers)
            print(f"✅ Document list: {response.status_code} - {len(response.json()['documents'])} documents")
            
            # Get system metrics
            response = requests.get(f"{API_BASE_URL}/system/metrics", headers=headers)
            print(f"✅ System metrics: {response.status_code} - Metrics received")
            
            print("\n🎉 API testing completed successfully!")
            print(f"🔑 Token: {token[:50]}...")
            print(f"📚 API Documentation: {API_BASE_URL}/docs")
            
        else:
            print(f"❌ Authentication failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ API testing failed: {e}")

if __name__ == "__main__":
    test_api()