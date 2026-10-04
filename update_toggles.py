with open('frontend/index.html', 'r', encoding='utf8') as f:
    content = f.read()

content = content.replace('<div id="cross-modal-selectors" style="padding: 10px;', '<div id="cross-modal-selectors" style="display: none; padding: 10px;')

with open('frontend/index.html', 'w', encoding='utf8') as f:
    f.write(content)

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# Add to toggle:
import re
content = re.sub(r"document\.getElementById\('change-analysis-selectors'\)\.style\.display = 'flex';", 
                 "document.getElementById('change-analysis-selectors').style.display = 'block';\n        document.getElementById('cross-modal-selectors').style.display = 'block';", content)

content = re.sub(r"if \(selectors\) selectors\.style\.display = 'flex';",
                 "if (selectors) selectors.style.display = 'block';\n    const cmSelectors = document.getElementById('cross-modal-selectors');\n    if (cmSelectors) cmSelectors.style.display = 'block';", content)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("Updated UI toggles")
