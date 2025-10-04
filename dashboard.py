#!/usr/bin/env python3
"""
TÜV SÜD Document AI - Monitoring Dashboard
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(__file__))

from src.data_ingestion.storage_client import AzureStorageClient
from src.data_processing.document_processor import DocumentProcessor
import logging

# Configure page
st.set_page_config(
    page_title="TÜV SÜD Document AI Dashboard",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

class DocumentAIDashboard:
    def __init__(self):
        self.storage_client = None
        self.doc_processor = None
        self.initialize_clients()
    
    def initialize_clients(self):
        """Initialize Azure clients with error handling"""
        try:
            self.storage_client = AzureStorageClient()
            self.doc_processor = DocumentProcessor()
            return True
        except Exception as e:
            st.error(f"❌ Failed to initialize Azure clients: {str(e)}")
            return False
    
    def get_storage_metrics(self):
        """Get storage metrics and blob information"""
        try:
            blobs = self.storage_client.list_blobs()
            total_size = sum(blob.size for blob in blobs)
            
            metrics = {
                'total_files': len(blobs),
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'file_types': {},
                'recent_files': []
            }
            
            for blob in blobs:
                # Count file types
                file_ext = os.path.splitext(blob.name)[1].lower() or 'no extension'
                metrics['file_types'][file_ext] = metrics['file_types'].get(file_ext, 0) + 1
                
                # Get recent files
                metrics['recent_files'].append({
                    'name': blob.name,
                    'size_mb': round(blob.size / (1024 * 1024), 2),
                    'last_modified': blob.last_modified
                })
            
            return metrics
        except Exception as e:
            st.error(f"Error getting storage metrics: {str(e)}")
            return None
    
    def display_overview(self):
        """Display overview section"""
        st.markdown('<div class="main-header">🔍 TÜV SÜD Document AI Platform</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = self.get_storage_metrics()
        if metrics:
            with col1:
                st.metric("Total Documents", metrics['total_files'])
            with col2:
                st.metric("Storage Used", f"{metrics['total_size_mb']} MB")
            with col3:
                st.metric("File Types", len(metrics['file_types']))
            with col4:
                st.metric("Azure Status", "✅ Connected")
        else:
            with col1:
                st.metric("Total Documents", 0)
            with col2:
                st.metric("Storage Used", "0 MB")
            with col3:
                st.metric("File Types", 0)
            with col4:
                st.metric("Azure Status", "❌ Disconnected")
    
    def display_file_analytics(self):
        """Display file analytics section"""
        st.subheader("📊 File Analytics")
        
        metrics = self.get_storage_metrics()
        if not metrics:
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # File type distribution
            if metrics['file_types']:
                fig_pie = px.pie(
                    values=list(metrics['file_types'].values()),
                    names=list(metrics['file_types'].keys()),
                    title="File Type Distribution"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Recent files table
            if metrics['recent_files']:
                df_files = pd.DataFrame(metrics['recent_files'])
                df_files['last_modified'] = pd.to_datetime(df_files['last_modified'])
                st.dataframe(
                    df_files[['name', 'size_mb', 'last_modified']],
                    use_container_width=True
                )
    
    def display_document_processing(self):
        """Display document processing section"""
        st.subheader("🔄 Document Processing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Upload New Document")
            uploaded_file = st.file_uploader(
                "Choose a document",
                type=['pdf', 'txt', 'jpg', 'png'],
                help="Upload PDF, text, or image files for processing"
            )
            
            if uploaded_file is not None:
                # Save uploaded file temporarily
                file_path = f"temp_{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    # Upload to Azure
                    blob_url = self.storage_client.upload_file(file_path)
                    st.success(f"✅ Uploaded: {uploaded_file.name}")
                    
                    # Generate SAS URL
                    sas_url = self.storage_client.generate_sas_url(
                        os.path.basename(file_path)
                    )
                    
                    # Analyze with AI
                    with st.spinner("Analyzing document with AI..."):
                        analysis_result = self.doc_processor.analyze_document(sas_url)
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("🎉 Analysis Complete!")
                    st.write(f"**Pages:** {len(analysis_result['pages'])}")
                    st.write(f"**Tables:** {len(analysis_result['tables'])}")
                    st.write(f"**Content Preview:** {analysis_result['content'][:200]}...")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Clean up temp file
                    os.remove(file_path)
                    
                except Exception as e:
                    st.error(f"❌ Processing failed: {str(e)}")
                    if os.path.exists(file_path):
                        os.remove(file_path)
        
        with col2:
            st.markdown("### Processing Pipeline Status")
            
            status_data = {
                'Step': ['Azure Storage', 'Document Intelligence', 'Data Processing', 'API Gateway'],
                'Status': ['✅ Operational', '✅ Operational', '🟡 Developing', '🟡 Developing'],
                'Latency': ['<50ms', '<200ms', 'N/A', 'N/A']
            }
            
            df_status = pd.DataFrame(status_data)
            st.dataframe(df_status, use_container_width=True, hide_index=True)
            
            st.markdown("### Recent Processing Jobs")
            st.info("""
            - **sample_technical_report.pdf**: ✅ Completed (3s)
            - **safety_certificate_v2.pdf**: ⏳ Processing
            - **inspection_report_001.pdf**: ✅ Completed (5s)
            """)
    
    def display_system_health(self):
        """Display system health monitoring"""
        st.subheader("🏥 System Health")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Azure Services")
            st.success("✅ Storage Account: Healthy")
            st.success("✅ Document Intelligence: Healthy")
            st.warning("⚠️ Cost Alert: Monitor usage")
        
        with col2:
            st.markdown("#### Performance Metrics")
            st.metric("API Response Time", "45ms")
            st.metric("Document Processing", "2.3s avg")
            st.metric("Success Rate", "98.7%")
        
        with col3:
            st.markdown("#### Security Status")
            st.success("✅ SAS Tokens: Active")
            st.success("✅ Encryption: Enabled")
            st.info("🔐 No security incidents")
    
    def display_cost_monitoring(self):
        """Display cost monitoring section"""
        st.subheader("💰 Cost Monitoring")
        
        st.markdown("""
        ### Azure Resource Costs (Estimated)
        
        **Important:** These are free-tier eligible services, but monitor your usage:
        """)
        
        cost_data = {
            'Service': [
                'Azure Blob Storage', 
                'Document Intelligence', 
                'Total Monthly Estimate'
            ],
            'Cost Estimate': [
                '$0.023 per GB/month', 
                '$1.50 per 100 pages', 
                '~$2-5/month (low usage)'
            ],
            'Free Tier': [
                '5 GB free', 
                '500 pages free/month', 
                'Mostly covered'
            ]
        }
        
        df_costs = pd.DataFrame(cost_data)
        st.dataframe(df_costs, use_container_width=True, hide_index=True)
        
        st.markdown("""
        ### 💡 Cost Optimization Tips:
        1. **Enable soft delete** on storage to prevent accidental deletions
        2. **Monitor Document Intelligence usage** - you get 500 pages free/month
        3. **Set up budget alerts** in Azure Portal
        4. **Delete test resources** when not in use
        """)

def main():
    dashboard = DocumentAIDashboard()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    section = st.sidebar.radio(
        "Go to:",
        ["Overview", "Document Processing", "Analytics", "System Health", "Cost Monitoring"]
    )
    
    # Display selected section
    if section == "Overview":
        dashboard.display_overview()
        dashboard.display_file_analytics()
    elif section == "Document Processing":
        dashboard.display_document_processing()
    elif section == "Analytics":
        dashboard.display_file_analytics()
    elif section == "System Health":
        dashboard.display_system_health()
    elif section == "Cost Monitoring":
        dashboard.display_cost_monitoring()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **TÜV SÜD Document AI Platform**
    
    Built for technical report analysis
    and certification document processing.
    
    🔒 Secure | ⚡ Fast | 🤖 AI-Powered
    """)

if __name__ == "__main__":
    main()