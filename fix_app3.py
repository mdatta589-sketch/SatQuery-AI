with open('frontend/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("descSpan.innerHTML = NDVI Analysis;", "descSpan.innerHTML = 'NDVI Analysis';")

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
