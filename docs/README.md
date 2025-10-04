# 🔒 SecureDoc AI - Document Intelligence Platform

![Azure](https://img.shields.io/badge/Azure-Cloud%20Platform-0078D4?logo=microsoft-azure)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)

> **Enterprise-grade document processing with AI-powered insights and real-time analytics**

## 🎯 Live Demos & Quick Access

| Demo Type | Link | Description |
|-----------|------|-------------|
| **🚀 Live Dashboard** | [Launch Dashboard](./dashboard_enhanced.py) | Interactive monitoring interface |
| **🛠️ Setup Script** | [Run Setup](./scripts/azure_setup.py) | Azure infrastructure deployment |
| **🔍 Test Pipeline** | [Process Documents](./scripts/process_document.py) | End-to-end document processing |
| **📊 Storage Test** | [Test Storage](./scripts/test_storage.py) | Azure Blob Storage verification |
| **💰 Cost Monitor** | [Check Costs](./scripts/check_costs.py) | Budget and spending analytics |
| **🧹 Cleanup** | [Remove Resources](./scripts/azure_cleanup.py) | Safe Azure resource deletion |

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture) 
- [Quick Start](#-quick-start)
- [Detailed Setup](#-detailed-setup)
- [API Reference](#-api-reference)
- [Cost Management](#-cost-management)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

### 🤖 AI-Powered Processing
- **Document Intelligence** - Extract text, tables, and structure from PDFs
- **Multi-format Support** - PDF, images, Word documents processing
- **Layout Analysis** - Intelligent document structure recognition
- **Data Extraction** - Transform unstructured documents to structured data

### 📊 Real-time Analytics
- **Interactive Dashboard** - Live monitoring with Streamlit
- **Budget Tracking** - Real-time Azure cost monitoring
- **Processing Metrics** - Performance and usage analytics
- **System Health** - Service status and performance monitoring

### 🔒 Enterprise Security
- **Secure Access** - SAS token authentication
- **Encrypted Storage** - Azure Blob Storage encryption
- **Environment Security** - Protected credential management
- **Access Control** - Role-based security patterns

### ☁️ Cloud Native
- **Azure Integration** - Native cloud service integration
- **Scalable Architecture** - Modular and extensible design
- **Cost Optimized** - Free-tier eligible services
- **DevOps Ready** - CI/CD and monitoring prepared

## 🏗️ Architecture

```mermaid
graph TB
    A[Document Upload] --> B[Azure Blob Storage]
    B --> C[SAS Token Generation]
    C --> D[Azure Document Intelligence]
    D --> E[Data Extraction]
    E --> F[Structured Data]
    F --> G[Streamlit Dashboard]
    F --> H[Analytics & Reporting]
    
    I[Budget Monitoring] --> J[Cost Alerts]
    K[Security Layer] --> L[Access Control]

Core Components
Component	Technology	Purpose
Frontend	Streamlit	Interactive dashboard
Storage	Azure Blob Storage	Secure file storage
AI Processing	Azure Document Intelligence	Document analysis
Security	SAS Tokens	Secure access control
Monitoring	Cost Analytics	Budget tracking
🚀 Quick Start
Prerequisites
Python 3.9+

Azure Account with active subscription

Azure CLI installed

5-Minute Setup
Clone & Setup

bash
git clone <repository-url>
cd tuv-sud-document-ai-platform
python -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate.ps1  # Windows
pip install -r requirements.txt
Azure Infrastructure → setup script

bash
python scripts/azure_setup.py
Launch Dashboard → dashboard

bash
streamlit run dashboard_enhanced.py
Test Pipeline → processing script

bash
python scripts/process_document.py
⚙️ Detailed Setup
1. Environment Configuration → settings
Copy the environment template:

bash
cp config/sample.env .env
Edit .env with your Azure credentials from the setup script.

2. Azure Services Deployment → setup script
The setup script creates:

Resource Group: tuv-sud-document-ai-rg

Storage Account: Secure blob storage

Document Intelligence: AI processing service

Security Configuration: Access policies

3. Testing the Pipeline → test scripts
Test	Script	Purpose
Storage Test	test_storage.py	Verify Azure Storage
AI Service Test	test_document_ai.py	Check Document Intelligence
Full Pipeline	process_document.py	End-to-end processing
Security Check	validate_security.py	Security validation
🔌 API Reference
Storage Client → storage_client.py
python
from src.data_ingestion.storage_client import AzureStorageClient

# Initialize client
client = AzureStorageClient()

# Upload document
blob_url = client.upload_file("document.pdf")

# Generate secure URL
sas_url = client.generate_sas_url("document.pdf")

# List documents
documents = client.list_blobs()
Document Processor → document_processor.py
python
from src.data_processing.document_processor import DocumentProcessor

# Initialize processor
processor = DocumentProcessor()

# Analyze document
results = processor.analyze_document(sas_url)

# Access extracted data
content = results['content']
pages = results['pages']
tables = results['tables']
💰 Cost Management
Budget Monitoring → check_costs.py
Monitor your Azure spending:

bash
python scripts/check_costs.py
Cost Optimization
Service	Free Tier	Cost Beyond Free Tier
Azure Blob Storage	5 GB/month	$0.023 per GB
Document Intelligence	500 pages/month	$1.50 per 100 pages
Estimated Monthly	$0-2	Monitor usage
Cleanup Resources → azure_cleanup.py
Safe resource deletion:

bash
python scripts/azure_cleanup.py
🛠️ Troubleshooting
Common Issues
Azure Authentication Error

bash
az login
az account set --subscription "your-subscription-id"
Module Import Errors

bash
pip install -r requirements.txt
Storage Connection Issues

Verify .env file contains correct connection strings

Check Azure portal for service status

Budget Alerts

Monitor usage in Azure Cost Management

Set up spending alerts in Azure Portal

Debugging Scripts
Script	Purpose	Debug Command
validate_security.py	Security check	python scripts/validate_security.py
test_storage.py	Storage test	python scripts/test_storage.py
test_document_ai.py	AI service test	python scripts/test_document_ai.py
🤝 Contributing
Development Setup
Fork the repository

Create feature branch

Make changes with tests

Submit pull request

Project Structure
tuv-sud-document-ai-platform/
├── 🎨 dashboard_enhanced.py          # Main interactive dashboard
├── 🎨 dashboard.py                   # Original dashboard
├── 🔧 scripts/                       # Utility and setup scripts
├── 💾 src/                           # Source code
│   ├── data_ingestion/              # Storage and file management
│   └── data_processing/             # AI and document processing
├── ⚙️ config/                        # Configuration management
├── 📚 docs/                          # Documentation
├── 🧪 tests/                         # Test suites
├── 📄 requirements.txt              # Python dependencies
├── 🔐 .env                          # Environment variables (local)
├── 📋 sample_technical_report.pdf   # Demo document
└── 📋 professional_technical_report.pdf # Professional demo document

Run the test suite:

bash
python -m pytest tests/
👨‍💻 Developer
Amer Almohammad
AWS Junior Cloud Engineer
📧 ajaber1973@web.de

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Azure Cognitive Services for document intelligence

Streamlit for interactive dashboard framework

Python community for extensive libraries

<div align="center">
⭐ If this project helped you, please give it a star!

Report Bug • Request Feature

</div> ```