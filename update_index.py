with open('frontend/index.html', 'r', encoding='utf8') as f:
    content = f.read()

# I will find where change-analysis is defined.
old_html = """                        <div id="change-analysis-selectors" style="display: none; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px; background: #f8f9fa; margin-bottom: 15px;">
                            <h6 class="text-primary mb-2" style="font-size: 0.9rem;">Change Analysis Setup</h6>
                            <div class="mb-2">
                                <label class="form-label small mb-1">Before Scene:</label>
                                <select id="change-before-scene" class="form-control form-control-sm">
                                    <option value="">-- Select Before Image --</option>
                                </select>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small mb-1">After Scene:</label>
                                <select id="change-after-scene" class="form-control form-control-sm">
                                    <option value="">-- Select After Image --</option>
                                </select>
                            </div>
                        </div>"""

new_html = """                        <div id="change-analysis-selectors" style="display: none; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px; background: #f8f9fa; margin-bottom: 15px;">
                            <h6 class="text-primary mb-2" style="font-size: 0.9rem;">Change Analysis Setup</h6>
                            <div class="mb-2">
                                <label class="form-label small mb-1">Before Scene:</label>
                                <select id="change-before-scene" class="form-control form-control-sm">
                                    <option value="">-- Select Before Image --</option>
                                </select>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small mb-1">After Scene:</label>
                                <select id="change-after-scene" class="form-control form-control-sm">
                                    <option value="">-- Select After Image --</option>
                                </select>
                            </div>
                        </div>
                        
                        <div id="cross-modal-selectors" style="padding: 10px; border: 1px solid #dee2e6; border-radius: 4px; background: #f8f9fa; margin-bottom: 15px;">
                            <h6 class="text-success mb-2" style="font-size: 0.9rem;">Cross-Modal Setup</h6>
                            <div class="mb-2">
                                <label class="form-label small mb-1">Optical Image (Sentinel-2):</label>
                                <select id="cross-modal-opt-scene" class="form-control form-control-sm">
                                    <option value="">-- Select Optical Image --</option>
                                </select>
                            </div>
                            <div class="mb-2">
                                <label class="form-label small mb-1">SAR Image (Sentinel-1):</label>
                                <select id="cross-modal-sar-scene" class="form-control form-control-sm">
                                    <option value="">-- Select SAR Image --</option>
                                </select>
                            </div>
                        </div>"""

content = content.replace(old_html, new_html)

# Add collection selector to STAC Search
old_stac = """                            <div class="mb-2">
                                <label class="form-label small">Max Cloud Cover (%)</label>
                                <input type="number" id="stac-cloud-cover" class="form-control form-control-sm" value="20" min="0" max="100">
                            </div>"""

new_stac = """                            <div class="mb-2">
                                <label class="form-label small">Max Cloud Cover (%)</label>
                                <input type="number" id="stac-cloud-cover" class="form-control form-control-sm" value="20" min="0" max="100">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small">Satellite Platform</label>
                                <select id="stac-collection" class="form-control form-control-sm">
                                    <option value="sentinel-2-l2a">Sentinel-2 (Optical)</option>
                                    <option value="sentinel-1-grd">Sentinel-1 (SAR)</option>
                                </select>
                            </div>"""

content = content.replace(old_stac, new_stac)

with open('frontend/index.html', 'w', encoding='utf8') as f:
    f.write(content)
print("Updated index.html")
