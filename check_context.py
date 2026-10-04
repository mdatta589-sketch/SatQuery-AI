with open('frontend/app.js', 'r', encoding='utf8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "btnQueryPanel = document.getElementById" in line:
        print(f"Line {i}: {line.strip()}")
        # Check context
        for j in range(max(0, i-10), i):
            print(f"  {j}: {lines[j].strip()}")
