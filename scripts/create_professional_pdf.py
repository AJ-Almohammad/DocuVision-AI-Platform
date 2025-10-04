#!/usr/bin/env python3
"""
Create professional technical report PDF for demo purposes
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import os

def create_professional_technical_report():
    """Create a professional technical report PDF"""
    filename = "professional_technical_report.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1,  # Center
        textColor=colors.HexColor('#1a365d')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        textColor=colors.HexColor('#2d3748')
    )
    
    # Title
    title = Paragraph("TECHNICAL COMPLIANCE REPORT", title_style)
    story.append(title)
    
    # Report metadata
    metadata = [
        ["Report ID:", "TR-QA-2024-089"],
        ["Document Type:", "Safety Compliance Certificate"],
        ["Product:", "Industrial Safety Helmet Pro-X900"],
        ["Manufacturer:", "SafeTech Industries GmbH"],
        ["Test Date:", datetime.now().strftime("%Y-%m-%d")],
        ["Inspector:", "Dr. Michael Weber, Senior Safety Engineer"],
        ["Standard:", "EN 397:2012 + A1:2023"],
        ["Validity:", "24 months from issue date"]
    ]
    
    # Create metadata table
    metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f7fafc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0'))
    ]))
    
    story.append(metadata_table)
    story.append(Spacer(1, 20))
    
    # Executive Summary
    summary_heading = Paragraph("EXECUTIVE SUMMARY", heading_style)
    story.append(summary_heading)
    
    summary_text = """
    This report documents the comprehensive testing and evaluation of the Industrial Safety Helmet Pro-X900 
    in accordance with European Standard EN 397:2012. The helmet has successfully passed all mandatory 
    safety tests including impact resistance, penetration resistance, flammability, and electrical insulation. 
    All test results meet or exceed the requirements specified in the standard.
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Test Results
    results_heading = Paragraph("TEST RESULTS SUMMARY", heading_style)
    story.append(results_heading)
    
    test_results = [
        ["Test Parameter", "Standard Requirement", "Test Result", "Status"],
        ["Impact Resistance", "≤ 5000 N", "3850 N", "PASS"],
        ["Penetration Test", "No contact with headform", "No contact", "PASS"],
        ["Flammability", "≤ 5 seconds after flame", "2 seconds", "PASS"],
        ["Electrical Insulation", "1200 V AC, 1 minute", "No breakdown", "PASS"],
        ["Chin Strap Strength", "≥ 150 N", "245 N", "PASS"],
        ["Temperature Resistance", "-20°C to +50°C", "No degradation", "PASS"]
    ]
    
    results_table = Table(test_results, colWidths=[1.5*inch, 1.8*inch, 1.2*inch, 1*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d3748')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('BACKGROUND', (3, 1), (3, -1), colors.HexColor('#c6f6d5'))
    ]))
    
    story.append(results_table)
    story.append(Spacer(1, 20))
    
    # Additional Notes
    notes_heading = Paragraph("TECHNICAL NOTES", heading_style)
    story.append(notes_heading)
    
    notes_text = """
    • The helmet demonstrated exceptional impact absorption capabilities, with results 23% better than required.
    • Material quality and workmanship meet high industry standards.
    • All safety labels and markings are clearly visible and permanent.
    • The adjustment system provides secure and comfortable fit across various head sizes.
    • Recommended for industrial, construction, and manufacturing environments.
    """
    story.append(Paragraph(notes_text, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Conclusion
    conclusion_heading = Paragraph("CONCLUSION", heading_style)
    story.append(conclusion_heading)
    
    conclusion_text = """
    Based on the comprehensive testing conducted, the Industrial Safety Helmet Pro-X900 manufactured by 
    SafeTech Industries GmbH fully complies with the requirements of EN 397:2012 + A1:2023. The product 
    is certified for use in industrial environments where head protection is required. This certificate 
    is valid for 24 months from the date of issue.
    """
    story.append(Paragraph(conclusion_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Created professional PDF: {filename}")
    print(f"📄 File size: {os.path.getsize(filename)} bytes")
    
    return filename

if __name__ == "__main__":
    create_professional_technical_report()