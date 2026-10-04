import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_analysis_panel = '''      <div id="analysis-panel" class="panel-content" style="display: none;">
        <div class="panel-section">
          <h2 class="panel-title">APP MODE</h2>
          <div class="form-group" style="margin-top: 12px;">
            <select id="app-mode-selector" class="form-control">
              <option value="farmer">Farmer Mode</option>
              <option value="student">Student Mode</option>
              <option value="researcher">Researcher Mode</option>
            </select>
          </div>
        </div>

        <div class="panel-section">
          <h2 class="panel-title">1. SELECT FARM AREA</h2>
          <div style="display: flex; gap: 8px; margin-top: 12px;">
             <button class="btn btn-secondary" id="btn-draw-rect" style="flex:1" title="Draw Rectangle"><i class="fa-solid fa-vector-square"></i> Rect</button>
             <button class="btn btn-secondary" id="btn-draw-poly" style="flex:1" title="Draw Polygon"><i class="fa-solid fa-draw-polygon"></i> Poly</button>
             <button class="btn btn-secondary" id="btn-clear-aoi" style="flex:1"><i class="fa-solid fa-trash"></i> Clear</button>
          </div>
          <div id="aoi-details" style="display: none; margin-top: 12px;">
             <div class="prop-row"><span class="label-text">Area</span><span class="value-text" id="aoi-area">-</span></div>
             <div class="prop-row"><span class="label-text">Center</span><span class="value-text mono" id="aoi-center">-</span></div>
             <div class="prop-row"><span class="label-text">Bounds</span><span class="value-text mono" id="aoi-bounds" style="line-height:1.4">-</span></div>
          </div>
          <p id="aoi-prompt" class="label-text" style="margin-top: 8px;">Click a draw button to select your farm.</p>
        </div>

        <div class="panel-section">
          <h2 class="panel-title">2. ANALYSIS</h2>
          
          <div class="form-group" style="margin-top: 16px;">
            <label class="label-text">Analysis type</label>
            <select id="analysis-type" class="form-control">
              <option value="temporal">Compare Years (Farmer)</option>
              <option value="ndvi">Vegetation Health (NDVI)</option>
            </select>
          </div>

          <div id="farmer-temporal-controls" class="form-group" style="margin-top: 12px;">
             <label class="label-text">Previous Observation</label>
             <input type="date" id="farmer-prev-date" class="form-control" value="2025-09-15" style="margin-bottom: 8px;"/>
             <label class="label-text">Current Observation</label>
             <input type="date" id="farmer-curr-date" class="form-control" value="2026-09-15" />
          </div>
          
          <div id="ndvi-controls" class="form-group" style="display:none; margin-top:12px;">
            <label class="label-text">Scene</label>
            <select id="analysis-scene" class="form-control">
              <option value="">No scene loaded...</option>
            </select>
          </div>
          
          <button class="btn btn-primary" id="btn-run-analysis" style="width: 100%; margin-top: 12px;">Run Analysis</button>
        </div>
        
        <div class="panel-section" id="student-explanation" style="display:none; margin-top: 16px;">
            <h2 class="panel-title">HOW IT WORKS</h2>
            <p class="label-text" style="margin-top:8px;"><strong>Sentinel-2:</strong> A satellite that takes pictures of the Earth. It sees visible light (RGB) and Near-Infrared (NIR) light.</p>
            <p class="label-text" style="margin-top:8px;"><strong>NDVI:</strong> Normalized Difference Vegetation Index. Healthy plants reflect a lot of NIR light. We use this to measure crop health.</p>
            <p class="label-text" style="margin-top:8px;"><strong>Workflow:</strong> Satellite Image &rarr; Preprocessing &rarr; Spectral Analysis &rarr; AI VQA &rarr; Result</p>
            <p class="label-text" style="margin-top:8px;"><strong>AI:</strong> We use an AI model (PaliGemma) to answer questions, and Grounding DINO to find where things are.</p>
        </div>

        <div class="panel-section" id="analysis-result-section" style="display: none; margin-top: 16px;">
          <h2 class="panel-title">3. RESULT</h2>
          
          <div id="farmer-result-card" style="display:none; background: var(--panel-bg); border: 1px solid var(--border); padding: 12px; border-radius: var(--radius); margin-top: 12px;">
              <h3 style="margin: 0 0 12px 0; font-size: 13px; font-weight: 600; color: var(--text);">FARM COMPARISON</h3>
              <div style="margin-bottom: 8px;"><span style="color: var(--text-muted); font-size: 11px;">Previous:</span> <span id="res-prev-date" style="color: var(--text); font-size: 12px;">-</span></div>
              <div style="margin-bottom: 12px;"><span style="color: var(--text-muted); font-size: 11px;">Current:</span> <span id="res-curr-date" style="color: var(--text); font-size: 12px;">-</span></div>
              
              <div style="margin-bottom: 12px; border-top: 1px solid var(--border); padding-top: 8px;">
                  <strong style="color: var(--accent); font-size: 12px;">Vegetation</strong><br/>
                  <span style="font-size: 11px; color: var(--text-light);" id="res-veg-change">-</span>
              </div>
              <div style="margin-bottom: 12px;">
                  <strong style="color: var(--accent); font-size: 12px;">Water</strong><br/>
                  <span style="font-size: 11px; color: var(--text-light);" id="res-water-change">-</span>
              </div>
              <div style="border-top: 1px solid var(--border); padding-top: 8px;">
                  <strong style="color: var(--text); font-size: 12px;">Overall Satellite Observation:</strong><br/>
                  <span style="font-size: 12px; color: var(--text); display: inline-block; margin-top: 4px;" id="res-overall">-</span>
              </div>
              <p style="font-size: 10px; color: var(--text-muted); margin-top: 12px; font-style: italic;">These results are satellite observations and should be verified on the ground.</p>
          </div>

          <div id="researcher-result-card" style="display:none;">
              <div class="inspector-field" style="margin-top: 12px;">
                  <span class="label-text">AOI Details</span>
                  <div id="res-researcher-aoi" style="color: var(--text-light); margin-top: 4px; font-size: 11px; white-space: pre-wrap;">-</div>
              </div>
              <div class="inspector-field" style="margin-top: 12px;">
                  <span class="label-text">VQA Answer</span>
                  <div id="vqa-answer" style="color: var(--text-light); margin-top: 4px;">-</div>
              </div>
              <div class="inspector-field" style="margin-top: 12px;">
                  <span class="label-text">Confidence</span>
                  <div id="vqa-confidence" style="color: var(--text-light); margin-top: 4px;">-</div>
              </div>
              <div class="inspector-field" style="margin-top: 12px;">
                  <span class="label-text">Evidence</span>
                  <div id="vqa-evidence" style="color: var(--text-light); margin-top: 4px;">-</div>
              </div>
              <div class="inspector-field" style="margin-top: 12px;">
                  <span class="label-text">Execution</span>
                  <div id="vqa-execution" style="color: var(--text-muted); margin-top: 4px; font-size: 11px; white-space: pre-wrap;">-</div>
              </div>
          </div>
        </div>
      </div>'''

new_settings_panel = '''      <div id="settings-panel" class="panel-content" style="display: none;">
        <div class="panel-section">
            <h2 class="panel-title">SETTINGS</h2>
            
            <div class="form-group" style="margin-top: 16px;">
                <label class="label-text">Map Language</label>
                <select id="map-language" class="form-control">
                    <option value="english">English (Carto Voyager)</option>
                    <option value="local">Local names (OSM Default)</option>
                </select>
                <p class="label-text" style="margin-top: 8px; font-size: 10px;">Note: Leaflet does not dynamically translate tiles. This changes the tile provider.</p>
            </div>
        </div>
      </div>'''

new_export_panel = '''      <div id="export-panel" class="panel-content" style="display: none;">
        <div class="panel-section">
            <h2 class="panel-title">EXPORT REPORT</h2>
            <p class="label-text" style="margin-top: 12px;">Download a summary of your analysis.</p>
            
            <button class="btn btn-primary" id="btn-export-farmer" style="width: 100%; margin-top: 12px;"><i class="fa-solid fa-file-pdf"></i> Farmer Report (HTML)</button>
            <button class="btn btn-secondary" id="btn-export-student" style="width: 100%; margin-top: 8px;"><i class="fa-solid fa-file-pdf"></i> Student Report (HTML)</button>
            <button class="btn btn-secondary" id="btn-export-researcher" style="width: 100%; margin-top: 8px;"><i class="fa-solid fa-file-code"></i> Researcher Report (JSON)</button>
        </div>
      </div>'''

# Replace analysis-panel
html = re.sub(r'<div id="analysis-panel" class="panel-content" style="display: none;">.*?</div>\s*<div id="export-panel"', new_analysis_panel + '\n      <div id="export-panel"', html, flags=re.DOTALL)
# Replace settings and export
html = re.sub(r'<div id="export-panel" class="panel-content" style="display: none;">.*?</div>\s*<div id="settings-panel" class="panel-content" style="display: none;">.*?</div>', new_export_panel + '\n' + new_settings_panel, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML updated.")
