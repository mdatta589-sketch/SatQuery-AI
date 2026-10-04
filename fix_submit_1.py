import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

submit_old = """    if (btnQueryPanel) {
        btnQueryPanel.addEventListener('click', async () => {
            const qInput = document.getElementById('query-input-panel');
            const q = qInput.value.trim();
            
            document.getElementById('header-status').textContent = 'VALIDATING...';
            const ctx = getVqaContext();
            if (!ctx) {
                document.getElementById('header-status').textContent = 'ERROR: No image selected';
                alert("No satellite image selected.");
                return;
            }
            if (!q) {
                document.getElementById('header-status').textContent = 'ERROR: Empty question';
                alert("Enter a question about the selected image.");
                return;
            }
            if (q.length > 500) {
                document.getElementById('header-status').textContent = 'ERROR: Question too long';
                alert("Question is too long.");
                return;
            }"""

submit_new = """    if (btnQueryPanel) {
        btnQueryPanel.addEventListener('click', async () => {
            const qInput = document.getElementById('query-input-panel');
            const q = qInput.value.trim();
            
            document.getElementById('header-status').textContent = 'VALIDATING...';
            
            if (!q) {
                document.getElementById('header-status').textContent = 'ERROR: Empty question';
                alert("Enter a question about the selected image.");
                return;
            }
            if (q.length > 500) {
                document.getElementById('header-status').textContent = 'ERROR: Question too long';
                alert("Question is too long.");
                return;
            }
            
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

if submit_old in content:
    content = content.replace(submit_old, submit_new)
    print("SUBMIT START REPLACED")
else:
    print("SUBMIT START NOT FOUND")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
