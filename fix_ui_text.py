import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# 1. Update the error messages
old_errors = '''                  if (!beforeSel.value || !afterSel.value) {
                      throw new Error("Please select both Before and After images.");
                  }
                  
                  if (beforeSel.value === afterSel.value) {
                      throw new Error("Before and After images must be different scenes.");
                  }
                  
                  const beforeParts = beforeSel.value.split('_');
                  const afterParts = afterSel.value.split('_');
                  
                  if (beforeParts.length > 5 && afterParts.length > 5) {
                      const beforeDate = beforeParts[2].substring(0, 8);
                      const afterDate = afterParts[2].substring(0, 8);
                      const beforeTile = beforeParts[4];
                      const afterTile = afterParts[4];
                      
                      if (beforeDate === afterDate) {
                          throw new Error("Change analysis requires scenes from different dates to detect temporal changes.");
                      }
                      if (beforeTile !== afterTile) {
                          throw new Error("Change Analysis requires scenes from the same geographic tile to ensure overlap.");
                      }
                  }'''

new_errors = '''                  if (!beforeSel.value || !afterSel.value) {
                      throw new Error("Change Analysis requires two different satellite scenes.<br><br>Please select both a Before and After scene.");
                  }
                  
                  if (beforeSel.value === afterSel.value) {
                      throw new Error("Before and After scenes must be different.<br><br>Please select different acquisition dates.");
                  }
                  
                  if (!aoiData) {
                      throw new Error("Please select an Area of Interest before running Change Analysis.");
                  }'''

content = content.replace(old_errors, new_errors)

# 2. Update the result card rendering
old_result = '''                let ansText = data.answer;
                if (task === 'change') {
                    if (data.status === 'success') {
                        const methodFormat = data.method === 'baseline_raster_difference' ? 'Baseline Raster Difference' : data.method;
                        let caseStudyHtml = '';
                        const caseStudySel = document.getElementById('change-case-study');
                        if (caseStudySel && caseStudySel.value === 'kancha') {
                            caseStudyHtml = <strong>Case Study:</strong> Kancha Gachibowli, Hyderabad<br><strong>Before:</strong> 28 March 2025<br><strong>After:</strong> 2 April 2025<br><br>;
                        }
                        ansText = <strong>Change Analysis</strong><br><br>\Changed area: \%<br>Changed pixels: \<br>Valid pixels: \<br>Threshold: \<br>Method: \;
                    } else {
                        ansText = data.error || data.message || "An error occurred during change analysis.";
                    }'''

new_result = '''                let ansText = data.answer;
                if (task === 'change') {
                    if (data.status === 'success') {
                        const methodFormat = data.method === 'baseline_raster_difference' ? 'Baseline Raster Difference' : data.method;
                        let caseStudyHtml = '';
                        const caseStudySel = document.getElementById('change-case-study');
                        const beforeSel = document.getElementById('change-before-select');
                        const afterSel = document.getElementById('change-after-select');
                        if (caseStudySel && caseStudySel.value === 'kancha') {
                            caseStudyHtml = Kancha Gachibowli, Hyderabad<br><br><strong>Before</strong><br>28 March 2025<br><br><strong>After</strong><br>2 April 2025<br><br>;
                        } else {
                            caseStudyHtml = <strong>Before</strong><br>\<br><br><strong>After</strong><br>\<br><br>;
                        }
                        
                        ansText = <div style="font-family: sans-serif; line-height: 1.5; font-size: 13px;">
<strong>CHANGE ANALYSIS</strong><br><br>
\<strong>Changed area</strong><br>
\%<br><br>
<strong>Changed pixels</strong><br>
\<br><br>
<strong>Valid pixels</strong><br>
\<br><br>
<strong>Threshold</strong><br>
\<br><br>
<strong>Method</strong><br>
\<br><br>
<strong>Status</strong><br>
✓ Analysis completed successfully
</div>;
                    } else {
                        ansText = "Change Analysis failed.<br><br>Please check the selected scenes and AOI and try again.";
                    }'''

content = content.replace(old_result, new_result)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED app.js")
