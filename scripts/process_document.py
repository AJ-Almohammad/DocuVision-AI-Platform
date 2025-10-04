#!/usr/bin/env python3
"""
Complete document processing pipeline: Upload -> Generate SAS -> Analyze with AI
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import logging
from src.data_ingestion.storage_client import AzureStorageClient
from src.data_processing.document_processor import DocumentProcessor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("🔄 Starting Complete Document Processing Pipeline...")
    
    try:
        # Step 1: Upload PDF file to storage
        print("\n1. 📤 Uploading PDF file to Azure Storage...")
        storage_client = AzureStorageClient()
        
        sample_file_path = "sample_technical_report.pdf"
        blob_name = "sample_technical_report.pdf"  # Keep the .pdf extension
        
        if os.path.exists(sample_file_path):
            blob_url = storage_client.upload_file(sample_file_path, blob_name)
            print(f"   ✅ Uploaded: {blob_name}")
        else:
            print(f"   ❌ File not found: {sample_file_path}")
            print("   Please run: python scripts/create_test_pdf.py")
            return
        
        # Step 2: Generate SAS URL for secure access
        print("\n2. 🔐 Generating secure SAS URL...")
        sas_url = storage_client.generate_sas_url(blob_name)
        print(f"   ✅ SAS URL generated (secure, temporary access)")
        
        # Step 3: Test Document Intelligence connection
        print("\n3. 🧪 Testing Document Intelligence connection...")
        doc_processor = DocumentProcessor()
        
        if doc_processor.test_connection():
            print("   ✅ Document Intelligence connection successful!")
        else:
            print("   ❌ Document Intelligence connection failed!")
            return
        
        # Step 4: Analyze the document with AI
        print("\n4. 🔍 Analyzing document with Azure AI...")
        analysis_result = doc_processor.analyze_document(sas_url)
        
        print("\n🎉 DOCUMENT ANALYSIS COMPLETE!")
        print("="*50)
        print(f"📄 Document: {blob_name}")
        print(f"📊 Pages analyzed: {len(analysis_result['pages'])}")
        print(f"📋 Tables found: {len(analysis_result['tables'])}")
        
        # Show extracted content preview
        if analysis_result['content']:
            content_preview = analysis_result['content'][:300] + "..." if len(analysis_result['content']) > 300 else analysis_result['content']
            print(f"\n📝 Content Preview:\n{content_preview}")
        
        # Show lines from first page
        if analysis_result['pages']:
            first_page = analysis_result['pages'][0]
            print(f"\n📄 First page lines ({len(first_page['lines'])} lines):")
            for i, line in enumerate(first_page['lines'][:10]):  # Show first 10 lines
                print(f"   {i+1}. {line}")
            
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error in document processing pipeline: {str(e)}")

if __name__ == "__main__":
    main()