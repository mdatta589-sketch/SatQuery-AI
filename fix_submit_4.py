import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

ans_match = re.search(r"const ansText = data\.answer \|\| \"No answer returned\.\";", content)
if ans_match:
    ans_new = """let ansText = data.answer;
                if (task === 'change') {
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
✓ Analysis completed successfully
</div>`;
                    } else {
                        ansText = "Change Analysis failed.<br><br>Please check the selected scenes and AOI and try again.";
                    }
                } else if (!ansText) {
                    ansText = "No answer returned.";
                }"""
    content = content[:ans_match.start()] + ans_new + content[ans_match.end():]
    print("ADDED RESULT CARD")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
