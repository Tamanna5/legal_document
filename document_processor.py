import re
import os
import pdfplumber
import docx
import nltk
from nltk.tokenize import sent_tokenize

def load_document(file_path):
    """Load document from various formats (PDF, DOCX, TXT)"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    
    elif file_extension == '.docx':
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

def preprocess_text(text):
    """Preprocess the legal text for better analysis"""
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove page numbers if any (common in legal docs)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    # Replace common legal abbreviations
    legal_abbreviations = {
        "i.e.": "that is",
        "e.g.": "for example",
        "viz.": "namely",
        "vs.": "versus",
    }
    
    for abbr, full_form in legal_abbreviations.items():
        text = text.replace(abbr, full_form)
    
    return text

def split_into_sections(text):
    """Split legal document into logical sections"""
    # Look for common section patterns in legal documents
    section_patterns = [
        r'(?:\n|^)([A-Z][A-Z\s]+:)',  # ALL CAPS HEADINGS:
        r'(?:\n|^)(\d+\.\s+[A-Z][^.]+)',  # Numbered sections
        r'(?:\n|^)(ARTICLE\s+[IVX]+)',  # ARTICLE I, ARTICLE II, etc.
        r'(?:\n|^)(Section\s+\d+)',  # Section 1, Section 2, etc.
    ]
    
    sections = []
    last_pos = 0
    current_heading = "PREAMBLE"
    
    # Combine all patterns
    combined_pattern = '|'.join(section_patterns)
    
    for match in re.finditer(combined_pattern, text):
        if last_pos > 0:  # Not the first match
            section_text = text[last_pos:match.start()].strip()
            sections.append({"heading": current_heading, "content": section_text})
        
        current_heading = match.group(1).strip()
        last_pos = match.start()
    
    # Add the last section
    if last_pos < len(text):
        section_text = text[last_pos:].strip()
        sections.append({"heading": current_heading, "content": section_text})
    
    return sections 