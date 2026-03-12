"""
Resume Parser Module
Extracts text content from uploaded PDF resume files using pdfplumber.
"""

import pdfplumber


def extract_text_from_pdf(pdf_file):
    """
    Extract all text from a PDF file.

    Args:
        pdf_file: A file-like object (e.g., uploaded via Streamlit).

    Returns:
        str: The extracted text from all pages of the PDF.
    """
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()
