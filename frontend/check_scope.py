import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find('function updateAOIPanel')
print("Position of updateAOIPanel:", start)
domcontentloaded = js.find('document.addEventListener(\'DOMContentLoaded\'')
print("Position of DOMContentLoaded:", domcontentloaded)
end_dom = js.find('});', domcontentloaded)
print("End of DOMContentLoaded:", end_dom)
