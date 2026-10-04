content = open('frontend/styles.css', 'r', encoding='utf8').read()
content = content.replace('.main-layout {', '.app-body {')
open('frontend/styles.css', 'w', encoding='utf8').write(content)
print('REPLACED')
