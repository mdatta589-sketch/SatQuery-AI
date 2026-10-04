with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re

old_decl = """let changeAnalysisMode = "live";"""
new_decl = """let changeAnalysisMode = "live";
let changeBeforeLayer = null;
let changeAfterLayer = null;
let changeOverlayLayer = null;"""

content = content.replace(old_decl, new_decl)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("ADDED GLOBALS")
