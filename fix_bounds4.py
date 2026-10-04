lines = []
with open('backend/app/api/catalog.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "import rasterio.transform" in line and "def search_catalog" in "".join(lines[max(0, i-50):i]):
        # This is the wrong one
        pass
        
with open('backend/app/api/catalog.py', 'w', encoding='utf-8') as f:
    in_search = False
    in_metadata = False
    for line in lines:
        if "def search_catalog" in line:
            in_search = True
            in_metadata = False
        if "def get_scene_metadata" in line:
            in_metadata = True
            in_search = False
            
        if "geo_bounds = transform_bounds(src.crs, 'EPSG:4326', *src.bounds)" in line and in_metadata:
            f.write("                  import rasterio.transform\n")
            f.write("                  left_3857, bottom_3857, right_3857, top_3857 = rasterio.transform.array_bounds(height, width, transform)\n")
            f.write("                  geo_bounds = transform_bounds('EPSG:3857', 'EPSG:4326', left_3857, bottom_3857, right_3857, top_3857)\n")
        elif "import rasterio.transform" in line and in_search:
            pass # skip
        elif "left_3857, bottom_3857, right_3857, top_3857" in line and in_search:
            pass
        elif "geo_bounds = transform_bounds('EPSG:3857'" in line and in_search:
            f.write("                              geo_bounds = transform_bounds(src.crs, 'EPSG:4326', *src.bounds)\n")
        else:
            f.write(line)

