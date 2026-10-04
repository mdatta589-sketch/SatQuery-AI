import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

# Fix the loggedFetch console logs
content = re.sub(
    r"console\.log\(\[FETCH REQUEST\] \\ \\\);",
    r"console.log(`[FETCH REQUEST] ${options.method || 'GET'} ${url}`);",
    content
)
content = re.sub(
    r"console\.log\(\[FETCH RESPONSE\] \\ \\\);",
    r"console.log(`[FETCH RESPONSE] ${res.status} ${res.url}`);",
    content
)

# Fix the caseStudyHtml template literal
content = re.sub(
    r"caseStudyHtml = `<strong>Before<\/strong><br>\\<br><br><strong>After<\/strong><br>\\<br><br>`;",
    r"caseStudyHtml = `<strong>Before</strong><br>${beforeSel.value}<br><br><strong>After</strong><br>${afterSel.value}<br><br>`;",
    content
)

# Fix the result card text
content = re.sub(
    r"\\\Changed area",
    r"${caseStudyHtml}<strong>Changed area</strong>",
    content
)
content = re.sub(
    r"\\%<br><br>\n<strong>Changed pixels<\/strong><br>\n\\<br><br>\n<strong>Valid pixels<\/strong><br>\n\\<br><br>\n<strong>Threshold<\/strong><br>\n\\<br><br>\n<strong>Method<\/strong><br>\n\\<br><br>",
    r"${data.change_percentage.toFixed(2)}%<br><br>\n<strong>Changed pixels</strong><br>\n${data.changed_pixel_count.toLocaleString()}<br><br>\n<strong>Valid pixels</strong><br>\n${data.total_valid_pixel_count.toLocaleString()}<br><br>\n<strong>Threshold</strong><br>\n${data.threshold}<br><br>\n<strong>Method</strong><br>\n${methodFormat}<br><br>",
    content
)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED TEMPLATE LITERALS")
