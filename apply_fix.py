with open('frontend/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = 0
for i, line in enumerate(lines):
    if skip > 0:
        skip -= 1
        continue
    
    if 'if (dataset.is_analysis) {' in line and i + 3 < len(lines) and 'datasetProps.innerHTML' in lines[i+3]:
        if 'let targetList;' in lines[i-1]:
            new_lines.append('  if (dataset.is_analysis) {\n')
            new_lines.append("      targetList = document.getElementById('list-analysis');\n")
            new_lines.append("      document.getElementById('group-analysis').style.display = 'block';\n")
            skip = 22
        elif 'descSpan.style' in lines[i-2]:
            new_lines.append('  if (dataset.is_analysis) {\n')
            new_lines.append("      descSpan.innerHTML = 'NDVI Analysis';\n")
            skip = 22
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
