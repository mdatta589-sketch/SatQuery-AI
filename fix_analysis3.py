import sys
import re

new_func = '''
class NDVIRequest(BaseModel):
    scene_id: str
    source_type: str = "stac"
    aoi: dict | None = None

# Simple in-memory cache for the generated images to avoid recomputing
NDVI_CACHE = {}

@router.post("/ndvi")
def calculate_ndvi(req: NDVIRequest):
    try:
        from app.processing.raster import get_aoi_window_and_transform
        from rasterio.warp import calculate_default_transform
        
        if req.source_type == "upload":
            import os
            from pathlib import Path
            project_root = Path(__file__).resolve().parent.parent.parent.parent
            dataset_dir = project_root / "temp" / "uploads" / req.scene_id
            
            if not dataset_dir.exists():
                raise HTTPException(status_code=404, detail="Uploaded dataset not found.")
                
            files = list(dataset_dir.glob("*.*"))
            
            # Check for B04 and B08
            b04_path = None
            b08_path = None
            
            for f in files:
                if "B04" in f.name.upper():
                    b04_path = str(f)
                elif "B08" in f.name.upper():
                    b08_path = str(f)
                    
            if not b04_path or not b08_path:
                raise HTTPException(status_code=400, detail="NDVI requires Red (B04) and NIR (B08) bands. The selected raster does not contain both required bands.")
                
            b04_url = b04_path
            b08_url = b08_path
            
        else:
            catalog = pystac_client.Client.open(
                "https://planetarycomputer.microsoft.com/api/stac/v1",
                modifier=planetary_computer.sign_inplace
            )
            search = catalog.search(collections=["sentinel-2-l2a"], ids=[req.scene_id])
            item = next(search.items(), None)
            if not item:
                raise HTTPException(status_code=404, detail="Scene not found")
                
            if "B04" not in item.assets or "B08" not in item.assets:
                raise HTTPException(status_code=400, detail="NDVI requires Red (B04) and NIR (B08) bands. The selected raster does not contain both required bands.")
                
            b04_url = item.assets["B04"].href
            b08_url = item.assets["B08"].href

        with rasterio.Env(CPL_VSIL_CURL_ALLOWED_EXTENSIONS='tif'):
            with rasterio.open(b04_url) as src_red, rasterio.open(b08_url) as src_nir:
                if req.aoi:
                    window, window_transform = get_aoi_window_and_transform(src_nir, req.aoi)
                    if window is None:
                        raise HTTPException(status_code=400, detail="AOI is completely outside the scene bounds.")
                    
                    window_bounds = rasterio.windows.bounds(window, window_transform)
                    transform, width, height = calculate_default_transform(
                        src_nir.crs, 'EPSG:3857', int(window.width), int(window.height), *window_bounds
                    )
                    
                    geo_bounds = transform_bounds(src_nir.crs, 'EPSG:4326', *window_bounds)
                else:
                    transform, width, height = calculate_default_transform(
                        src_nir.crs, 'EPSG:3857', src_nir.width, src_nir.height, *src_nir.bounds
                    )
                    geo_bounds = transform_bounds(src_nir.crs, 'EPSG:4326', *src_nir.bounds)

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

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''

with open('backend/app/api/analysis.py', 'r') as f:
    content = f.read()
    
content = re.sub(r'class NDVIRequest\(BaseModel\).*?(?=^\@router\.get\("/render"\))', new_func + '\n', content, flags=re.DOTALL | re.MULTILINE)

with open('backend/app/api/analysis.py', 'w') as f:
    f.write(content)
