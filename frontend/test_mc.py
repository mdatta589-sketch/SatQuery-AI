import re
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

assignments = re.findall(r'(mcFit|mcLayers|mcDraw|mcPixel|stacCloudCover)\s*=\s*document\.getElementById\([\'"](.*?)[\'"]\)', js)
print(assignments)
