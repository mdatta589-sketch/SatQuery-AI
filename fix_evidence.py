import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

match = re.search(r"if \(task === 'change' && data\.status === 'success' && data\.overlay_base64\) \{", content)
if match:
    new_cond = """
                const changeEv = (data.evidence || []).find(e => e.type === 'image_overlay');
                if (task === 'change' && data.status === 'success' && changeEv) {
                    const evData = changeEv.data;
"""
    content = content[:match.start()] + new_cond + content[match.end():]
    
    # Now replace data.overlay_base64 references inside this block
    # Actually, changeEv.data is ALREADY "data:image/png;base64,...".
    # I wrote `"data:image/png;base64," + data.overlay_base64` in my logic.
    content = content.replace('"data:image/png;base64," + data.overlay_base64', 'evData')
    
    print("FIXED EVIDENCE PARSING")
else:
    print("NOT FOUND")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
