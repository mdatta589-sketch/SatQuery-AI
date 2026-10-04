import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

submit_old = '''const res = await fetch('http://127.0.0.1:8000/api/v1/query/route', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: q })
                });'''
submit_new = '''const routeRes = await loggedFetch('http://127.0.0.1:8000/api/v1/query/route', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: q })
                });'''
content = content.replace(submit_old, submit_new)

content = content.replace("const routeData = await res.json();", "const routeData = await routeRes.json();")

submit_old2 = '''res = await fetch('http://127.0.0.1:8000/api/v1/change/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });'''
submit_new2 = '''res = await loggedFetch('http://127.0.0.1:8000/api/v1/change/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });'''
content = content.replace(submit_old2, submit_new2)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("RECOVERED STAGE 2")
