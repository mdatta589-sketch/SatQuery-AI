import json
with open(r'C:\Users\admin\.gemini\antigravity\brain\fcaf5554-1444-4d94-8253-b40e8cbe42b5\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for line in lines[-10:]:
    data = json.loads(line)
    if data.get('source') == 'USER_EXPLICIT' and 'media' in data:
        print(data['media'])
