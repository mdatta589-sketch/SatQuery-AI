import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

count = content.count("updateChangeAnalysisDropdowns")
print(f"COUNT: {count}")

# Let's add it to processGeoTIFF (upload) and STAC load
content = content.replace(
    "layers.push(layerMeta);",
    "layers.push(layerMeta);\n    updateChangeAnalysisDropdowns();"
)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
