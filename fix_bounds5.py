with open('backend/app/api/catalog.py', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace("                              # Transform native bounds to EPSG:4326 for Leaflet\n                              raster_bounds = list(geo_bounds)", "                              # Transform native bounds to EPSG:4326 for Leaflet\n                              geo_bounds = transform_bounds(src.crs, 'EPSG:4326', *src.bounds)\n                              raster_bounds = list(geo_bounds)")
with open('backend/app/api/catalog.py', 'w', encoding='utf-8') as f:
    f.write(code)
