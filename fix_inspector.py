import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = '''            <div class="prop-row"><span class="label-text">Dataset</span><span class="value-text" style="color: var(--accent-color); font-weight: 600;"></span></div>
            <div class="prop-row"><span class="label-text">AOI</span><span class="value-text"></span></div>
            <div class="prop-row"><span class="label-text">AOI Area</span><span class="value-text mono"></span></div>
            <div class="prop-row"><span class="label-text">Formula</span><span class="value-text mono" id="inspector-formula" style="font-size: 11px;">(B08 - B04) / (B08 + B04)</span></div>'''

replacement = '''            <div class="prop-row"><span class="label-text">Dataset</span><span class="value-text" style="color: var(--accent-color); font-weight: 600;"></span></div>
            <div class="prop-row"><span class="label-text">Source</span><span class="value-text"></span></div>
            <div class="prop-row"><span class="label-text">Bands</span><span class="value-text"></span></div>
            <div class="prop-row"><span class="label-text">AOI</span><span class="value-text"></span></div>
            <div class="prop-row"><span class="label-text">AOI Area</span><span class="value-text mono"></span></div>
            <div class="prop-row"><span class="label-text">Formula</span><span class="value-text mono" id="inspector-formula" style="font-size: 11px;">(B08 - B04) / (B08 + B04)</span></div>'''

js = js.replace(target, replacement)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
