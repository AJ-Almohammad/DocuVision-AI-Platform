#!/usr/bin/env python3
"""
Create a proper PDF test file for Document Intelligence
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_technical_report_pdf():
    """Create a sample TÜV SÜD technical report PDF"""
    filename = "sample_technical_report.pdf"
    
    # Create a PDF document
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Set title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "TÜV SÜD TECHNICAL REPORT")
    
    # Add report details
    c.setFont("Helvetica", 12)
    y_position = height - 140
    
    report_data = [
        ("Report ID:", "TR-2024-001"),
        ("Product:", "Safety Helmet Model X"),
        ("Test Date:", "2024-10-01"),
        ("Inspector:", "Dr. Schmidt"),
        ("Result:", "PASS"),
        ("", ""),
        ("Notes:", "All safety standards met."),
        ("", "Impact resistance exceeds requirements."),
        ("", ""),
        ("Additional Tests:", ""),
        ("- Temperature Resistance:", "PASS"),
        ("- Durability:", "PASS"),
        ("- Material Quality:", "PASS")
    ]
    
    for label, value in report_data:
        c.drawString(100, y_position, f"{label} {value}")
        y_position -= 25
    
    # Add a simple table
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position - 40, "Test Results Summary:")
    
    c.setFont("Helvetica", 10)
    table_data = [
        ["Test", "Standard", "Result", "Value"],
        ["Impact", "EN 397", "PASS", ">5000 N"],
        ["Penetration", "EN 397", "PASS", "No penetration"],
        ["Flammability", "EN 397", "PASS", "Self-extinguishing"]
    ]
    
    table_y = y_position - 80
    for row in table_data:
        x_pos = 100
        for cell in row:
            c.drawString(x_pos, table_y, cell)
            x_pos += 120
        table_y -= 20
    
    # Save the PDF
    c.save()
    print(f"✅ Created PDF: {filename}")
    print(f"📄 File size: {os.path.getsize(filename)} bytes")
    
    return filename

if __name__ == "__main__":
    create_technical_report_pdf()