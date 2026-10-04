import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

content = content.replace("const imgOverlay = L.imageOverlay(evData, data.bounds, {opacity: 0.65, interactive: false});", "const imgOverlay = L.imageOverlay(evData, changeEv.bounds, {opacity: 0.65, interactive: false});")

content = content.replace("const rect = L.rectangle(data.bounds, {color: '#ef4444', weight: 2, fill: false});", "const rect = L.rectangle(changeEv.bounds, {color: '#ef4444', weight: 2, fill: false});")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED BOUNDS")
