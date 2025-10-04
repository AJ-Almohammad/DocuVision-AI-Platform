#!/usr/bin/env python3
"""
Test client for Simplified SecureDoc AI FastAPI
"""
import requests
import json

API_BASE_URL = "http://localhost:8001"

def test_simple_api():
    print("🧪 Testing Simplified SecureDoc AI FastAPI")
    print("=" * 50)
    
    # Test public endpoints
    print("\n1. Testing public endpoints...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        
        response = requests.get(f"{API_BASE_URL}/system/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Public endpoints failed: {e}")
        return
    
    # Test authentication with different users
    users = [
        {"username": "amer", "password": "demo123", "role": "user"},
        {"username": "admin", "password": "admin123", "role": "admin"},
        {"username": "viewer", "password": "view123", "role": "viewer"}
    ]
    
    for user in users:
        print(f"\n2. Testing authentication for {user['username']}...")
        try:
            response = requests.post(f"{API_BASE_URL}/token", data=user, timeout=5)
            
            if response.status_code == 200:
                token = response.json()["access_token"]
                print(f"✅ Authentication successful for {user['username']}")
                
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test protected endpoints
                response = requests.get(f"{API_BASE_URL}/users/me", headers=headers, timeout=5)
                print(f"✅ User info: {response.json()['username']}")
                
                response = requests.get(f"{API_BASE_URL}/system/metrics", headers=headers, timeout=5)
                print(f"✅ System metrics: {response.status_code}")
                
                response = requests.get(f"{API_BASE_URL}/demo/documents", headers=headers, timeout=5)
                print(f"✅ Demo documents: {len(response.json()['documents'])} documents")
                
                # Test admin endpoint
                if user['username'] == 'admin':
                    response = requests.get(f"{API_BASE_URL}/users", headers=headers, timeout=5)
                    print(f"✅ Admin users list: {len(response.json()['users'])} users")
                
            else:
                print(f"❌ Authentication failed for {user['username']}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test failed for {user['username']}: {e}")
    
    print("\n🎉 Simplified API testing completed!")
    print(f"📚 Full API Documentation: {API_BASE_URL}/docs")

if __name__ == "__main__":
    test_simple_api()