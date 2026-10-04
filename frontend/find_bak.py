import json
with open(r'C:\Users\admin\.gemini\antigravity\brain\fcaf5554-1444-4d94-8253-b40e8cbe42b5\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if not line.strip(): continue
        try:
            data = json.loads(line)
        except:
            continue
        content = data.get('content', '')
        if 'app.js' in content and ('backup' in content.lower() or 'original' in content.lower()):
            if data.get('step_index', 0) < 500:
                print(f"Found backup mention in step {data.get('step_index')}")
                print(content[:300])
