with open('frontend/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix 1: The first block was supposed to assign targetList and show the group
broken_block_1 = '''  if (dataset.is_analysis) {
        const stats = dataset.analysis_data.statistics;
        const areaStr = dataset.analysis_data.area ? (dataset.analysis_data.area / 1000000).toFixed(2) + ' km\xb2' : '-';
        datasetProps.innerHTML = 
          <div class="prop-row"><span class="label-text">Analysis</span><span class="value-text" id="inspector-sensor">NDVI</span></div>
          <div class="prop-row"><span class="label-text">Dataset</span><span class="value-text" style="color: var(--accent-color); font-weight: 600;"></span></div>
          <div class="prop-row"><span class="label-text">AOI</span><span class="value-text"></span></div>
          <div class="prop-row"><span class="label-text">AOI Area</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Formula</span><span class="value-text mono" id="inspector-formula" style="font-size: 11px;">(B08 - B04) / (B08 + B04)</span></div>
          
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">STATISTICS</div>
          <div class="prop-row"><span class="label-text">Minimum NDVI</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Maximum NDVI</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Mean NDVI</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Median NDVI</span><span class="value-text mono"></span></div>
          
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">PIXEL COUNTS</div>
          <div class="prop-row"><span class="label-text">Total pixels</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Valid pixels</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">No-data pixels</span><span class="value-text mono"></span></div>
        ;'''

fixed_block_1 = '''  if (dataset.is_analysis) {
      targetList = document.getElementById('list-analysis');
      document.getElementById('group-analysis').style.display = 'block';'''

# Fix 2: The second block was supposed to assign descSpan
broken_block_2 = '''  if (dataset.is_analysis) {
        const stats = dataset.analysis_data.statistics;
        const areaStr = dataset.analysis_data.area ? (dataset.analysis_data.area / 1000000).toFixed(2) + ' km\xb2' : '-';
        datasetProps.innerHTML = 
          <div class="prop-row"><span class="label-text">Analysis</span><span class="value-text" id="inspector-sensor">NDVI</span></div>
          <div class="prop-row"><span class="label-text">Dataset</span><span class="value-text" style="color: var(--accent-color); font-weight: 600;"></span></div>
          <div class="prop-row"><span class="label-text">AOI</span><span class="value-text"></span></div>
          <div class="prop-row"><span class="label-text">AOI Area</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Formula</span><span class="value-text mono" id="inspector-formula" style="font-size: 11px;">(B08 - B04) / (B08 + B04)</span></div>
          
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">STATISTICS</div>
          <div class="prop-row"><span class="label-text">Minimum NDVI</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Maximum NDVI</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Mean NDVI</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Median NDVI</span><span class="value-text mono"></span></div>
          
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">PIXEL COUNTS</div>
          <div class="prop-row"><span class="label-text">Total pixels</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">Valid pixels</span><span class="value-text mono"></span></div>
          <div class="prop-row"><span class="label-text">No-data pixels</span><span class="value-text mono"></span></div>
        ;'''

fixed_block_2 = '''  if (dataset.is_analysis) {
      descSpan.innerHTML = NDVI Analysis;'''

if broken_block_1 in code and broken_block_2 in code:
    code = code.replace(broken_block_1, fixed_block_1, 1)
    code = code.replace(broken_block_2, fixed_block_2, 1)
    with open('frontend/app.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Fixed!")
else:
    print("Blocks not found.")
