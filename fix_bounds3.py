import re

with open('backend/app/api/catalog.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Undo the wrong one in search_catalog
wrong = '''                                                import rasterio.transform
                  left_3857, bottom_3857, right_3857, top_3857 = rasterio.transform.array_bounds(height, width, transform)
                  geo_bounds = transform_bounds('EPSG:3857', 'EPSG:4326', left_3857, bottom_3857, right_3857, top_3857)'''
code = code.replace(wrong, "                              geo_bounds = transform_bounds(src.crs, 'EPSG:4326', *src.bounds)")

# Do the right one in get_scene_metadata
target = "                  geo_bounds = transform_bounds(src.crs, 'EPSG:4326', *src.bounds)"
replacement = '''                  import rasterio.transform
                  left_3857, bottom_3857, right_3857, top_3857 = rasterio.transform.array_bounds(height, width, transform)
                  geo_bounds = transform_bounds('EPSG:3857', 'EPSG:4326', left_3857, bottom_3857, right_3857, top_3857)'''
code = code.replace(target, replacement)

with open('backend/app/api/catalog.py', 'w', encoding='utf-8') as f:
    f.write(code)
