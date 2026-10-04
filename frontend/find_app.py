import json
import sys

with open(r'C:\Users\admin\.gemini\antigravity\brain\fcaf5554-1444-4d94-8253-b40e8cbe42b5\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        content = data.get('content', '')
        if 'app.js' in content and 'setupEventListeners' in content:
            print(f"Found app.js in step {data.get('step_index')} (line {i})")
            if 'const btnSearchStac' in content:
                print("btnSearchStac is also in this block.")
                idx = content.find('const btnSearchStac')
                print(content[idx-100:idx+200])
                break
