with open('backend/app/api/catalog.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'raise HTTPException(status_code=400, detail="AOI is outside scene bounds")',
    'raise HTTPException(status_code=400, detail="Selected AOI does not overlap the selected raster.")'
)

with open('backend/app/api/catalog.py', 'w', encoding='utf-8') as f:
    f.write(content)
