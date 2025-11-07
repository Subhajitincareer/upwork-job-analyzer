"""PDF Report Generator"""

from fpdf import FPDF
from datetime import datetime
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Upwork Job Analysis Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, datetime.now().strftime('%d %B %Y, %I:%M %p'), 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(analysis_text, job_count):
    """
    Generate PDF report
    
    Args:
        analysis_text: Analysis from Gemini
        job_count: Number of jobs analyzed
        
    Returns:
        PDF filename
    """
    pdf = PDFReport()
    pdf.add_page()
    
    # Summary
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Total Jobs Analyzed: {job_count}', 0, 1)
    pdf.ln(5)
    
    # Analysis content
    pdf.set_font('Arial', '', 10)
    
    # Clean text for PDF
    clean_text = analysis_text.replace('##', '').replace('**', '')
    
    # Add text
    pdf.multi_cell(0, 5, clean_text)
    
    # Save
    filename = f"data/reports/upwork_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    
    return filename

