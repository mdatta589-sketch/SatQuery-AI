with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()
import re
match = re.search(r"const changeEv =(.*?)\} else if \(!ansText\)", content, flags=re.DOTALL)
if match:
    print(match.group(0))
