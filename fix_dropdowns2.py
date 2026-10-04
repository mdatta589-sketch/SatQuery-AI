import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

content = re.sub(r'if \(msg\) msg\.style\.display = \'block\';\s*if \(selectors\) selectors\.style\.display = \'none\';', r'if (msg) msg.style.display = \'none\';\n        if (selectors) selectors.style.display = \'flex\';', content)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED DROPDOWNS PROPERLY")
