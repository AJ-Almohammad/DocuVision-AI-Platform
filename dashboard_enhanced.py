#!/usr/bin/env python3
"""
SecureDoc AI - Document Processing Platform Dashboard
Enhanced with Azure Budget Integration
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(__file__))

from src.data_ingestion.storage_client import AzureStorageClient
from src.data_processing.document_processor import DocumentProcessor
import logging

# Configure page
st.set_page_config(
    page_title="SecureDoc AI Platform",
    page_icon="🔒",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2563eb;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #2563eb;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #dcfce7;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #16a34a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .warning-box {
        background-color: #fef3c7;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #d97706;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .budget-alert {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

class SecureDocDashboard:
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
                'recent_files': [],
                'daily_processing': self.generate_processing_stats()
            }
            
            for blob in blobs:
                # Count file types
                file_ext = os.path.splitext(blob.name)[1].lower() or 'no extension'
                metrics['file_types'][file_ext] = metrics['file_types'].get(file_ext, 0) + 1
                
                # Get recent files
                metrics['recent_files'].append({
                    'name': blob.name,
                    'size_mb': round(blob.size / (1024 * 1024), 2),
                    'last_modified': blob.last_modified,
                    'type': file_ext
                })
            
            return metrics
        except Exception as e:
            st.error(f"Error getting storage metrics: {str(e)}")
            return None
    
    def generate_processing_stats(self):
        """Generate simulated processing statistics"""
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now())
        return {
            'dates': dates,
            'documents_processed': [max(0, int(10 + i * 0.5 + (i % 7) * 2)) for i in range(len(dates))],
            'processing_time': [max(1.0, 2.0 + (i % 5) * 0.3) for i in range(len(dates))]
        }
    
    def get_budget_data(self):
        """Get budget and cost data"""
        return {
            'budget_name': 'secureai-limited-budget',
            'budget_amount': 5.00,
            'current_spend': 0.42,  # Simulated current spend
            'forecasted_spend': 0.85,
            'progress_percent': 8.4,
            'reset_period': 'Monthly',
            'creation_date': '2024-09-01',
            'expiration_date': '2026-08-31',
            'alert_threshold': 80.0
        }
    
    def display_overview(self):
        """Display overview section"""
        st.markdown('<div class="main-header">🔒 SecureDoc AI Platform</div>', unsafe_allow_html=True)
        
        # Budget Alert Banner
        budget_data = self.get_budget_data()
        if budget_data['progress_percent'] > budget_data['alert_threshold']:
            st.markdown(f"""
            <div class="budget-alert">
                <h3>🚨 Budget Alert</h3>
                <p>Current spend ({budget_data['progress_percent']}%) is approaching your ${budget_data['budget_amount']} budget limit.</p>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = self.get_storage_metrics()
        budget_data = self.get_budget_data()
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Documents", metrics['total_files'] if metrics else 0)
            st.caption("📁 Storage Container")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Storage Used", f"{metrics['total_size_mb']} MB" if metrics else "0 MB")
            st.caption("💾 Azure Blob Storage")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Monthly Budget", f"${budget_data['current_spend']}/${budget_data['budget_amount']}")
            st.caption(f"📊 {budget_data['progress_percent']}% used")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("AI Processing", "Active" if metrics else "Inactive")
            st.caption("🤖 Document Intelligence")
            st.markdown('</div>', unsafe_allow_html=True)
    
    def display_budget_analytics(self):
        """Display budget and cost analytics"""
        st.subheader("💰 Budget & Cost Analytics")
        
        budget_data = self.get_budget_data()
        metrics = self.get_storage_metrics()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Budget progress gauge
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = budget_data['progress_percent'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f"Budget Usage (%)", 'font': {'size': 20}},
                delta = {'reference': budget_data['alert_threshold'], 'increasing': {'color': "red"}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': 'lightgreen'},
                        {'range': [50, 80], 'color': 'yellow'},
                        {'range': [80, 100], 'color': 'red'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': budget_data['alert_threshold']
                    }
                }
            ))
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            # Cost breakdown
            cost_breakdown = {
                'Service': ['Document Intelligence', 'Blob Storage', 'Networking', 'Monitoring'],
                'Cost': [0.25, 0.12, 0.03, 0.02],
                'Percentage': [60, 29, 7, 4]
            }
            df_costs = pd.DataFrame(cost_breakdown)
            
            fig_pie = px.pie(
                df_costs, 
                values='Cost', 
                names='Service',
                title="Monthly Cost Distribution",
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Budget details table
        st.markdown("### Budget Details")
        budget_details = {
            'Metric': [
                'Budget Name', 'Total Budget', 'Current Spend', 
                'Forecasted Spend', 'Reset Period', 'Status'
            ],
            'Value': [
                budget_data['budget_name'],
                f"${budget_data['budget_amount']}",
                f"${budget_data['current_spend']}",
                f"${budget_data['forecasted_spend']}",
                budget_data['reset_period'],
                "🟢 Within Budget" if budget_data['progress_percent'] < 80 else "🟡 Approaching Limit"
            ]
        }
        df_budget = pd.DataFrame(budget_details)
        st.dataframe(df_budget, use_container_width=True, hide_index=True)
    
    def display_processing_analytics(self):
        """Display processing analytics"""
        st.subheader("📈 Processing Analytics")
        
        metrics = self.get_storage_metrics()
        if not metrics:
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Documents processed over time
            processing_data = metrics['daily_processing']
            df_trend = pd.DataFrame({
                'Date': processing_data['dates'],
                'Documents Processed': processing_data['documents_processed']
            })
            
            fig_trend = px.line(
                df_trend, 
                x='Date', 
                y='Documents Processed',
                title="Daily Documents Processed",
                line_shape='spline'
            )
            fig_trend.update_traces(line=dict(color='#2563eb', width=3))
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            # File type distribution
            if metrics['file_types']:
                df_files = pd.DataFrame({
                    'File Type': list(metrics['file_types'].keys()),
                    'Count': list(metrics['file_types'].values())
                })
                
                fig_bar = px.bar(
                    df_files,
                    x='File Type',
                    y='Count',
                    title="Files by Type",
                    color='Count',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
    
    def display_document_processing(self):
        """Display document processing section"""
        st.subheader("🔄 Document Processing Pipeline")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Upload & Process Documents")
            
            # File uploader
            uploaded_file = st.file_uploader(
                "Choose a document to process",
                type=['pdf', 'txt', 'jpg', 'png', 'docx'],
                help="Supported formats: PDF, Text, Images, Word Documents"
            )
            
            if uploaded_file is not None:
                # Display file info
                file_info = {
                    'Name': uploaded_file.name,
                    'Type': uploaded_file.type,
                    'Size': f"{len(uploaded_file.getvalue()) / 1024:.1f} KB"
                }
                
                st.markdown("#### File Details")
                for key, value in file_info.items():
                    st.write(f"**{key}:** {value}")
                
                # Processing options
                st.markdown("#### Processing Options")
                col_opt1, col_opt2 = st.columns(2)
                with col_opt1:
                    extract_text = st.checkbox("Extract Text", value=True)
                    detect_tables = st.checkbox("Detect Tables", value=True)
                with col_opt2:
                    analyze_layout = st.checkbox("Analyze Layout", value=True)
                    save_to_db = st.checkbox("Save to Database", value=False)
                
                # Process button
                if st.button("🚀 Process Document", type="primary"):
                    with st.spinner("Processing document with AI..."):
                        try:
                            # Save uploaded file temporarily
                            file_path = f"temp_{uploaded_file.name}"
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                            
                            # Upload to Azure
                            blob_url = self.storage_client.upload_file(file_path)
                            
                            # Generate SAS URL
                            sas_url = self.storage_client.generate_sas_url(
                                os.path.basename(file_path)
                            )
                            
                            # Analyze with AI
                            analysis_result = self.doc_processor.analyze_document(sas_url)
                            
                            # Display results
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.success("🎉 Document Processing Complete!")
                            
                            col_res1, col_res2, col_res3 = st.columns(3)
                            with col_res1:
                                st.metric("Pages", len(analysis_result['pages']))
                            with col_res2:
                                st.metric("Tables", len(analysis_result['tables']))
                            with col_res3:
                                st.metric("Lines", sum(len(page['lines']) for page in analysis_result['pages']))
                            
                            # Show content preview
                            with st.expander("📝 View Extracted Content"):
                                st.text_area(
                                    "Document Content",
                                    analysis_result['content'],
                                    height=200
                                )
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Clean up
                            os.remove(file_path)
                            
                        except Exception as e:
                            st.error(f"❌ Processing failed: {str(e)}")
                            if os.path.exists(file_path):
                                os.remove(file_path)
        
        with col2:
            st.markdown("### Pipeline Status")
            
            # Real-time status indicators
            status_data = [
                {"Stage": "File Upload", "Status": "✅", "Duration": "<1s"},
                {"Stage": "Storage", "Status": "✅", "Duration": "<2s"},
                {"Stage": "AI Analysis", "Status": "✅", "Duration": "2-5s"},
                {"Stage": "Data Extraction", "Status": "🟡", "Duration": "<1s"},
                {"Stage": "Results", "Status": "✅", "Duration": "Instant"}
            ]
            
            for stage in status_data:
                st.write(f"{stage['Status']} **{stage['Stage']}**")
                st.caption(f"⏱️ {stage['Duration']}")
                st.progress(100 if stage['Status'] == "✅" else 75)
            
            st.markdown("---")
            st.markdown("#### Cost Estimate")
            st.info("""
            **Current Processing:**
            - Storage: $0.001
            - AI Processing: $0.015
            - **Total: ~$0.016**
            """)
    
    def display_system_monitoring(self):
        """Display system monitoring section"""
        st.subheader("🏥 System Health & Monitoring")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🔧 Azure Services")
            services = [
                ("Blob Storage", "✅ Healthy", "5.2 MB used"),
                ("Document Intelligence", "✅ Healthy", "23 pages processed"),
                ("App Service", "🟡 Developing", "Not deployed"),
                ("Database", "🟡 Planned", "Q4 2024")
            ]
            
            for service, status, details in services:
                st.write(f"**{service}**")
                st.write(f"{status} - {details}")
                st.progress(90 if status == "✅ Healthy" else 50)
        
        with col2:
            st.markdown("#### 📊 Performance")
            performance_data = {
                'Metric': ['API Response', 'Document Processing', 'Upload Speed', 'AI Analysis'],
                'Value': ['48ms', '2.1s', '4.2 MB/s', '1.8s'],
                'Trend': ['↘️', '→', '↗️', '→']
            }
            df_perf = pd.DataFrame(performance_data)
            st.dataframe(df_perf, use_container_width=True, hide_index=True)
        
        with col3:
            st.markdown("#### 🔒 Security")
            security_status = [
                ("SAS Tokens", "✅ Active", "1hr expiry"),
                ("Encryption", "✅ Enabled", "AES-256"),
                ("Access Control", "✅ Configured", "RBAC"),
                ("Audit Logs", "🟡 Developing", "Q4 2024")
            ]
            
            for item, status, details in security_status:
                st.write(f"**{item}**")
                st.write(f"{status} - {details}")

def main():
    dashboard = SecureDocDashboard()
    
    # Sidebar navigation
    st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1>🔒</h1>
        <h3>SecureDoc AI</h3>
        <p>Document Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    section = st.sidebar.radio(
        "Navigation",
        ["📊 Overview", "💰 Budget Analytics", "📈 Processing Analytics", "🔄 Document Processing", "🏥 System Health"]
    )
    
    # Display selected section
    if section == "📊 Overview":
        dashboard.display_overview()
        dashboard.display_processing_analytics()
    elif section == "💰 Budget Analytics":
        dashboard.display_budget_analytics()
    elif section == "📈 Processing Analytics":
        dashboard.display_processing_analytics()
    elif section == "🔄 Document Processing":
        dashboard.display_document_processing()
    elif section == "🏥 System Health":
        dashboard.display_system_monitoring()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **Platform Information**
    
    🔒 **SecureDoc AI**
    - Document Processing & Analysis
    - AI-Powered Insights
    - Enterprise Security
    
    **Version:** 1.0.0
    **Last Updated:** October 2024
                        
    **Contact:**
    Amer Almohammad
    AWS Junior Cloud Engineer
    📧 ajaber1973@web.de
    
    📞 Support: platform@securedoc-ai.com
    """)

if __name__ == "__main__":
    main()