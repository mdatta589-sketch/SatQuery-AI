with open('backend/app/services/change_service.py', 'r', encoding='utf8') as f:
    content = f.read()

old_code = """                if aoi and "west" in aoi:
                    left, bottom, right, top = aoi["west"], aoi["south"], aoi["east"], aoi["north"]"""

new_code = """                bbox = aoi.get('bbox', aoi) if isinstance(aoi, dict) else (aoi or {})
                if bbox and "west" in bbox:
                    left, bottom, right, top = bbox["west"], bbox["south"], bbox["east"], bbox["north"]"""

content = content.replace(old_code, new_code)
with open('backend/app/services/change_service.py', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED change_service.py AOI parsing")
