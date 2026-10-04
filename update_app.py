with open('frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re

target_text = "if (btnReport) btnReport.addEventListener('click', () => alert('AI Summary functionality is not yet implemented.'));"
replacement_text = """if (btnReport) btnReport.addEventListener('click', async () => {
    try {
        const payload = {
            layer: currentLayer ? {
                name: currentLayer.name,
                id: currentLayer.id,
                stac_properties: currentLayer.stac_properties || {}
            } : null,
            aoi: currentAOI ? {
                type: currentAOI.geometry_type || currentAOI.type,
                area: currentAOI.area_m2 || currentAOI.area,
                bounds: {
                    north: currentAOI.bounds ? currentAOI.bounds.getNorth() : currentAOI.bbox.north,
                    south: currentAOI.bounds ? currentAOI.bounds.getSouth() : currentAOI.bbox.south,
                    east: currentAOI.bounds ? currentAOI.bounds.getEast() : currentAOI.bbox.east,
                    west: currentAOI.bounds ? currentAOI.bounds.getWest() : currentAOI.bbox.west
                }
            } : null,
            ndvi: (currentLayer && currentLayer.is_analysis && currentLayer.analysis_data) ? currentLayer.analysis_data : null,
            vqa: document.getElementById('vqa-answer').textContent !== '-' && document.getElementById('vqa-answer').textContent !== 'Analyzing satellite image...' ? {
                question: document.getElementById('query-input').value,
                answer: document.getElementById('vqa-answer').textContent,
                confidence_status: document.getElementById('vqa-confidence').textContent,
                execution: {
                    model: 'google/paligemma-3b-ft-rsvqa-hr-224'
                }
            } : null
        };
        
        btnReport.disabled = true;
        btnReport.textContent = "Generating...";
        
        const res = await fetch('http://127.0.0.1:8000/api/v1/export/pdf', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        
        if (!res.ok) throw new Error('Failed to generate report');
        
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'satquery_report.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (e) {
        alert("Error exporting PDF: " + e.message);
    } finally {
        btnReport.disabled = false;
        btnReport.textContent = "Export PDF Report";
    }
});"""

content = content.replace(target_text, replacement_text)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
