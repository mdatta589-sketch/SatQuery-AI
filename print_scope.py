with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()
import re
match = re.search(r"data = await routeRes\.json\(\);\s*\}(.*?)\s*document\.getElementById\('header-status'\)", content, flags=re.DOTALL)
if match:
    print(match.group(1))
