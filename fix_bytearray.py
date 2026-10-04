with open('backend/app/api/export.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("return Response(content=pdf_bytes", "return Response(content=bytes(pdf_bytes)")

with open('backend/app/api/export.py', 'w', encoding='utf-8') as f:
    f.write(content)
