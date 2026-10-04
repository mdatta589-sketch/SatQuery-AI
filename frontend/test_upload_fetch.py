import sys
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find("document.getElementById('geotiff-upload').addEventListener('change'")
end = js.find('catch (err)', start)
sys.stdout.reconfigure(encoding='utf-8')
print(js[start:end])
