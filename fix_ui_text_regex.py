import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# 2. Update the result card rendering using REGEX to avoid strict whitespace mismatch
content = re.sub(
    r'ansText = <strong>Change Analysis</strong><br><br>\$\{caseStudyHtml\}Changed area: \$\{data\.change_percentage\.toFixed\(2\)\}%<br>Changed pixels: \$\{data\.changed_pixel_count\.toLocaleString\(\)\}<br>Valid pixels: \$\{data\.total_valid_pixel_count\.toLocaleString\(\)\}<br>Threshold: \$\{data\.threshold\}<br>Method: \$\{methodFormat\};',
    '''ansText = <div style="font-family: sans-serif; line-height: 1.5; font-size: 13px;">
<strong>CHANGE ANALYSIS</strong><br><br>
<strong>Changed area</strong><br>
%<br><br>
<strong>Changed pixels</strong><br>
<br><br>
<strong>Valid pixels</strong><br>
<br><br>
<strong>Threshold</strong><br>
<br><br>
<strong>Method</strong><br>
<br><br>
<strong>Status</strong><br>
✓ Analysis completed successfully
</div>;''',
    content
)

content = re.sub(
    r"caseStudyHtml = <strong>Case Study:</strong> Kancha Gachibowli, Hyderabad<br><strong>Before:</strong> 28 March 2025<br><strong>After:</strong> 2 April 2025<br><br>;",
    "caseStudyHtml = Kancha Gachibowli, Hyderabad<br><br><strong>Before</strong><br>28 March 2025<br><br><strong>After</strong><br>2 April 2025<br><br>;",
    content
)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED RESULT CARD TEXT")
