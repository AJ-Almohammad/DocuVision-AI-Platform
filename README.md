# 🧠 DocuVision AI – Intelligent Document Processing Platform

![Azure](https://img.shields.io/badge/Azure-Cloud%20Platform-0078D4?logo=microsoft-azure)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)
![Node.js](https://img.shields.io/badge/Node.js-Backend-339933?logo=node.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Service-009688?logo=fastapi)

> **AI-powered document intelligence platform for secure automation, monitoring, and analytics.**  
> Built with **Python**, **Azure**, and **Streamlit**, featuring a web-based control dashboard.

---

## 🚀 Quick Start

```bash
# 1️⃣ Setup environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt

# 2️⃣ Launch Streamlit dashboard
streamlit run dashboard_enhanced.py

# 3️⃣ Launch Web Dashboard
cd dashboard_web
node server.js
# Visit http://localhost:8080

# 4️⃣ Test document processing pipeline
python scripts/process_document.py
```

## 🌐 Live Dashboards

| Component | Description | Launch Command | File Path |
|-----------|-------------|----------------|-----------|
| 🧭 Streamlit Dashboard | AI analytics & metrics view | `streamlit run dashboard_enhanced.py` | `dashboard_enhanced.py` |
| 🌍 Web Dashboard | HTML/CSS/JS interface linking all project files | `node server.js` | `dashboard_web/index.html` |

## 🧱 Project Structure

```bash
docuvision-ai-platform/
├── dashboard_enhanced.py            # Streamlit dashboard
├── dashboard_web/                   # HTML/CSS/JS dashboard
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── server.js
├── scripts/                         # Utility and setup scripts
│   ├── azure_setup.py
│   ├── azure_cleanup.py
│   ├── check_costs.py
│   ├── process_document.py
│   ├── validate_security.py
│   ├── upload_sample.py
│   └── test_*.py
├── src/                             # Core application code
│   ├── api/
│   │   ├── main.py
│   │   └── simple_main.py
│   ├── auth/
│   │   ├── authentication.py
│   │   └── simple_auth.py
│   ├── data_ingestion/
│   │   └── storage_client.py
│   ├── data_processing/
│   │   └── document_processor.py
│   └── monitoring/
├── config/
│   └── settings.py
├── docs/
│   ├── Amer-Almohammad-Data-Engineer-CV-2024.md
│   ├── COVER_LETTER_TEMPLATE.md
│   └── README.md
├── requirements.txt
├── requirements-prod.txt
├── .gitignore
└── README.md
```

## ⚙️ Core Components

### Data Ingestion
**`src/data_ingestion/storage_client.py`**  
Handles Azure Blob Storage connections, uploads, and secure SAS tokens.

### AI Document Processing
**`src/data_processing/document_processor.py`**  
Performs OCR, text extraction, table parsing, and content classification.

### Authentication
**`src/auth/authentication.py`**  
Implements secure access tokens and role-based verification.

### API Layer
**`src/api/main.py`**  
Exposes endpoints for document upload, processing, and retrieval.

## 🧩 Scripts Overview

| Script | Purpose |
|--------|---------|
| `scripts/azure_setup.py` | Automate Azure service provisioning |
| `scripts/azure_cleanup.py` | Clean up deployed Azure resources |
| `scripts/check_costs.py` | Check and optimize Azure billing costs |
| `scripts/process_document.py` | Run full document AI pipeline |
| `scripts/validate_security.py` | Verify access policies and encryption |
| `scripts/upload_sample.py` | Upload sample PDF to Azure Blob |
| `scripts/test_api.py` | Validate FastAPI endpoint health |

## 👨‍💻 Developer

**Amer Almohammad**  
Data Engineer & Cloud Specialist

📧 ajaber1973@web.de  
🐙 [GitHub Profile](https://github.com/AmerAlmohd)

---

<div align="center">

⭐ **If this project helped you, please give it a star!** ⭐

[Report Bug](https://github.com/AmerAlmohd/docuvision-ai-platform/issues) • [Request Feature](https://github.com/AmerAlmohd/docuvision-ai-platform/issues)

</div>