with open('backend/app/services/query_router.py', 'r', encoding='utf8') as f:
    content = f.read()

import re

# Fix VQA regex
old_vqa = """        vqa_keywords = [
            'is there', 'are there', 'what is visible', 'what type', 'what are', 'how many', 'describe the image'
        ]
        if any(q.startswith(kw) or f" {kw} " in f" {q} " for kw in vqa_keywords) or q.endswith('?'):
            return {"task": "vqa", "confidence": 0.8, "reason": "Matched ordinary VQA intent"}"""

new_vqa = """        vqa_keywords = [
            'is there', 'are there', 'what is visible', 'what type', 'what are', 'how many', 'describe the image',
            'what is in', 'what can you see', 'what do you see', 'describe', 'is this area'
        ]
        if any(q.startswith(kw) or f" {kw} " in f" {q} " for kw in vqa_keywords):
            return {"task": "vqa", "confidence": 0.8, "reason": "Matched ordinary VQA intent"}"""

content = content.replace(old_vqa, new_vqa)

with open('backend/app/services/query_router.py', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED ROUTER LOGIC")
