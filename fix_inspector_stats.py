import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = '''
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">STATISTICS</div>
          <div class="prop-row"><span class="label-text">Minimum</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Maximum</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Mean</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Median</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Vegetation > 0.4</span><span class="value-text mono"> %</span></div>
          
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">PIXEL COUNTS</div>
          <div class="prop-row"><span class="label-text">Total pixels</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Valid pixels</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">No-data pixels</span><span class="value-text mono"></span></div>
'''

js = re.sub(r'<div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var\(--text-secondary\);">STATISTICS</div>.*?<div class="prop-row"><span class="value-text mono">\$\{stats\.valid_pixel_count\.toLocaleString\(\)\}</span></div>', replacement.strip(), js, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
