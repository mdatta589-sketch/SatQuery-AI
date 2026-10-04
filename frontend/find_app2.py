import json

with open(r'C:\Users\admin\.gemini\antigravity\brain\fcaf5554-1444-4d94-8253-b40e8cbe42b5\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if not line.strip(): continue
        try:
            data = json.loads(line)
        except:
            continue
        content = data.get('content', '')
        if 'btnSearchStac.addEventListener' in content:
            print(f"Found btnSearchStac.addEventListener in step {data.get('step_index')} (line {i})")
