import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

old_fetch = '''async function loggedFetch(url, options) {
    console.log("SATQUERY FETCH URL:", url);
    console.log("SATQUERY FETCH METHOD:", options.method || 'GET');
    console.log("SATQUERY FETCH BODY:", options.body);
    const response = await fetch(url, options);'''

new_fetch = '''async function loggedFetch(url, options = {}) {
    console.log("SATQUERY FETCH URL:", url);
    console.log("SATQUERY FETCH METHOD:", options.method || 'GET');
    console.log("SATQUERY FETCH BODY:", options.body);
    const response = await fetch(url, options);'''

if old_fetch in content:
    content = content.replace(old_fetch, new_fetch)
    with open('frontend/app.js', 'w', encoding='utf8') as f:
        f.write(content)
    print("REPLACED")
else:
    print("NOT FOUND")
