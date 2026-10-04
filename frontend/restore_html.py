import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

original_panels = '''      <div id="analysis-panel" class="panel-content" style="display: none;">
        <div class="panel-section">
          <h2 class="panel-title">ANALYSIS</h2>
          
          <div class="form-group" style="margin-top: 16px;">
            <label class="label-text">Analysis type</label>
            <select id="analysis-type" class="form-control">
              <option value="ndvi">NDVI (Vegetation Index)</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="label-text">Scene</label>
            <select id="analysis-scene" class="form-control">
              <option value="">No scene loaded...</option>
            </select>
          </div>
          
          <button class="btn btn-primary" id="btn-calc-ndvi" style="width: 100%; margin-top: 8px;">Calculate NDVI</button>
        </div>
        
        <div class="panel-section" id="vqa-result-section" style="display: none; margin-top: 16px;">
          <h2 class="panel-title">RESULT</h2>
          
          <div class="inspector-field" style="margin-top: 12px;">
              <span class="label-text">Answer</span>
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
      <div id="export-panel" class="panel-content" style="display: none;">
        <div class="panel-section"><h2 class="panel-title">EXPORT</h2></div>
      </div>
      <div id="settings-panel" class="panel-content" style="display: none;">
        <div class="panel-section"><h2 class="panel-title">SETTINGS</h2></div>
      </div>'''

html = re.sub(r'<div id="analysis-panel" class="panel-content" style="display: none;">.*?<div id="settings-panel" class="panel-content" style="display: none;">.*?</div>', original_panels, html, flags=re.DOTALL)
html = html.replace('<button id="btn-calc-ndvi" style="display:none;"></button>\n          <button class="btn btn-primary" id="btn-run-analysis"', '')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
