with open('backend/app/processing/raster.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_func = '''def get_aoi_window_and_transform(src, aoi: dict):
    from rasterio.warp import transform_bounds
    from rasterio.windows import from_bounds
    # aoi must have west, south, east, north in EPSG:4326
    wgs84_bounds = [aoi['west'], aoi['south'], aoi['east'], aoi['north']]
    try:
        target_bounds = transform_bounds('EPSG:4326', src.crs, *wgs84_bounds)
    except Exception as e:
        target_bounds = transform_bounds('EPSG:4326', 'EPSG:3857', *wgs84_bounds) # fallback
    
    # Clip to raster bounds to avoid out of bounds read
    left = max(target_bounds[0], src.bounds.left)
    bottom = max(target_bounds[1], src.bounds.bottom)
    right = min(target_bounds[2], src.bounds.right)
    top = min(target_bounds[3], src.bounds.top)
    
    if left >= right or bottom >= top:
        return None, None
        
    window = from_bounds(left, bottom, right, top, src.transform)
    return window, src.window_transform(window)'''

new_func = '''def get_aoi_window_and_transform(src, aoi: dict):
    from rasterio.warp import transform_bounds
    from rasterio.windows import from_bounds
    from fastapi import HTTPException
    
    if aoi['west'] == aoi['east'] or aoi['south'] == aoi['north']:
        raise HTTPException(status_code=400, detail="Point AOI cannot be used for NDVI. Please select a rectangle or polygon.")
        
    # aoi must have west, south, east, north in EPSG:4326
    wgs84_bounds = [aoi['west'], aoi['south'], aoi['east'], aoi['north']]
    try:
        target_bounds = transform_bounds('EPSG:4326', src.crs, *wgs84_bounds)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to transform AOI to raster CRS: {str(e)}")
    
    # Clip to raster bounds to avoid out of bounds read
    left = max(target_bounds[0], src.bounds.left)
    bottom = max(target_bounds[1], src.bounds.bottom)
    right = min(target_bounds[2], src.bounds.right)
    top = min(target_bounds[3], src.bounds.top)
    
    if left >= right or bottom >= top:
        return None, None
        
    window = from_bounds(left, bottom, right, top, src.transform)
    return window, src.window_transform(window)'''

code = code.replace(old_func, new_func)

with open('backend/app/processing/raster.py', 'w', encoding='utf-8') as f:
    f.write(code)
