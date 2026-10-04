import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = """
  if (dataset.is_analysis) {
        const stats = dataset.analysis_data.statistics;
        const areaStr = dataset.analysis_data.area ? (dataset.analysis_data.area / 1000000).toFixed(2) + ' km²' : '-';
        datasetProps.innerHTML = `
          <div class="prop-row"><span class="label-text">Analysis</span><span class="value-text" id="inspector-sensor">NDVI</span></div>
          <div class="prop-row"><span class="label-text">Dataset</span><span class="value-text" style="color: var(--accent-color); font-weight: 600;">${dataset.source_layer_name || dataset.scene_info?.scene_id || dataset.analysis_data.scene_id}</span></div>
          <div class="prop-row"><span class="label-text">AOI</span><span class="value-text">${dataset.analysis_data.scope || 'Full Scene'}</span></div>
          <div class="prop-row"><span class="label-text">AOI Area</span><span class="value-text mono">${areaStr}</span></div>
          <div class="prop-row"><span class="label-text">Formula</span><span class="value-text mono" id="inspector-formula" style="font-size: 11px;">(B08 - B04) / (B08 + B04)</span></div>
          
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">STATISTICS</div>
          <div class="prop-row"><span class="label-text">Minimum NDVI</span><span class="value-text mono">${stats.min.toFixed(4)}</span></div>
          <div class="prop-row"><span class="label-text">Maximum NDVI</span><span class="value-text mono">${stats.max.toFixed(4)}</span></div>
          <div class="prop-row"><span class="label-text">Mean NDVI</span><span class="value-text mono">${stats.mean.toFixed(4)}</span></div>
          <div class="prop-row"><span class="label-text">Median NDVI</span><span class="value-text mono">${stats.median.toFixed(4)}</span></div>
          
          <div style="margin-top: 12px; margin-bottom: 4px; font-weight: 600; font-size: 11px; color: var(--text-secondary);">PIXEL COUNTS</div>
          <div class="prop-row"><span class="label-text">Total pixels</span><span class="value-text mono">${(stats.total_pixel_count || 0).toLocaleString()}</span></div>
          <div class="prop-row"><span class="label-text">Valid pixels</span><span class="value-text mono">${(stats.valid_pixel_count || 0).toLocaleString()}</span></div>
          <div class="prop-row"><span class="label-text">No-data pixels</span><span class="value-text mono">${(stats.nodata_pixel_count || 0).toLocaleString()}</span></div>
        `;
    } else if (dataset.is_stac) {
"""

# The bad code starts at `if (dataset.is_analysis) {` and goes until `} else if (dataset.is_stac) { else if (dataset.is_stac) {`
# We'll just regex replace from `if (dataset.is_analysis) {` to the `} else if (dataset.is_stac) {` and fix the duplicated else if.

js = re.sub(r'if \(dataset\.is_analysis\) \{.*?\} else if \(dataset\.is_stac\) \{ else if \(dataset\.is_stac\) \{', replacement.strip(), js, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
