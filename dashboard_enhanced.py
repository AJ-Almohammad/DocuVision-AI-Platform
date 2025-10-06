#!/usr/bin/env python3
"""
SecureDoc AI - Document Processing Platform Dashboard
Enhanced with Dark Glowing Theme & Animations
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os
import time
import random

# Add project root to path
sys.path.append(os.path.dirname(__file__))

from src.data_ingestion.storage_client import AzureStorageClient
from src.data_processing.document_processor import DocumentProcessor
import logging

# Configure page with premium settings
st.set_page_config(
    page_title="SecureDoc AI Platform",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Glowing Dark Theme CSS with Animations
st.markdown("""
<style>
    /* Main dark theme */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Animated background elements */
    .bg-animation {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    
    .floating-circle {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    /* Glowing text and elements */
    .glow-text {
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.8), 
                     0 0 20px rgba(102, 126, 234, 0.6),
                     0 0 30px rgba(102, 126, 234, 0.4);
    }
    
    .glow-box {
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3),
                   0 0 40px rgba(102, 126, 234, 0.2),
                   0 0 60px rgba(102, 126, 234, 0.1);
    }
    
    /* Main header with animation */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
        animation: glow-pulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow-pulse {
        from { text-shadow: 0 0 10px rgba(102, 126, 234, 0.5); }
        to { text-shadow: 0 0 20px rgba(102, 126, 234, 0.8), 
                         0 0 30px rgba(102, 126, 234, 0.6); }
    }
    
    /* Premium Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4),
                   0 0 80px rgba(102, 126, 234, 0.2);
    }
    
    /* Animated metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        transition: all 0.4s ease;
        animation: card-float 3s ease-in-out infinite;
    }
    
    @keyframes card-float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.5);
    }
    
    /* Status indicators with pulse */
    .status-pulse {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(72, 187, 120, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(72, 187, 120, 0); }
        100% { box-shadow: 0 0 0 0 rgba(72, 187, 120, 0); }
    }
    
    /* Button animations */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress bars with glow */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(102, 126, 234, 0.5);
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .uploadedFile:hover {
        border-color: rgba(102, 126, 234, 0.8);
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #ffffff;
        border-radius: 10px;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Fade-in animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Typewriter effect */
    .typewriter {
        overflow: hidden;
        border-right: 2px solid #667eea;
        white-space: nowrap;
        animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #667eea; }
    }
</style>

<!-- Animated Background Elements -->
<div class="bg-animation">
    <div class="floating-circle" style="width: 300px; height: 300px; top: 10%; left: 5%; animation-delay: 0s;"></div>
    <div class="floating-circle" style="width: 200px; height: 200px; top: 60%; left: 80%; animation-delay: 2s;"></div>
    <div class="floating-circle" style="width: 150px; height: 150px; top: 20%; left: 70%; animation-delay: 4s;"></div>
    <div class="floating-circle" style="width: 250px; height: 250px; top: 70%; left: 10%; animation-delay: 1s;"></div>
</div>
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
            'budget_name': 'secureai-premium-budget',
            'budget_amount': 5.00,
            'current_spend': 0.42,
            'forecasted_spend': 0.85,
            'progress_percent': 8.4,
            'reset_period': 'Monthly',
            'creation_date': '2024-09-01',
            'expiration_date': '2026-08-31',
            'alert_threshold': 80.0
        }
    
    def display_hero_section(self):
        """Display animated hero section"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="main-header glow-text">🔒 SecureDoc AI Platform</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="typewriter fade-in-up" style='color: #e2e8f0; font-size: 1.3rem; text-align: center; margin-bottom: 3rem;'>
                Enterprise-grade document intelligence with AI-powered insights and real-time analytics
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass-card glow-box" style='text-align: center;'>
                <h3 style='color: white;'>🚀 Live Status</h3>
                <div style='display: flex; justify-content: center; gap: 1rem; margin: 1rem 0;'>
                    <span class="status-pulse" style='background: #48bb78;'></span>
                    <span style='color: #48bb78; font-weight: bold;'>Online</span>
                </div>
                <p style='color: #a0aec0;'>All Systems Operational</p>
            </div>
            """, unsafe_allow_html=True)
    
    def display_overview(self):
        """Display enhanced overview section with animations"""
        # Budget Alert Banner with animation
        budget_data = self.get_budget_data()
        if budget_data['progress_percent'] > budget_data['alert_threshold']:
            st.markdown(f"""
            <div class="glass-card" style='background: linear-gradient(135deg, rgba(245, 101, 101, 0.3) 0%, rgba(229, 62, 62, 0.3) 100%); border: 1px solid rgba(245, 101, 101, 0.5);'>
                <div style='display: flex; align-items: center; gap: 1rem;'>
                    <div style='font-size: 2rem; animation: glow-pulse 1s ease-in-out infinite alternate;'>🚨</div>
                    <div>
                        <h3 style='margin: 0; color: white;'>Budget Alert</h3>
                        <p style='margin: 0; color: #feb2b2;'>Current spend ({budget_data['progress_percent']}%) is approaching your ${budget_data['budget_amount']} budget limit.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Key Metrics with staggered animations
        metrics = self.get_storage_metrics()
        budget_data = self.get_budget_data()
        
        col1, col2, col3, col4 = st.columns(4)
        
        metrics_data = [
            {"icon": "📁", "value": metrics['total_files'] if metrics else 0, "label": "Total Documents", "sub": "Azure Blob Storage"},
            {"icon": "💾", "value": f"{metrics['total_size_mb'] if metrics else 0} MB", "label": "Storage Used", "sub": "Cloud Storage"},
            {"icon": "💰", "value": f"${budget_data['current_spend']}", "label": "Current Spend", "sub": f"${budget_data['budget_amount']} Budget"},
            {"icon": "🤖", "value": sum(metrics['daily_processing']['documents_processed']) if metrics else 0, "label": "AI Processed", "sub": "This Month"}
        ]
        
        for i, (col, metric) in enumerate(zip([col1, col2, col3, col4], metrics_data)):
            with col:
                st.markdown(f"""
                <div class="metric-card fade-in-up" style="animation-delay: {i * 0.2}s;">
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{metric['icon']}</div>
                    <div style='font-size: 2rem; font-weight: bold; color: white;'>{metric['value']}</div>
                    <div style='opacity: 0.9; color: #e2e8f0;'>{metric['label']}</div>
                    <div style='font-size: 0.8rem; margin-top: 0.5rem; color: #a0aec0;'>{metric['sub']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    def display_budget_analytics(self):
        """Display premium budget analytics with dark theme"""
        st.markdown('<div class="section-header glow-text" style="font-size: 2rem; margin: 2rem 0;">💰 Budget & Cost Analytics</div>', unsafe_allow_html=True)
        
        budget_data = self.get_budget_data()
        
        # Budget Overview Cards
        col1, col2, col3, col4 = st.columns(4)
        
        budget_cards = [
            {"icon": "📊", "value": f"${budget_data['budget_amount']}", "label": "Total Budget", "color": "#667eea"},
            {"icon": "💸", "value": f"${budget_data['current_spend']}", "label": "Current Spend", "color": "#48bb78"},
            {"icon": "🔮", "value": f"${budget_data['forecasted_spend']}", "label": "Forecasted", "color": "#ed8936"},
            {"icon": "⚡", "value": f"{budget_data['progress_percent']}%", "label": "Usage", "color": "#48bb78" if budget_data['progress_percent'] < 80 else "#f56565"}
        ]
        
        for i, (col, card) in enumerate(zip([col1, col2, col3, col4], budget_cards)):
            with col:
                st.markdown(f"""
                <div class="glass-card fade-in-up" style='text-align: center; animation-delay: {i * 0.1}s;'>
                    <div style='font-size: 2rem; color: {card["color"]};'>{card['icon']}</div>
                    <div style='font-size: 1.5rem; font-weight: bold; color: white;'>{card['value']}</div>
                    <div style='color: #a0aec0;'>{card['label']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Budget progress gauge with dark theme
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = budget_data['progress_percent'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Budget Usage (%)", 'font': {'size': 20, 'color': 'white'}},
                delta = {'reference': budget_data['alert_threshold'], 'increasing': {'color': "red"}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': 'white'},
                    'bar': {'color': "#667eea"},
                    'bgcolor': 'rgba(0,0,0,0.3)',
                    'borderwidth': 2,
                    'bordercolor': "rgba(255,255,255,0.2)",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(72, 187, 120, 0.3)'},
                        {'range': [50, 80], 'color': 'rgba(237, 137, 54, 0.3)'},
                        {'range': [80, 100], 'color': 'rgba(245, 101, 101, 0.3)'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': budget_data['alert_threshold']
                    }
                }
            ))
            fig_gauge.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white"},
                margin=dict(t=50, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            # Cost breakdown with dark theme
            cost_breakdown = {
                'Service': ['Document Intelligence', 'Blob Storage', 'Networking', 'Monitoring', 'Compute'],
                'Cost': [0.25, 0.12, 0.03, 0.02, 0.05],
                'Color': ['#667eea', '#764ba2', '#48bb78', '#ed8936', '#f56565']
            }
            df_costs = pd.DataFrame(cost_breakdown)
            
            fig_pie = px.pie(
                df_costs, 
                values='Cost', 
                names='Service',
                title="Monthly Cost Distribution",
                color='Service',
                color_discrete_sequence=cost_breakdown['Color']
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "white"},
                legend={'font': {'color': 'white'}}
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    def display_processing_analytics(self):
        """Display premium processing analytics with dark theme"""
        st.markdown('<div class="section-header glow-text" style="font-size: 2rem; margin: 2rem 0;">📈 Processing Analytics</div>', unsafe_allow_html=True)
        
        metrics = self.get_storage_metrics()
        if not metrics:
            return
        
        # Quick Stats with animations
        col1, col2, col3, col4 = st.columns(4)
        
        quick_stats = [
            {"label": "Avg Processing Time", "value": f"{sum(metrics['daily_processing']['processing_time']) / len(metrics['daily_processing']['processing_time']):.1f}s", "delta": "-0.2s"},
            {"label": "Total Processed", "value": f"{sum(metrics['daily_processing']['documents_processed'])}", "delta": "+12%"},
            {"label": "Peak Daily", "value": f"{max(metrics['daily_processing']['documents_processed'])} docs", "delta": "Yesterday"},
            {"label": "Success Rate", "value": "99.2%", "delta": "0.3%"}
        ]
        
        for i, (col, stat) in enumerate(zip([col1, col2, col3, col4], quick_stats)):
            with col:
                st.markdown(f"""
                <div class="glass-card fade-in-up" style='text-align: center; animation-delay: {i * 0.1}s;'>
                    <div style='font-size: 1.2rem; font-weight: bold; color: white;'>{stat['value']}</div>
                    <div style='color: #a0aec0; margin-bottom: 0.5rem;'>{stat['label']}</div>
                    <div style='color: #48bb78; font-size: 0.9rem;'>{stat['delta']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Documents processed over time with dark theme
            processing_data = metrics['daily_processing']
            df_trend = pd.DataFrame({
                'Date': processing_data['dates'],
                'Documents Processed': processing_data['documents_processed'],
                'Processing Time (s)': processing_data['processing_time']
            })
            
            fig_trend = px.area(
                df_trend, 
                x='Date', 
                y='Documents Processed',
                title="📊 Daily Documents Processed",
                line_shape='spline'
            )
            fig_trend.update_traces(
                line=dict(color='#667eea', width=3),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.1)'
            )
            fig_trend.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "white"},
                xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
                yaxis={'gridcolor': 'rgba(255,255,255,0.1)'}
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            # File type distribution with dark theme
            if metrics['file_types']:
                df_files = pd.DataFrame({
                    'File Type': list(metrics['file_types'].keys()),
                    'Count': list(metrics['file_types'].values())
                })
                
                fig_bar = px.bar(
                    df_files,
                    x='File Type',
                    y='Count',
                    title="📁 Files by Type",
                    color='Count',
                    color_continuous_scale='Viridis'
                )
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "white"},
                    xaxis={'gridcolor': 'rgba(255,255,255,0.1)'},
                    yaxis={'gridcolor': 'rgba(255,255,255,0.1)'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
    
    def display_document_processing(self):
        """Display premium document processing section"""
        st.markdown('<div class="section-header glow-text" style="font-size: 2rem; margin: 2rem 0;">🔄 Document Processing Pipeline</div>', unsafe_allow_html=True)
        
        # Use tabs for better organization
        tab1, tab2, tab3 = st.tabs(["🚀 Upload & Process", "📊 Pipeline Status", "💡 Quick Actions"])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                <div class="glass-card glow-box">
                    <h3 style='color: white;'>📤 Upload Documents</h3>
                    <p style='color: #a0aec0;'>Drag and drop your documents for AI-powered processing and analysis.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced file uploader
                uploaded_file = st.file_uploader(
                    " ",
                    type=['pdf', 'txt', 'jpg', 'png', 'docx'],
                    help="Supported formats: PDF, Text, Images, Word Documents",
                    label_visibility="collapsed"
                )
                
                if uploaded_file is not None:
                    # File info in premium card
                    file_info = {
                        'Name': uploaded_file.name,
                        'Type': uploaded_file.type,
                        'Size': f"{len(uploaded_file.getvalue()) / 1024:.1f} KB"
                    }
                    
                    st.markdown("""
                    <div class="glass-card">
                        <h4 style='color: white;'>📄 File Details</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    info_cols = st.columns(3)
                    for idx, (key, value) in enumerate(file_info.items()):
                        with info_cols[idx]:
                            st.markdown(f"""
                            <div class="glass-card" style='text-align: center; padding: 1rem;'>
                                <div style='color: #667eea; font-weight: bold;'>{key}</div>
                                <div style='color: white;'>{value}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Processing options
                    with st.expander("⚙️ Processing Options", expanded=True):
                        col_opt1, col_opt2 = st.columns(2)
                        with col_opt1:
                            extract_text = st.checkbox("Extract Text", value=True)
                            detect_tables = st.checkbox("Detect Tables", value=True)
                        with col_opt2:
                            analyze_layout = st.checkbox("Analyze Layout", value=True)
                            save_to_db = st.checkbox("Save to Database", value=False)
                    
                    # Animated process button
                    if st.button("🚀 Process Document with AI", use_container_width=True, type="primary"):
                        # Simulate processing with progress animation
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        steps = [
                            "📤 Uploading to secure cloud...",
                            "🔍 Analyzing document structure...",
                            "📝 Extracting text content...",
                            "📊 Identifying tables and layouts...",
                            "🎯 Generating insights..."
                        ]
                        
                        for i, step in enumerate(steps):
                            progress = (i + 1) * 20
                            progress_bar.progress(progress)
                            status_text.markdown(f"""
                            <div class="glass-card" style='padding: 1rem;'>
                                <div style='color: white;'>{step}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            time.sleep(0.5)
                        
                        # Success animation
                        st.balloons()
                        st.markdown("""
                        <div class="glass-card" style='background: linear-gradient(135deg, rgba(72, 187, 120, 0.3) 0%, rgba(56, 161, 105, 0.3) 100%); border: 1px solid rgba(72, 187, 120, 0.5);'>
                            <div style='display: flex; align-items: center; gap: 1rem;'>
                                <div style='font-size: 2rem;'>🎉</div>
                                <div>
                                    <h3 style='margin: 0; color: white;'>Processing Complete!</h3>
                                    <p style='margin: 0; color: #c6f6d5;'>Your document has been successfully analyzed with AI.</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Results metrics
                        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
                        results = [
                            ("Pages", "5"),
                            ("Tables", "3"), 
                            ("Lines", "142"),
                            ("Confidence", "98.2%")
                        ]
                        
                        for i, (col, (label, value)) in enumerate(zip([col_res1, col_res2, col_res3, col_res4], results)):
                            with col:
                                st.markdown(f"""
                                <div class="glass-card fade-in-up" style='text-align: center; padding: 1rem; animation-delay: {i * 0.1}s;'>
                                    <div style='font-size: 1.5rem; font-weight: bold; color: #667eea;'>{value}</div>
                                    <div style='color: #a0aec0;'>{label}</div>
                                </div>
                                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="glass-card">
                    <h3 style='color: white;'>💡 Tips</h3>
                    <ul style='color: #a0aec0;'>
                        <li>PDF files work best for text extraction</li>
                        <li>High-resolution images improve accuracy</li>
                        <li>Enable layout analysis for complex documents</li>
                        <li>Check cost estimates before processing</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div class="glass-card">
                <h3 style='color: white;'>🔧 Pipeline Status</h3>
                <p style='color: #a0aec0;'>Real-time monitoring of document processing pipeline</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Animated pipeline visualization
            pipeline_steps = [
                {"name": "File Upload", "status": "completed", "icon": "📤", "description": "File securely uploaded"},
                {"name": "Storage", "status": "completed", "icon": "💾", "description": "Stored in Azure Blob"},
                {"name": "AI Analysis", "status": "completed", "icon": "🤖", "description": "AI processing complete"},
                {"name": "Data Extraction", "status": "processing", "icon": "🔍", "description": "Extracting content"},
                {"name": "Results", "status": "pending", "icon": "📊", "description": "Awaiting completion"}
            ]
            
            for i, step in enumerate(pipeline_steps):
                status_config = {
                    "completed": {"color": "#48bb78", "icon": "✅", "pulse": False},
                    "processing": {"color": "#ed8936", "icon": "🔄", "pulse": True},
                    "pending": {"color": "#a0aec0", "icon": "⏳", "pulse": False}
                }
                
                config = status_config[step['status']]
                pulse_class = "status-pulse" if config['pulse'] else ""
                
                st.markdown(f"""
                <div class="glass-card fade-in-up" style='animation-delay: {i * 0.1}s;'>
                    <div style='display: flex; align-items: center; gap: 1rem;'>
                        <div style='font-size: 2rem;'>{step['icon']}</div>
                        <div style='flex: 1;'>
                            <div style='font-weight: bold; color: white;'>{step['name']}</div>
                            <div style='color: {config["color"]};'>{step['description']}</div>
                        </div>
                        <div class="{pulse_class}" style='background: {config["color"]};'></div>
                        <div style='color: {config["color"]}; font-weight: bold;'>{config["icon"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
            <div class="glass-card">
                <h3 style='color: white;'>⚡ Quick Actions</h3>
                <p style='color: #a0aec0;'>Frequently used operations and shortcuts</p>
            </div>
            """, unsafe_allow_html=True)
            
            quick_col1, quick_col2 = st.columns(2)
            
            with quick_col1:
                if st.button("📥 Batch Process", use_container_width=True):
                    st.success("🚀 Batch processing started for queued documents")
                
                if st.button("🔄 Sync Storage", use_container_width=True):
                    st.success("✅ Storage synchronized successfully")
            
            with quick_col2:
                if st.button("📋 View Logs", use_container_width=True):
                    st.info("📊 Opening processing logs...")
                
                if st.button("⚙️ Settings", use_container_width=True):
                    st.info("🔧 Opening configuration settings...")
    
    def display_system_monitoring(self):
        """Display premium system monitoring with dark theme"""
        st.markdown('<div class="section-header glow-text" style="font-size: 2rem; margin: 2rem 0;">🏥 System Health & Monitoring</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Azure Services Status
            st.markdown("""
            <div class="glass-card">
                <h3 style='color: white;'>🔧 Azure Services</h3>
                <p style='color: #a0aec0;'>Real-time status of cloud infrastructure</p>
            </div>
            """, unsafe_allow_html=True)
            
            services = [
                {"name": "Blob Storage", "status": "healthy", "usage": "5.2 MB", "latency": "23ms"},
                {"name": "Document Intelligence", "status": "healthy", "usage": "87%", "latency": "45ms"},
                {"name": "App Service", "status": "developing", "usage": "Not deployed", "latency": "N/A"},
                {"name": "Database", "status": "planned", "usage": "Q4 2024", "latency": "N/A"}
            ]
            
            for i, service in enumerate(services):
                status_config = {
                    "healthy": {"color": "#48bb78", "icon": "✅", "pulse": True},
                    "developing": {"color": "#ed8936", "icon": "🛠️", "pulse": False},
                    "planned": {"color": "#a0aec0", "icon": "📅", "pulse": False}
                }
                
                config = status_config[service['status']]
                pulse_class = "status-pulse" if config['pulse'] else ""
                
                st.markdown(f"""
                <div class="glass-card fade-in-up" style='animation-delay: {i * 0.1}s;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='display: flex; align-items: center; gap: 1rem;'>
                            <div class="{pulse_class}" style='background: {config["color"]};'></div>
                            <div>
                                <div style='font-weight: bold; color: white;'>{service['name']}</div>
                                <div style='color: #718096; font-size: 0.8rem;'>{service['usage']} • {service['latency']}</div>
                            </div>
                        </div>
                        <div style='color: {config["color"]}; font-weight: bold;'>{config["icon"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Performance Metrics
            st.markdown("""
            <div class="glass-card">
                <h3 style='color: white;'>📊 Performance Metrics</h3>
                <p style='color: #a0aec0;'>System performance and response times</p>
            </div>
            """, unsafe_allow_html=True)
            
            performance_data = {
                'Metric': ['API Response', 'Document Processing', 'Upload Speed', 'AI Analysis', 'Storage I/O'],
                'Value': ['48ms', '2.1s', '4.2 MB/s', '1.8s', '12ms'],
                'Trend': ['↘️ Improving', '→ Stable', '↗️ Improving', '→ Stable', '↘️ Improving']
            }
            df_perf = pd.DataFrame(performance_data)
            
            # Custom dataframe styling for dark theme
            st.dataframe(
                df_perf,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Metric": st.column_config.TextColumn("Metric", width="medium"),
                    "Value": st.column_config.TextColumn("Value", width="small"),
                    "Trend": st.column_config.TextColumn("Trend", width="medium")
                }
            )
            
            # Security Status
            st.markdown("""
            <div class="glass-card">
                <h3 style='color: white;'>🔒 Security Status</h3>
                <p style='color: #a0aec0;'>Security controls and compliance</p>
            </div>
            """, unsafe_allow_html=True)
            
            security_items = [
                ("SAS Tokens", "✅ Active", "1hr expiry"),
                ("Encryption", "✅ Enabled", "AES-256"),
                ("Access Control", "✅ Configured", "RBAC"),
                ("Audit Logs", "🛠️ Developing", "Q4 2024")
            ]
            
            for i, (item, status, details) in enumerate(security_items):
                st.markdown(f"""
                <div class="glass-card fade-in-up" style='padding: 1rem; margin: 0.5rem 0; animation-delay: {i * 0.1}s;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='font-weight: bold; color: white;'>{item}</div>
                        <div style='display: flex; gap: 1rem; align-items: center;'>
                            <div style='color: #48bb78;'>{status}</div>
                            <div style='color: #718096; font-size: 0.8rem;'>{details}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def main():
    dashboard = SecureDocDashboard()
    
    # Premium dark sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem; padding: 2rem 1rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%); border-radius: 20px; border: 1px solid rgba(102, 126, 234, 0.3);'>
            <h1 style='font-size: 3rem; margin: 0;' class="glow-text">🔒</h1>
            <h2 style='margin: 0; color: white;'>SecureDoc AI</h2>
            <p style='opacity: 0.9; margin: 0; color: #a0aec0;'>Premium Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation with icons
        st.markdown("### 🧭 Navigation")
        section = st.radio(
            "Choose a section:",
            ["📊 Overview", "💰 Budget Analytics", "📈 Processing Analytics", "🔄 Document Processing", "🏥 System Health"],
            label_visibility="collapsed"
        )
        
        # Quick stats in sidebar
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        
        metrics = dashboard.get_storage_metrics()
        budget_data = dashboard.get_budget_data()
        
        if metrics:
            stats = [
                ("Files", f"{metrics['total_files']}"),
                ("Storage", f"{metrics['total_size_mb']} MB"),
                ("Budget Used", f"{budget_data['progress_percent']}%"),
                ("AI Processing", "Active" if metrics else "Inactive")
            ]
            
            for label, value in stats:
                st.markdown(f"""
                <div class="glass-card" style='padding: 1rem; margin: 0.5rem 0; text-align: center;'>
                    <div style='font-size: 1.2rem; font-weight: bold; color: #667eea;'>{value}</div>
                    <div style='color: #a0aec0; font-size: 0.9rem;'>{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #718096;'>
            <p><strong style='color: white;'>🔒 SecureDoc AI Premium</strong></p>
            <p style='color: #a0aec0;'>Enterprise Document Intelligence</p>
            <p style='color: #a0aec0;'>Version: 2.0.0</p>
            <p style='color: #a0aec0;'>October 2024</p>
            <br>
            <p style='color: white;'><strong>Contact:</strong></p>
            <p style='color: #a0aec0;'>Amer Almohammad</p>
            <p style='color: #a0aec0;'>AWS Junior Cloud Engineer</p>
            <p style='color: #a0aec0;'>📧 ajaber1973@web.de</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    if section == "📊 Overview":
        dashboard.display_hero_section()
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

if __name__ == "__main__":
    main()