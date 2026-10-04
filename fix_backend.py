with open('backend/app/models/vqa/preprocessing.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

if lines[-1].strip() == 'return str(out_path.resolve())' and not lines[-1].startswith(' '):
    lines.pop()

with open('backend/app/models/vqa/preprocessing.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
