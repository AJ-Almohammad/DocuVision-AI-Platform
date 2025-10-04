#!/usr/bin/env python3
"""
Upload sample file to Azure Storage
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import logging
from src.data_ingestion.storage_client import AzureStorageClient

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("📤 Uploading sample file to Azure Storage...")
    
    try:
        # Initialize storage client
        storage_client = AzureStorageClient()
        
        # Upload the sample file
        sample_file_path = "sample_data.txt"
        
        if os.path.exists(sample_file_path):
            print(f"📄 Found sample file: {sample_file_path}")
            blob_url = storage_client.upload_file(sample_file_path, "sample_technical_report.txt")
            
            print(f"\n🎉 Upload successful!")
            print(f"📎 File uploaded as: sample_technical_report.txt")
            print(f"🔗 Blob URL: {blob_url}")
            
            # List all blobs to confirm
            print(f"\n📁 Current blobs in container:")
            storage_client.list_blobs()
            
        else:
            print(f"❌ Sample file not found: {sample_file_path}")
            print("Please make sure sample_data.txt exists in the project root")
            
    except Exception as e:
        print(f"❌ Error during upload: {str(e)}")

if __name__ == "__main__":
    main()