import sys
import re
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = '''
document.getElementById('vqa-execution').textContent = Scope: \\nTask: \\nModel: \\nProvider: \\nStatus: \\nGrounding Provider: \\nGrounding Status: ;
'''

js = re.sub(r'document\.getElementById\(\'vqa-execution\'\)\.textContent = Task: \$\{data\.task\}\\nModel: \$\{data\.execution\?\.model \|\| \'None\'\}\\nProvider: \$\{data\.execution\?\.provider \|\| \'Unknown\'\}\\nStatus: \$\{data\.execution\?\.status \|\| \'Unknown\'\}\\nGrounding Provider: \$\{gProvider\}\\nGrounding Status: \$\{gStatus\};', replacement.strip(), js, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
