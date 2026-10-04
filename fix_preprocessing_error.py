with open('backend/app/models/vqa/preprocessing.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
content = content.replace(
    'raise ValueError("AOI is outside the raster bounds.")',
    'raise ValueError("Selected AOI does not overlap the selected raster.")'
)

with open('backend/app/models/vqa/preprocessing.py', 'w', encoding='utf-8') as f:
    f.write(content)
