with open('frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re

target_text = """        btnReport.disabled = true;
        btnReport.textContent = "Generating...";"""

replacement_text = """        btnReport.disabled = true;
        btnReport.textContent = "Generating...";
        
        if (imageOverlay && imageOverlay._url) {
            try {
                const imgRes = await fetch(imageOverlay._url);
                const blob = await imgRes.blob();
                payload.image_data = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onloadend = () => resolve(reader.result);
                    reader.readAsDataURL(blob);
                });
            } catch (e) {
                console.warn("Could not fetch image data for PDF: ", e);
            }
        }"""

content = content.replace(target_text, replacement_text)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
