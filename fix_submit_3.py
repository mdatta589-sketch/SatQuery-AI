import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

match = re.search(r"\s*const data = await res\.json\(\);\s*if \(\!res\.ok\) \{\s*throw new Error\(data\.detail \|\| data\.error \|\| `HTTP Error \$\{res\.status\}`\);\s*\}", content)
if match:
    content = content[:match.start()] + content[match.end():]
    print("REMOVED OLD RES PARSE")
else:
    print("NOT FOUND OLD RES PARSE")

# Remove extra closing brace that got left behind
content = content.replace("data = await routeRes.json();\n            }\n            }", "data = await routeRes.json();\n            }")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
