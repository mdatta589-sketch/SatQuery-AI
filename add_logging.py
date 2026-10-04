import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# Add a helper function for logging
logging_helper = '''
async function loggedFetch(url, options) {
    console.log("SATQUERY FETCH URL:", url);
    console.log("SATQUERY FETCH METHOD:", options.method || 'GET');
    console.log("SATQUERY FETCH BODY:", options.body);
    const response = await fetch(url, options);
    console.log("SATQUERY RESPONSE STATUS:", response.status);
    console.log("SATQUERY RESPONSE URL:", response.url);
    return response;
}
'''
if 'async function loggedFetch' not in content:
    content = content.replace('// ==== Global State ====', '// ==== Global State ====\n' + logging_helper)

# Replace all fetch calls inside the btn-run-vqa click handler with loggedFetch
# First, change route fetch
content = content.replace(
    "const routeRes = await fetch('http://127.0.0.1:8000/api/v1/query/route', {",
    "const routeRes = await loggedFetch('http://127.0.0.1:8000/api/v1/query/route', {"
)

content = content.replace(
    "res = await fetch('http://127.0.0.1:8000/api/v1/change/analyze', {",
    "res = await loggedFetch('http://127.0.0.1:8000/api/v1/change/analyze', {"
)

content = content.replace(
    "res = await fetch('http://127.0.0.1:8000/api/v1/change/vqa', {",
    "res = await loggedFetch('http://127.0.0.1:8000/api/v1/change/vqa', {"
)

content = content.replace(
    "res = await fetch('http://127.0.0.1:8000/api/v1/cross-modal/analyze', {",
    "res = await loggedFetch('http://127.0.0.1:8000/api/v1/cross-modal/analyze', {"
)

content = content.replace(
    "res = await fetch('http://127.0.0.1:8000/api/v1/vqa/query', {",
    "res = await loggedFetch('http://127.0.0.1:8000/api/v1/vqa/query', {"
)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED app.js")
