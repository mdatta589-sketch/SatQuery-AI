import re
with open('backend/app/api/catalog.py', 'r', encoding='utf8') as f:
    content = f.read()

old_return = '''                return {
                    "image_url": f"http://127.0.0.1:8000/api/v1/catalog/scene/{scene_id}/preview.png",
                    "bounds": [
                        [south, west],
                        [north, east]
                    ],'''

new_return = '''                return {
                    "id": item.id,
                    "datetime": item.datetime.isoformat() if item.datetime else None,
                    "bbox": item.bbox,
                    "eo:cloud_cover": item.properties.get("eo:cloud_cover"),
                    "assets": {k: v.to_dict() for k, v in item.assets.items()},
                    "preview_url": f"http://127.0.0.1:8000/api/v1/catalog/scene/{scene_id}/preview.png",
                    "image_url": f"http://127.0.0.1:8000/api/v1/catalog/scene/{scene_id}/preview.png",
                    "bounds": [
                        [south, west],
                        [north, east]
                    ],'''

if old_return in content:
    content = content.replace(old_return, new_return)
    with open('backend/app/api/catalog.py', 'w', encoding='utf8') as f:
        f.write(content)
    print("REPLACED")
else:
    print("NOT FOUND")
