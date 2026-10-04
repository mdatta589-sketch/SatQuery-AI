with open('frontend/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'fetch' in line and 'vqa/query' in line:
        print(f"Line {i}: {line.strip()}")
        print([ord(c) for c in line.strip()])
