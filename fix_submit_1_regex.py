import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

match = re.search(r"btnQueryPanel\.addEventListener\('click', async \(\) => \{\s*const qInput = document\.getElementById\('query-input-panel'\);\s*const q = qInput\.value\.trim\(\);\s*document\.getElementById\('header-status'\)\.textContent = 'VALIDATING\.\.\.';\s*const ctx = getVqaContext\(\);\s*if \(\!ctx\) \{\s*document\.getElementById\('header-status'\)\.textContent = 'ERROR: No image selected';\s*alert\(\"No satellite image selected\.\"\);\s*return;\s*\}", content)

if match:
    submit_new = """btnQueryPanel.addEventListener('click', async () => {
            const qInput = document.getElementById('query-input-panel');
            const q = qInput.value.trim();
            
            document.getElementById('header-status').textContent = 'VALIDATING...';
            
            const qLower = q.toLowerCase();
            const changeKeywords = [
                'compare', 'difference', 'changed', 'changes', 
                'what changed', 'detect changes', 'change between these images', 
                'compare these images', 'how has this area changed', 
                'identify changed areas', 'show changes'
            ];
            const isChangeQuery = changeKeywords.some(kw => qLower.includes(kw));
            
            const beforeSel = document.getElementById('change-before-select');
            const afterSel = document.getElementById('change-after-select');
            const beforeId = beforeSel ? beforeSel.value : null;
            const afterId = afterSel ? afterSel.value : null;
            
            let task = 'vqa';
            let ctx = null;
            
            if (isChangeQuery && beforeId && afterId && beforeId !== afterId) {
                task = 'change';
            } else {
                ctx = getVqaContext();
                if (!ctx) {
                    document.getElementById('header-status').textContent = 'ERROR: No image selected';
                    alert("No satellite image selected.");
                    return;
                }
            }"""
    content = content[:match.start()] + submit_new + content[match.end():]
    print("MATCHED AND REPLACED")
else:
    print("NOT MATCHED")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
