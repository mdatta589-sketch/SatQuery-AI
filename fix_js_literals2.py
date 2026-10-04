with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

content = content.replace(
    "console.log([FETCH REQUEST] \ \);",
    "console.log(`[FETCH REQUEST] ${options.method || 'GET'} ${url}`);"
)

content = content.replace(
    "console.log([FETCH RESPONSE] \ \);",
    "console.log(`[FETCH RESPONSE] ${res.status} ${res.url}`);"
)

content = content.replace(
    "caseStudyHtml = `<strong>Before</strong><br>\<br><br><strong>After</strong><br>\<br><br>`;",
    "caseStudyHtml = `<strong>Before</strong><br>${beforeSel.value}<br><br><strong>After</strong><br>${afterSel.value}<br><br>`;"
)

content = content.replace(
    "\Changed area",
    "${caseStudyHtml}<strong>Changed area</strong>"
)

content = content.replace(
    "\%<br><br>\n<strong>Changed pixels</strong><br>\n\<br><br>\n<strong>Valid pixels</strong><br>\n\<br><br>\n<strong>Threshold</strong><br>\n\<br><br>\n<strong>Method</strong><br>\n\<br><br>",
    "${data.change_percentage.toFixed(2)}%<br><br>\n<strong>Changed pixels</strong><br>\n${data.changed_pixel_count.toLocaleString()}<br><br>\n<strong>Valid pixels</strong><br>\n${data.total_valid_pixel_count.toLocaleString()}<br><br>\n<strong>Threshold</strong><br>\n${data.threshold}<br><br>\n<strong>Method</strong><br>\n${methodFormat}<br><br>"
)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED")
