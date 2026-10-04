content = open('frontend/styles.css', 'r', encoding='utf8').read()
old = '''body {
  grid-row: 2;
  display: grid;
  grid-template-columns: 280px 1fr 320px;
  overflow: hidden;
}'''
new = '''.main-layout {
  grid-row: 2;
  display: grid;
  grid-template-columns: 280px 1fr 320px;
  overflow: hidden;
}'''
if old in content:
    content = content.replace(old, new)
    open('frontend/styles.css', 'w', encoding='utf8').write(content)
    print('REPLACED')
else:
    print('NOT FOUND')
