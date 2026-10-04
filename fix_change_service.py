import re

with open('backend/app/services/change_service.py', 'r', encoding='utf8') as f:
    content = f.read()

old_block = '''                from rasterio.enums import Resampling
                max_dim = 1024
                scale = min(1.0, max_dim / max(src_b.width, src_b.height))
                out_w = max(1, int(src_b.width * scale))
                out_h = max(1, int(src_b.height * scale))
                
                b_data = src_b.read(list(range(1, bands_to_read + 1)), out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                a_data = src_a.read(list(range(1, bands_to_read + 1)), out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                
                analysis_transform = src_b.transform * src_b.transform.scale(
                    (src_b.width / out_w),
                    (src_b.height / out_h)
                )'''

new_block = '''                from rasterio.enums import Resampling
                from rasterio.windows import from_bounds, Window
                from rasterio.warp import transform_bounds
                
                if aoi and "west" in aoi:
                    left, bottom, right, top = aoi["west"], aoi["south"], aoi["east"], aoi["north"]
                    src_left, src_bottom, src_right, src_top = transform_bounds("EPSG:4326", src_b.crs, left, bottom, right, top)
                    
                    window = from_bounds(src_left, src_bottom, src_right, src_top, transform=src_b.transform)
                    window = window.intersection(Window(0, 0, src_b.width, src_b.height))
                    
                    # Convert window attributes to floats, then to ints to avoid math.ceil issues
                    w_w, w_h = float(window.width), float(window.height)
                    # For out dimensions, we can't be negative.
                    out_w, out_h = max(1, int(w_w)), max(1, int(w_h))
                    
                    max_dim = 1024
                    if out_w > max_dim or out_h > max_dim:
                        scale = min(1.0, max_dim / max(out_w, out_h))
                        out_w = max(1, int(out_w * scale))
                        out_h = max(1, int(out_h * scale))
                        
                    b_data = src_b.read(list(range(1, bands_to_read + 1)), window=window, out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                    a_data = src_a.read(list(range(1, bands_to_read + 1)), window=window, out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                    
                    import rasterio.windows
                    win_transform = rasterio.windows.transform(window, src_b.transform)
                    
                    analysis_transform = win_transform
                    if out_w != int(w_w) or out_h != int(w_h):
                        analysis_transform = win_transform * win_transform.scale(
                            (w_w / out_w),
                            (w_h / out_h)
                        )
                        
                    analysis_bounds = rasterio.windows.bounds(window, src_b.transform)
                else:
                    max_dim = 1024
                    scale = min(1.0, max_dim / max(src_b.width, src_b.height))
                    out_w = max(1, int(src_b.width * scale))
                    out_h = max(1, int(src_b.height * scale))
                    
                    b_data = src_b.read(list(range(1, bands_to_read + 1)), out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                    a_data = src_a.read(list(range(1, bands_to_read + 1)), out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                    
                    analysis_transform = src_b.transform * src_b.transform.scale(
                        (src_b.width / out_w),
                        (src_b.height / out_h)
                    )
                    analysis_bounds = src_b.bounds'''

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("FAILED TO MATCH BLOCK 1")

old_bounds = '''                    transform, width, height = calculate_default_transform(
                        src_b.crs, 'EPSG:3857', out_w, out_h, *src_b.bounds
                    )'''

new_bounds = '''                    transform, width, height = calculate_default_transform(
                        src_b.crs, 'EPSG:3857', out_w, out_h, *analysis_bounds
                    )'''

if old_bounds in content:
    content = content.replace(old_bounds, new_bounds)
else:
    print("FAILED TO MATCH BLOCK 2")

with open('backend/app/services/change_service.py', 'w', encoding='utf8') as f:
    f.write(content)
print("REPLACED change_service.py")
