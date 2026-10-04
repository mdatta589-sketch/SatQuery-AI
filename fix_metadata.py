import re

with open('backend/app/api/catalog.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''                  # Rasterio's transform_bounds returns (left, bottom, right, top)
                  from rasterio.warp import transform_bounds
                  # We still return the display bounds in EPSG:4326 because Leaflet's L.imageOverlay API 
                  # expects LatLng coordinates, but the image PIXELS must be EPSG:3857
                  geo_bounds = transform_bounds(src.crs, 'EPSG:4326', *src.bounds)
                  west, south, east, north = geo_bounds'''

replacement = '''                  # Rasterio's transform_bounds returns (left, bottom, right, top)
                  from rasterio.warp import transform_bounds
                  import rasterio.transform
                  # We still return the display bounds in EPSG:4326 because Leaflet's L.imageOverlay API 
                  # expects LatLng coordinates, but the image PIXELS must be EPSG:3857
                  left_3857, bottom_3857, right_3857, top_3857 = rasterio.transform.array_bounds(height, width, transform)
                  geo_bounds = transform_bounds('EPSG:3857', 'EPSG:4326', left_3857, bottom_3857, right_3857, top_3857)
                  west, south, east, north = geo_bounds'''

code = code.replace(target, replacement)

with open('backend/app/api/catalog.py', 'w', encoding='utf-8') as f:
    f.write(code)
