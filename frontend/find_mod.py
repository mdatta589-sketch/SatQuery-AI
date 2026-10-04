import json
import sys

tool_calls = []
with open(r'C:\Users\admin\.gemini\antigravity\brain\fcaf5554-1444-4d94-8253-b40e8cbe42b5\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if not line.strip(): continue
        try:
            data = json.loads(line)
        except:
            continue
        
        if 'tool_calls' in data:
            for tc in data['tool_calls']:
                if 'app.js' in str(tc):
                    tool_calls.append((data['step_index'], tc['name'], tc.get('arguments', {})))
