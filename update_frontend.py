with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re

# 1. Change task routing to change_vqa
content = re.sub(
    r"if \(isChangeQuery && beforeId && afterId && beforeId !== afterId\) \{\s*task = 'change';",
    "if (isChangeQuery && beforeId && afterId && beforeId !== afterId) {\n                task = 'change_vqa';",
    content
)

# 2. Change the fetch block
fetch_old = """            if (task === 'change') {
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
                data = await res.json();"""

fetch_new = """            if (task === 'change_vqa') {
                document.getElementById('header-status').textContent = 'RUNNING CHANGE VQA...';
                
                const beforeSel = document.getElementById('change-before-select');
                const afterSel = document.getElementById('change-after-select');
                
                if (!beforeSel.value || !afterSel.value) {
                    throw new Error("Change-VQA requires two different satellite scenes.<br><br>Please select both a Before and After scene.");
                }
                
                if (beforeSel.value === afterSel.value) {
                    throw new Error("Before and After scenes must be different.<br><br>Please select different acquisition dates.");
                }
                
                if (!aoiData) {
                    throw new Error("Please select an Area of Interest before running Change-VQA.");
                }
                const payload = {
                    image_before_id: beforeSel.value,
                    image_after_id: afterSel.value,
                    question: q,
                    aoi: aoiData
                };
                
                const res = await loggedFetch('http://127.0.0.1:8000/api/v1/change/vqa', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                data = await res.json();"""
content = content.replace(fetch_old, fetch_new)

# 3. Change task check for overlay logic
content = re.sub(r"if \(task === 'change' && data\.status === 'success'\)", "if (task === 'change_vqa' && data.status === 'success')", content)

# 4. Change Inspector logic
inspector_old = """                        try {
                            document.getElementById('inspector-name').textContent = "Change Analysis";
                            document.getElementById('inspector-sensor').textContent = "Sentinel-2 L2A";
                            document.getElementById('inspector-band').textContent = "Before: 2025-03-28";
                            document.getElementById('inspector-dim').textContent = "After: 2025-04-02";
                            document.getElementById('inspector-dtype').textContent = "Baseline Raster Difference";
                            document.getElementById('inspector-res').textContent = "0.25 (Threshold)";
                            document.getElementById('inspector-source-crs').textContent = "-";
                            document.getElementById('inspector-display-crs').textContent = "-";
                            document.getElementById('inspector-coord-crs').textContent = "-";
                            document.getElementById('inspector-bounds').textContent = "-";
                        } catch(e) {}"""
inspector_new = """                        try {
                            document.getElementById('inspector-name').textContent = "Change-VQA";
                            document.getElementById('inspector-sensor').textContent = "Sentinel-2 L2A";
                            document.getElementById('inspector-band').textContent = "Before: 2025-03-28";
                            document.getElementById('inspector-dim').textContent = "After: 2025-04-02";
                            document.getElementById('inspector-dtype').textContent = "Baseline Raster Difference";
                            document.getElementById('inspector-res').textContent = "0.25 (Threshold)";
                            document.getElementById('inspector-source-crs').textContent = "-";
                            document.getElementById('inspector-display-crs').textContent = "-";
                            document.getElementById('inspector-coord-crs').textContent = "-";
                            document.getElementById('inspector-bounds').textContent = "-";
                        } catch(e) {}"""
content = content.replace(inspector_old, inspector_new)

# 5. Change Result Card logic
result_card_old = """                if (task === 'change') {
                    if (data.status === 'success') {
                        const methodFormat = data.method === 'baseline_raster_difference' ? 'Baseline Raster Difference' : data.method;
                        let caseStudyHtml = '';
                        const caseStudySel = document.getElementById('change-case-study');
                        const beforeSel = document.getElementById('change-before-select');
                        const afterSel = document.getElementById('change-after-select');
                        
                        if (caseStudySel && caseStudySel.value === 'kancha') {
                            caseStudyHtml = `Kancha Gachibowli, Hyderabad<br><br><strong>Before</strong><br>28 March 2025<br><br><strong>After</strong><br>2 April 2025<br><br>`;
                        } else {
                            caseStudyHtml = `<strong>Before</strong><br>${beforeSel.value}<br><br><strong>After</strong><br>${afterSel.value}<br><br>`;
                        }
                        
                        ansText = `<div style="font-family: sans-serif; line-height: 1.5; font-size: 13px;">
<strong>CHANGE ANALYSIS</strong><br><br>
${caseStudyHtml}<strong>Changed area</strong><br>
${data.change_percentage.toFixed(2)}%<br><br>
<strong>Changed pixels</strong><br>
${data.changed_pixel_count.toLocaleString()}<br><br>
<strong>Valid pixels</strong><br>
${data.total_valid_pixel_count.toLocaleString()}<br><br>
<strong>Threshold</strong><br>
${data.threshold}<br><br>
<strong>Method</strong><br>
${methodFormat}<br><br>
<strong>Status</strong><br>
[CHECK] Analysis completed successfully
</div>`;
                    } else {
                        ansText = "Change Analysis failed.<br><br>Please check the selected scenes and AOI and try again.";
                    }
                }"""

result_card_new = """                if (task === 'change_vqa') {
                    if (data.status === 'success') {
                        const methodFormat = data.method === 'baseline_raster_difference' ? 'Baseline Raster Difference' : data.method;
                        const exec = data.execution || {};
                        ansText = `<div style="font-family: sans-serif; line-height: 1.5; font-size: 13px;">
<strong>CHANGE-VQA</strong><br><br>
<strong>Question:</strong><br>
${data.question || q}<br><br>
<strong>Answer:</strong><br>
${data.answer}<br><br>
<strong>Change detected:</strong><br>
${data.change_percentage.toFixed(2)}%<br><br>
<strong>Changed pixels:</strong><br>
${data.changed_pixel_count.toLocaleString()}<br><br>
<strong>Valid pixels:</strong><br>
${data.total_valid_pixel_count.toLocaleString()}<br><br>
<strong>Before:</strong><br>
${data.before_scene}<br><br>
<strong>After:</strong><br>
${data.after_scene}<br><br>
<strong>Method:</strong><br>
${methodFormat}<br><br>
<strong>Evidence:</strong><br>
Visual overlay on map<br><br>
<strong>Execution:</strong><br>
Task: ${exec.task || 'change_vqa'}<br>
Model: ${exec.model || 'change_interpreter'}<br>
Provider: ${exec.provider || 'local'}<br>
Status: ${exec.status || 'success'}
</div>`;
                    } else {
                        ansText = "Change-VQA failed.<br><br>" + (data.error || "Please check the selected scenes and AOI and try again.");
                    }
                }"""
content = content.replace(result_card_old, result_card_new)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FRONTEND UPDATED")
