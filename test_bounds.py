from rasterio.warp import transform_bounds

wgs84_bounds = [-45.2, 70.9, -45.0, 71.0]

# Try UTM Zone 23N which is EPSG:32623, or maybe something near Greenland
try:
    crs = 'EPSG:32623'
    target_bounds = transform_bounds('EPSG:4326', crs, *wgs84_bounds)
    print(f"Target bounds in {crs}:", target_bounds)
    
    # And convert back
    geo_bounds = transform_bounds(crs, 'EPSG:4326', *target_bounds)
    print("Back to WGS84:", geo_bounds)
except Exception as e:
    print(e)
