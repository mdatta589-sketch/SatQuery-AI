import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

match = re.search(r"const routeRes = await fetch\('http://127\.0\.0\.1:8000/api/v1/query/route'.*?body: JSON\.stringify\(\{\s*image_id: currentLayer\.id,\s*image_type: ctx\.image_type,\s*source: ctx\.source,\s*modality: ctx\.modality,\s*representation: ctx\.representation,\s*question: q,\s*mode: 'vqa',\s*aoi: aoiData\s*\}\)\s*\}\);", content, flags=re.DOTALL)

if not match:
    match = re.search(r"const routeRes = await fetch\('http://127\.0\.0\.1:8000/api/v1/query/route'.*?\}\);", content, flags=re.DOTALL)

if not match:
    match = re.search(r"// 1\. Route the query\s*const (res|routeRes) = await fetch\('http://127\.0\.0\.1:8000/api/v1/query/route'.*?\}\);", content, flags=re.DOTALL)

if match:
    new_call = """let data = null;
            if (task === 'change') {
                document.getElementById('header-status').textContent = 'RUNNING CHANGE ANALYSIS...';
                
                const beforeSel = document.getElementById('change-before-select');
                const afterSel = document.getElementById('change-after-select');
                
                if (!beforeSel.value || !afterSel.value) {
                    throw new Error("Change Analysis requires two different satellite scenes.<br><br>Please select both a Before and After scene.");
                }
                
                if (beforeSel.value === afterSel.value) {
                    throw new Error("Before and After scenes must be different.<br><br>Please select different acquisition dates.");
                }
                
                if (!aoiData) {
                    throw new Error("Please select an Area of Interest before running Change Analysis.");
                }
                const payload = {
                    image_before_id: beforeSel.value,
                    image_after_id: afterSel.value,
                    aoi: aoiData
                };
                
                const res = await loggedFetch('http://127.0.0.1:8000/api/v1/change/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                data = await res.json();
            } else {
                document.getElementById('header-status').textContent = 'RUNNING VQA...';
                const routeRes = await loggedFetch('http://127.0.0.1:8000/api/v1/query/route', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image_id: currentLayer.id,
                        image_type: ctx.image_type,
                        source: ctx.source,
                        modality: ctx.modality,
                        representation: ctx.representation,
                        question: q,
                        mode: 'vqa',
                        aoi: aoiData
                    })
                });
                data = await routeRes.json();
            }"""
    content = content[:match.start()] + new_call + content[match.end():]
    print("MATCHED API CALL")
else:
    print("NOT MATCHED")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
