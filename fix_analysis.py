import sys
with open('backend/app/api/analysis.py', 'r') as f:
    content = f.read()

# I will replace the calculate_ndvi function using Python directly
new_func = '''
@router.post("/ndvi")
def calculate_ndvi(req: NDVIRequest):
    try:
        catalog = pystac_client.Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace
        )
        search = catalog.search(collections=["sentinel-2-l2a"], ids=[req.scene_id])
        item = next(search.items(), None)
        if not item:
            raise HTTPException(status_code=404, detail="Scene not found")
            
        if "B04" not in item.assets or "B08" not in item.assets:
            raise HTTPException(status_code=400, detail="Required Sentinel-2 bands B04 and B08 are unavailable.")
            
        b04_url = item.assets["B04"].href
        b08_url = item.assets["B08"].href
        
        from app.processing.raster import get_aoi_window_and_transform
        
        with rasterio.Env(CPL_VSIL_CURL_ALLOWED_EXTENSIONS='tif'):
            with rasterio.open(b04_url) as src_red, rasterio.open(b08_url) as src_nir:
                if req.aoi:
                    window, window_transform = get_aoi_window_and_transform(src_nir, req.aoi)
                    if window is None:
                        raise HTTPException(status_code=400, detail="AOI is completely outside the scene bounds.")
                        
                    width = int(window.width)
                    height = int(window.height)
                    transform = window_transform
                    
                    geo_bounds = transform_bounds(src_nir.crs, 'EPSG:4326', 
                        transform[2], transform[5] + height * transform[4], 
                        transform[2] + width * transform[0], transform[5]
                    )
                else:
                    transform, width, height = calculate_default_transform(
                        src_nir.crs, 'EPSG:3857', src_nir.width, src_nir.height, *src_nir.bounds
                    )
                    geo_bounds = transform_bounds(src_nir.crs, 'EPSG:4326', *src_nir.bounds)
                    window = None

                west, south, east, north = geo_bounds
                
                vrt_options = {
                    'crs': 'EPSG:3857',
                    'transform': transform,
                    'width': width,
                    'height': height
                }
                
                max_dim = 1024
                scale = min(1.0, max_dim / max(width, height))
                dst_width = max(1, int(width * scale))
                dst_height = max(1, int(height * scale))
                
                # If we have a window, we want to read only that window from the source
                # WarpedVRT reads from the source, so we need to constrain it. 
                # Actually, WarpedVRT takes src. If we just want to warp a subset, we can pass 
                # a Windowed read if we create a memory file, or we can let WarpedVRT handle it 
                # by passing the cropped bounds as the target transform!
                # Since vrt_options sets transform and width/height, WarpedVRT will only pull the requested area!
                
                with WarpedVRT(src_red, **vrt_options) as vrt_red, WarpedVRT(src_nir, **vrt_options) as vrt_nir:
                    red_data = vrt_red.read(1, out_shape=(dst_height, dst_width), resampling=Resampling.bilinear).astype(np.float32)
                    nir_data = vrt_nir.read(1, out_shape=(dst_height, dst_width), resampling=Resampling.bilinear).astype(np.float32)
                    
                    valid_mask = (red_data > 0) & (nir_data > 0)
                    denominator = nir_data + red_data
                    np.putmask(denominator, denominator == 0, 1e-10)
                    ndvi = (nir_data - red_data) / denominator
                    ndvi[~valid_mask] = np.nan
                    
                    valid_pixels = ndvi[valid_mask]
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
                            "valid_pixel_count": int(valid_pixels.size),
                            "vegetation_area_percentage": veg_pct
                        },
                        "threshold": {
                            "ndvi": 0.4,
                            "meaning": "Prototype vegetation interpretation threshold"
                        },
                        "image_url": f"http://127.0.0.1:8000/api/v1/analysis/result/{result_id}/image.png",
                        "bounds": [
                            [south, west],
                            [north, east]
                        ],
                        "source": {
                            "red": "B04",
                            "nir": "B08"
                        }
                    }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''

import re
content = re.sub(r'@router\.post\("/ndvi"\).*?except Exception as e:\n\s+raise HTTPException\(status_code=500, detail=str\(e\)\)', new_func, content, flags=re.DOTALL)
content = content.replace("roi: dict | None = None", "aoi: dict | None = None")
with open('backend/app/api/analysis.py', 'w') as f:
    f.write(content)
