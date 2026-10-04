with open('backend/app/api/export.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

def safe_string(text):
    return text.encode('latin-1', 'replace').decode('latin-1')

# We can just replace the multi_cell and cell calls to sanitize the string.
# But an easier way is to just define a wrapper function in the file.
target = "class PDF(FPDF):"
replacement = """def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    # Replaces unmappable characters with ?
    return text.encode('windows-1252', 'replace').decode('windows-1252')

class PDF(FPDF):"""
content = content.replace(target, replacement)

content = re.sub(r'pdf\.cell\(190, 6, (f".*?"), ln=True\)', r'pdf.cell(190, 6, clean_text(\1), ln=True)', content)
content = re.sub(r'pdf\.multi_cell\(190, 6, (f".*?")\)', r'pdf.multi_cell(190, 6, clean_text(\1))', content)

with open('backend/app/api/export.py', 'w', encoding='utf-8') as f:
    f.write(content)
