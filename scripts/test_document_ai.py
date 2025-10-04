#!/usr/bin/env python3
"""
Test script for Azure Document Intelligence
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import logging
from src.data_processing.document_processor import DocumentProcessor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("🧪 Testing Azure Document Intelligence Connection...")
    
    try:
        # Initialize document processor
        doc_processor = DocumentProcessor()
        
        # Test connection
        if doc_processor.test_connection():
            print("✅ Document Intelligence connection successful!")
        else:
            print("❌ Document Intelligence connection failed!")
            
    except Exception as e:
        print(f"❌ Error during Document Intelligence test: {str(e)}")

if __name__ == "__main__":
    main()