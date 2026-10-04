import sys
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

ids = ['aoi-no-selection', 'aoi-details', 'aoi-type', 'aoi-point-group', 'aoi-bbox-group', 'aoi-area-group', 'aoi-coords', 'aoi-bbox', 'aoi-area']
for i in ids:
    if f'id="{i}"' not in html:
        print(f"Missing: {i}")
print("Done checking IDs.")
