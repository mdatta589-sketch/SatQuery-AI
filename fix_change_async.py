with open('backend/app/api/change.py', 'r', encoding='utf8') as f:
    content = f.read()

# Remove async from analyze_change
content = content.replace('async def analyze_change', 'def analyze_change')
# Remove async from change_vqa
content = content.replace('async def change_vqa', 'def change_vqa')

with open('backend/app/api/change.py', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED change.py async blocking")
