import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# Force the change analysis selectors to always be visible on load
fix = """
    // FORCE case study selectors to be visible immediately
    const selectors = document.getElementById('change-analysis-selectors');
    const msg = document.getElementById('change-analysis-message');
    if (selectors) selectors.style.display = 'flex';
    if (msg) msg.style.display = 'none';
"""

content = re.sub(r'updateNoDataState\(\);\s*\}\);', r'updateNoDataState();' + fix + r'\n});', content)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED VISIBILITY PROPERLY")
