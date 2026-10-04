with open('frontend/app.js', 'r', encoding='utf8') as f:
    lines = f.readlines()

start = -1
for i, line in enumerate(lines):
    if "function setupEventListeners" in line:
        start = i
        break

if start != -1:
    brace_count = 0
    for i in range(start, len(lines)):
        brace_count += lines[i].count('{')
        brace_count -= lines[i].count('}')
        if brace_count == 0 and i > start:
            print(f"setupEventListeners ends at line {i}")
            break
