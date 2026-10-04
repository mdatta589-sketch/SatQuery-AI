with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re
match = re.search(r"if \(btnQueryPanel\) \{\s*btnQueryPanel\.addEventListener\('click', async \(\) => \{(.*?)\}\);\s*\}", content, flags=re.DOTALL)
if match:
    with open('extract.js', 'w', encoding='utf8') as out:
        out.write(match.group(0))
    print("EXTRACTED")
else:
    print("NOT FOUND")
