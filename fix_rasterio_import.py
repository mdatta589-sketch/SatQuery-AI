import re

with open('backend/app/services/change_service.py', 'r', encoding='utf8') as f:
    content = f.read()

old_bad = '''                    import rasterio.windows
                    win_transform = rasterio.windows.transform(window, src_b.transform)
                    
                    analysis_transform = win_transform
                    if out_w != int(w_w) or out_h != int(w_h):
                        analysis_transform = win_transform * win_transform.scale(
                            (w_w / out_w),
                            (w_h / out_h)
                        )
                        
                    analysis_bounds = rasterio.windows.bounds(window, src_b.transform)'''

new_good = '''                    from rasterio.windows import transform as win_get_transform, bounds as win_get_bounds
                    win_transform = win_get_transform(window, src_b.transform)
                    
                    analysis_transform = win_transform
                    if out_w != int(w_w) or out_h != int(w_h):
                        analysis_transform = win_transform * win_transform.scale(
                            (w_w / out_w),
                            (w_h / out_h)
                        )
                        
                    analysis_bounds = win_get_bounds(window, src_b.transform)'''

if old_bad in content:
    content = content.replace(old_bad, new_good)
    with open('backend/app/services/change_service.py', 'w', encoding='utf8') as f:
        f.write(content)
    print("FIXED")
else:
    print("NOT FOUND")
