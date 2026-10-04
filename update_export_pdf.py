with open('backend/app/api/export.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("pdf.multi_cell(0, 6", "pdf.multi_cell(190, 6")
content = content.replace("pdf.cell(0, 6", "pdf.cell(190, 6")
content = content.replace("pdf.cell(0, 8", "pdf.cell(190, 8")

with open('backend/app/api/export.py', 'w', encoding='utf-8') as f:
    f.write(content)
