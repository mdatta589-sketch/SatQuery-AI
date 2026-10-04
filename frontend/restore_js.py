with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('// =============== NEW SATQUERY FEATURES ==============='):
        break
    new_lines.append(line)

with open('app.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
