from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

def generate_pdf_summary(analysis_results, output_path):
    """Generate a PDF summary of the legal document analysis"""
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50'),
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#2c3e50'),
        borderWidth=1,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=5,
        borderRadius=5
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.HexColor('#34495e')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        leftIndent=20,
        spaceAfter=4
    )

    # Build the content
    content = []

    # Title and timestamp
    content.append(Paragraph("Legal Document Analysis Summary", title_style))
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                           ParagraphStyle('Timestamp', parent=normal_style, alignment=1)))
    content.append(Spacer(1, 30))

    # Document Summary
    content.append(Paragraph("Document Summary", heading_style))
    content.append(Paragraph(analysis_results['document_summary'], normal_style))
    content.append(Spacer(1, 20))

    # Key Legal Entities
    content.append(Paragraph("Key Legal Entities", heading_style))
    for entity_type, entities in analysis_results['entities'].items():
        if entities:
            content.append(Paragraph(f"{entity_type.title()}", subheading_style))
            for entity in entities[:5]:  # Show top 5 entities
                content.append(Paragraph(f"• {entity}", bullet_style))
            if len(entities) > 5:
                content.append(Paragraph(f"... and {len(entities) - 5} more", normal_style))
            content.append(Spacer(1, 10))
    content.append(Spacer(1, 20))

    # Key Clauses
    content.append(Paragraph("Key Clauses", heading_style))
    for clause_type, clauses in analysis_results['key_clauses'].items():
        content.append(Paragraph(f"{clause_type.replace('_', ' ').title()}", subheading_style))
        for clause in clauses[:2]:  # Show top 2 clauses
            content.append(Paragraph(f"• {clause[:200]}...", bullet_style))
        if len(clauses) > 2:
            content.append(Paragraph(f"... and {len(clauses) - 2} more instances", normal_style))
        content.append(Spacer(1, 10))
    content.append(Spacer(1, 20))

    # Obligations and Rights
    content.append(Paragraph("Obligations and Rights", heading_style))
    
    # Obligations
    content.append(Paragraph("Obligations:", subheading_style))
    for obligation in analysis_results['obligations_and_rights']['obligations'][:5]:
        content.append(Paragraph(f"• {obligation['text']}", bullet_style))
    if len(analysis_results['obligations_and_rights']['obligations']) > 5:
        content.append(Paragraph(f"... and {len(analysis_results['obligations_and_rights']['obligations']) - 5} more obligations", normal_style))
    
    content.append(Spacer(1, 10))
    
    # Rights
    content.append(Paragraph("Rights:", subheading_style))
    for right in analysis_results['obligations_and_rights']['rights'][:5]:
        content.append(Paragraph(f"• {right['text']}", bullet_style))
    if len(analysis_results['obligations_and_rights']['rights']) > 5:
        content.append(Paragraph(f"... and {len(analysis_results['obligations_and_rights']['rights']) - 5} more rights", normal_style))
    
    content.append(Spacer(1, 20))

    # Section Summaries
    content.append(Paragraph("Section Summaries", heading_style))
    for section in analysis_results['section_summaries']:
        content.append(Paragraph(f"{section['heading']}", subheading_style))
        content.append(Paragraph(section['summary'], normal_style))
        content.append(Spacer(1, 10))

    # Footer
    content.append(PageBreak())
    content.append(Paragraph("Generated by Legal Document Analyzer", 
                           ParagraphStyle('Footer', parent=normal_style, alignment=1)))

    # Build the PDF
    doc.build(content) 