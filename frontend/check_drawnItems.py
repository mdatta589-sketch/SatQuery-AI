import sys
with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'drawnItems' in line:
        start = max(0, i-2)
        end = min(len(lines), i+3)
        print(f"--- line {i+1} ---")
        print("".join(lines[start:end]))
