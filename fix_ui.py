with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re

# Remove history logic
bad_code = """            const historyList = document.getElementById('vqa-history-list');
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            const qDiv = document.createElement('div');
            qDiv.style.fontWeight = '600';
            qDiv.style.marginBottom = '4px';
            qDiv.innerHTML = `<i class="fa-solid fa-user" style="margin-right: 6px; color: #888;"></i> ${q}`;
            historyItem.appendChild(qDiv);
            
            const aDiv = document.createElement('div');
            aDiv.style.marginBottom = '8px';
            historyItem.appendChild(aDiv);
            historyList.appendChild(historyItem);"""

good_code = """            // (Removed hallucinated history code)"""

content = content.replace(bad_code, good_code)

bad_code_2 = """                aDiv.innerHTML = `<span style="color: var(--accent);"><i class="fa-solid fa-reply" style="margin-right: 6px;"></i> ${ansText}</span>`;
                
                const statusDiv = document.createElement('div');
                statusDiv.style.fontSize = '11px';
                statusDiv.style.color = 'var(--text-muted)';
                statusDiv.style.marginTop = '8px';
                statusDiv.textContent = `Provider: ${data.execution?.provider || 'remote'} | Model: ${data.execution?.model || 'unknown'} | Status: ${data.execution?.status || 'success'}`;
                historyItem.appendChild(statusDiv);
                
                document.getElementById('vqa-answer').textContent = 'Analysis complete.';"""

good_code_2 = """                document.getElementById('vqa-answer').innerHTML = ansText;"""

content = content.replace(bad_code_2, good_code_2)

bad_code_3 = """                aDiv.innerHTML = `<span style="color: var(--accent);"><i class="fa-solid fa-reply" style="margin-right: 6px;"></i> ${msg}</span>`;
                  document.getElementById('vqa-answer').textContent = msg;"""

good_code_3 = """                  document.getElementById('vqa-answer').textContent = msg;"""

content = content.replace(bad_code_3, good_code_3)

bad_code_4 = """                aDiv.innerHTML = `<span style="color: #ef4444;"><i class="fa-solid fa-triangle-exclamation" style="margin-right: 6px;"></i> ${errMsg}</span>`;
                document.getElementById('vqa-answer').textContent = "Error during execution.";"""

good_code_4 = """                document.getElementById('vqa-answer').textContent = `Error: ${errMsg}`;"""

content = content.replace(bad_code_4, good_code_4)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED UI INJECTIONS")
