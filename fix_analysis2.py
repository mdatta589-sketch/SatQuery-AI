import re

new_func = '''
                if req.aoi:
                    from rasterio.warp import calculate_default_transform
                    window, window_transform = get_aoi_window_and_transform(src_nir, req.aoi)
                    if window is None:
                        raise HTTPException(status_code=400, detail="AOI is completely outside the scene bounds.")
                    
                    # Convert window bounds to EPSG:3857 for WarpedVRT
                    window_bounds = rasterio.windows.bounds(window, window_transform)
                    transform, width, height = calculate_default_transform(
                        src_nir.crs, 'EPSG:3857', int(window.width), int(window.height), *window_bounds
                    )
                    
                    geo_bounds = transform_bounds('EPSG:3857', 'EPSG:4326', *transform_bounds(src_nir.crs, 'EPSG:3857', *window_bounds))
                    # Actually, geo_bounds can just be transformed directly from window_bounds
                    geo_bounds = transform_bounds(src_nir.crs, 'EPSG:4326', *window_bounds)
                else:
                    transform, width, height = calculate_default_transform(
                        src_nir.crs, 'EPSG:3857', src_nir.width, src_nir.height, *src_nir.bounds
                    )
                    geo_bounds = transform_bounds(src_nir.crs, 'EPSG:4326', *src_nir.bounds)
'''

with open('backend/app/api/analysis.py', 'r') as f:
    content = f.read()
    
# We just need to replace the if req.aoi: block
pattern = r'if req\.aoi:.*?geo_bounds = transform_bounds\(src_nir\.crs, \'EPSG:4326\', \*src_nir\.bounds\)'
content = re.sub(r'if req\.aoi:.*?(?=west, south, east, north = geo_bounds)', new_func.strip() + '\n\n                ', content, flags=re.DOTALL)
with open('backend/app/api/analysis.py', 'w') as f:
    f.write(content)
