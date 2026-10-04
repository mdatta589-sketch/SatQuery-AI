with open('frontend/app.js', 'r', encoding='utf8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'btn-search-stac' in line:
        print(i, line.strip())
