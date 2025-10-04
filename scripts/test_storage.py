#!/usr/bin/env python3
"""
Test script for Azure Storage connection
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import logging
from src.data_ingestion.storage_client import AzureStorageClient

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("🧪 Testing Azure Storage Connection...")
    
    try:
        # Initialize storage client
        storage_client = AzureStorageClient()
        
        # Test connection
        if storage_client.test_connection():
            print("✅ Storage connection successful!")
            
            # List existing blobs
            print("\n📁 Listing existing blobs:")
            storage_client.list_blobs()
            
        else:
            print("❌ Storage connection failed!")
            
    except Exception as e:
        print(f"❌ Error during storage test: {str(e)}")

if __name__ == "__main__":
    main()