
import os
import re
from PyPDF2 import PdfReader
import docx

def extract_text_from_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.txt':
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    elif ext == '.pdf':
        try:
            reader = PdfReader(path)
            texts = []
            for page in reader.pages:
                texts.append(page.extract_text() or '')
            return '\n'.join(texts)
        except Exception as e:
            return ''
    elif ext in ('.docx', '.doc'):
        try:
            doc = docx.Document(path)
            return '\n'.join(p.text for p in doc.paragraphs)
        except Exception as e:
            return ''
    else:
        # Unknown type: try to read as text
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            return ''
