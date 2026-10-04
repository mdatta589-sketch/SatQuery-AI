with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()
import re
print(re.search(r'function calcNDVI.*?\{.*?(fetch\([^)]+\)).*?\}', js, re.DOTALL))
