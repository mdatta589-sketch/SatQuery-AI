import re
with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

func = """function updateChangeAnalysisDropdowns() {
    if (changeAnalysisMode === 'case-study') return;
    
    const beforeSel = document.getElementById('change-before-select');
    const afterSel = document.getElementById('change-after-select');
    const msg = document.getElementById('change-analysis-message');
    const selectors = document.getElementById('change-analysis-selectors');
    
    const stacLayers = layers.filter(l => l.is_stac);
    if (stacLayers.length >= 2) {
        if (msg) msg.style.display = 'none';
        if (selectors) selectors.style.display = 'flex';
        
        const bVal = beforeSel.value;
        const aVal = afterSel.value;
        
        beforeSel.innerHTML = '';
        afterSel.innerHTML = '';
        stacLayers.forEach(l => {
            beforeSel.add(new Option(l.name, l.id));
            afterSel.add(new Option(l.name, l.id));
        });
        
        if (bVal && stacLayers.some(l => l.id === bVal)) beforeSel.value = bVal;
        if (aVal && stacLayers.some(l => l.id === aVal)) afterSel.value = aVal;
    } else {
        if (msg) msg.style.display = 'block';
        if (selectors) selectors.style.display = 'none';
    }
}

"""

# Insert before function activateKanchaCaseStudy
content = content.replace("function activateKanchaCaseStudy() {", func + "function activateKanchaCaseStudy() {")

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
