import json
with open(r'C:\Users\admin\.gemini\antigravity\brain\fcaf5554-1444-4d94-8253-b40e8cbe42b5\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for line in lines[-20:]:
    try:
        data = json.loads(line)
        if 'media' in data:
            print(f"Found media in {data.get('type')}: {data['media']}")
    except:
        pass
