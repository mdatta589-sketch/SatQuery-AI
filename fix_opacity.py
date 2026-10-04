with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

content = content.replace("const imgOverlay = L.imageOverlay(evData, KANCHA_AOI, {opacity: 0.65, interactive: false});", "const imgOverlay = L.imageOverlay(evData, KANCHA_AOI, {opacity: 1.0, interactive: false});")

content = content.replace("const imgOverlay = L.imageOverlay(evData, changeEv.bounds, {opacity: 0.65, interactive: false});", "const imgOverlay = L.imageOverlay(evData, changeEv.bounds, {opacity: 1.0, interactive: false});")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED OPACITY")
