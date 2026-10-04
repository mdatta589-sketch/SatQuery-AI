import re

with open('backend/app/api/analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace error strings
content = content.replace(
    'raise HTTPException(status_code=400, detail="AOI is completely outside the scene bounds.")',
    'raise HTTPException(status_code=400, detail="Selected AOI does not overlap the selected raster.")'
)

# Replace stats calculation
new_stats = '''
                    total_pixels = ndvi.size
                    nodata_pixels = total_pixels - valid_pixels.size
                    
                    if valid_pixels.size > 0:
                        min_val = float(np.min(valid_pixels))
                        max_val = float(np.max(valid_pixels))
                        mean_val = float(np.mean(valid_pixels))
                        median_val = float(np.median(valid_pixels))
                        veg_pixels = np.sum(valid_pixels >= 0.4)
                        veg_pct = float(veg_pixels / valid_pixels.size * 100.0)
                    else:
                        min_val = max_val = mean_val = median_val = veg_pct = 0.0
                        
                    result_id = str(uuid.uuid4())
                    NDVI_CACHE[result_id] = {
                        'ndvi': ndvi,
                        'valid_mask': valid_mask,
                        'width': dst_width,
                        'height': dst_height
                    }
                    
                    return {
                        "scene_id": req.scene_id,
                        "analysis": "NDVI",
                        "formula": "(B08 - B04) / (B08 + B04)",
                        "scope": "Selected AOI" if req.aoi else "Full Scene",
                        "statistics": {
                            "min": min_val,
                            "max": max_val,
                            "mean": mean_val,
                            "median": median_val,
                            "total_pixel_count": total_pixels,
                            "valid_pixel_count": int(valid_pixels.size),
                            "nodata_pixel_count": nodata_pixels,
                            "vegetation_area_percentage": veg_pct
                        },
'''
content = re.sub(r'valid_pixels\.size > 0:.*?"vegetation_area_percentage": veg_pct\n\s+\},', new_stats.strip() + ',', content, flags=re.DOTALL)

with open('backend/app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
