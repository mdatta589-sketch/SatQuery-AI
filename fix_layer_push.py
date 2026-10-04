with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

content = content.replace("layers.push(layerMeta);", "layers.push(layerMeta);\n        if (typeof updateChangeAnalysisDropdowns === 'function') updateChangeAnalysisDropdowns();")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("ADDED LAYER LISTENER")
