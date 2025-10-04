# SecureDoc AI - GitHub Repository Setup Guide

## 🚀 Quick Start for Reviewers

### 1. Main Dashboard
- **File:** [`../dashboard_enhanced.py`](../dashboard_enhanced.py)
- **Purpose:** Interactive monitoring interface with budget analytics
- **Run:** `streamlit run dashboard_enhanced.py`

### 2. Core Data Pipeline
- **File:** [`../scripts/process_document.py`](../scripts/process_document.py)
- **Purpose:** End-to-end document processing demonstration
- **Run:** `python scripts/process_document.py`

### 3. Azure Infrastructure
- **File:** [`../scripts/azure_setup.py`](../scripts/azure_setup.py)
- **Purpose:** Automated Azure resource deployment
- **Run:** `python scripts/azure_setup.py`

### 4. Key Components

| Component | File | Description |
|-----------|------|-------------|
| **Storage Client** | [`../src/data_ingestion/storage_client.py`](../src/data_ingestion/storage_client.py) | Azure Blob Storage integration |
| **Document Processor** | [`../src/data_processing/document_processor.py`](../src/data_processing/document_processor.py) | AI-powered document analysis |
| **Security Validation** | [`../scripts/validate_security.py`](../scripts/validate_security.py) | Security best practices check |
| **Cost Monitoring** | [`../scripts/check_costs.py`](../scripts/check_costs.py) | Budget and spending analytics |

## 📊 Project Architecture
📁 tuv-sud-document-ai-platform/
├── 🎨 dashboard_enhanced.py # Main dashboard interface
├── 🎨 dashboard.py # Original dashboard
├── 🔧 scripts/ # Utility scripts
│ ├── azure_setup.py # Azure infrastructure
│ ├── process_document.py # Data pipeline
│ ├── test_storage.py # Storage testing
│ └── check_costs.py # Cost monitoring
├── 💾 src/ # Source code
│ ├── data_ingestion/
│ │ └── storage_client.py # Azure Storage integration
│ └── data_processing/
│ └── document_processor.py # AI document processing
├── ⚙️ config/ # Configuration
│ └── settings.py # Settings management
├── 📚 docs/ # Documentation (this folder)
├── 🧪 tests/ # Test suites
└── 📄 requirements.txt # Dependencies


## 🎯 Setup Instructions

```bash
# 1. Clone repository
git clone https://github.com/AJ-Almohammad/tuv-sud-document-ai-platform.git
cd tuv-sud-document-ai-platform

# 2. Setup environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate.ps1  # Windows
pip install -r requirements.txt

# 3. Configure Azure (requires Azure account)
python scripts/azure_setup.py

# 4. Launch dashboard
streamlit run dashboard_enhanced.py

# 5. Test the pipeline
python scripts/process_document.py

🔧 Testing the System
Quick Test Sequence
# Test storage connection
python scripts/test_storage.py

# Test document intelligence
python scripts/test_document_ai.py

# Run complete pipeline
python scripts/process_document.py

# Check security
python scripts/validate_security.py

# Monitor costs
python scripts/check_costs.py

💰 Cost Management
Budget Monitoring
Run: python scripts/check_costs.py

Monitor Azure spending and budget utilization

Set up alerts in Azure Portal for $5 monthly budget

Cleanup Resources
Run: python scripts/azure_cleanup.py

Safely delete all Azure resources when done testing

Prevents ongoing charges for unused services

🎥 Demo Features to Showcase
1. Dashboard Features
Real-time budget tracking and analytics

Document processing metrics

System health monitoring

Interactive file upload and processing

2. Data Pipeline
PDF document upload to Azure Storage

AI-powered text and table extraction

Structured data output

Error handling and retry mechanisms

3. Technical Implementation
Modular Python architecture

Azure cloud service integration

Security best practices

Cost optimization features

📋 File Reference Guide
Core Application Files
../dashboard_enhanced.py - Main dashboard

../src/data_ingestion/storage_client.py - Storage management

../src/data_processing/document_processor.py - AI processing

Utility Scripts
../scripts/azure_setup.py - Infrastructure setup

../scripts/process_document.py - Pipeline testing

../scripts/check_costs.py - Cost monitoring

../scripts/azure_cleanup.py - Resource cleanup

Configuration
../config/settings.py - Application settings

../.env - Environment variables (create from sample)

../requirements.txt - Python dependencies

🛠️ Troubleshooting
Common Issues
Azure Authentication
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

👨‍💻 Developer
Amer Almohammad
Data Engineer & Cloud Specialist
📧 ajaber1973@web.de
🔗 LinkedIn
🐙 GitHub

<div align="center">
For questions or technical support, please open an issue on GitHub

Main Repository •
Report Issues

</div> ```