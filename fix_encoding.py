import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("kmA", "km²")
js = js.replace("kmA\ufffd", "km²")

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
