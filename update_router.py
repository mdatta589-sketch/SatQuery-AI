with open('backend/app/services/query_router.py', 'r', encoding='utf8') as f:
    content = f.read()

old_code = """        # 2. NDVI / VEGETATION"""

new_code = """        # 1.5 CROSS MODAL
        cross_modal_keywords = [
            'optical and sar', 'sar and optical', 'cross modal', 'cross-modal',
            'fuse optical', 'fuse sar', 'combine optical', 'compare optical and sar'
        ]
        if any(kw in q for kw in cross_modal_keywords):
            return {"task": "cross_modal", "confidence": 0.9, "reason": "Matched Cross-Modal intent"}
            
        # 2. NDVI / VEGETATION"""

content = content.replace(old_code, new_code)
with open('backend/app/services/query_router.py', 'w', encoding='utf8') as f:
    f.write(content)
print("Updated query_router.py")
