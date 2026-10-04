with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re

# 1. Add historyItem creation
insertion_point = """            const resultSec = document.getElementById('vqa-result-section');"""
history_creation = """            const historyContainer = document.getElementById('query-history-container');
            const emptyHistory = document.getElementById('query-history-empty');
            if (emptyHistory) emptyHistory.style.display = 'none';
            
            const historyItem = document.createElement('div');
            historyItem.style.background = 'var(--app-bg)';
            historyItem.style.border = '1px solid var(--border)';
            historyItem.style.borderRadius = 'var(--radius)';
            historyItem.style.padding = '12px';
            
            const qDiv = document.createElement('div');
            qDiv.style.fontWeight = '600';
            qDiv.style.fontSize = '12px';
            qDiv.style.marginBottom = '8px';
            qDiv.innerHTML = `<i class="fa-solid fa-user" style="margin-right: 6px; color: var(--accent);"></i> ${q}`;
            
            const aDiv = document.createElement('div');
            aDiv.style.fontSize = '12px';
            aDiv.style.color = 'var(--text-light)';
            aDiv.innerHTML = '<i class="fa-solid fa-spinner fa-spin" style="margin-right: 6px;"></i> Analyzing...';
            
            historyItem.appendChild(qDiv);
            historyItem.appendChild(aDiv);
            historyContainer.prepend(historyItem);
            
            const resultSec = document.getElementById('vqa-result-section');"""

content = content.replace(insertion_point, history_creation)

# 2. Add historyItem update on success
success_update = """                document.getElementById('vqa-answer').innerHTML = ansText;"""
success_history = """                document.getElementById('vqa-answer').innerHTML = ansText;
                aDiv.innerHTML = `<span style="color: var(--accent);"><i class="fa-solid fa-reply" style="margin-right: 6px;"></i></span>` + ansText;
                
                const statusDiv = document.createElement('div');
                statusDiv.style.fontSize = '11px';
                statusDiv.style.color = 'var(--text-muted)';
                statusDiv.style.marginTop = '8px';
                statusDiv.textContent = `Provider: ${data.execution?.provider || 'remote'} | Model: ${data.execution?.model || 'unknown'} | Status: ${data.execution?.status || 'success'}`;
                historyItem.appendChild(statusDiv);"""

content = content.replace(success_update, success_history)

# 3. Add historyItem update on unknown task
unknown_update = """                  document.getElementById('vqa-answer').textContent = msg;"""
unknown_history = """                  document.getElementById('vqa-answer').textContent = msg;
                  aDiv.innerHTML = `<span style="color: var(--accent);"><i class="fa-solid fa-reply" style="margin-right: 6px;"></i></span>${msg}`;"""

content = content.replace(unknown_update, unknown_history)

# 4. Add historyItem update on error
error_update = """                document.getElementById('vqa-answer').textContent = `Error: ${errMsg}`;"""
error_history = """                document.getElementById('vqa-answer').textContent = `Error: ${errMsg}`;
                aDiv.innerHTML = `<span style="color: #ef4444;"><i class="fa-solid fa-triangle-exclamation" style="margin-right: 6px;"></i> ${errMsg}</span>`;"""

content = content.replace(error_update, error_history)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED HISTORY LOGIC")
