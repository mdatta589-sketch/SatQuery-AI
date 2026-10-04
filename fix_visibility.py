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

content = content.replace("updateNoDataState();\n  });", "updateNoDataState();" + fix + "\n  });")

# And fix updateChangeAnalysisDropdowns so it doesn't hide them again
content = content.replace("if (msg) msg.style.display = 'block';\n        if (selectors) selectors.style.display = 'none';", "if (msg) msg.style.display = 'none';\n        if (selectors) selectors.style.display = 'flex';")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED VISIBILITY")
