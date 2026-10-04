html = open('index.html', 'r', encoding='utf-8').read()
html = html.replace('<button class="btn btn-primary" id="btn-run-analysis"', '<button id="btn-calc-ndvi" style="display:none;"></button>\n          <button class="btn btn-primary" id="btn-run-analysis"')
open('index.html', 'w', encoding='utf-8').write(html)
