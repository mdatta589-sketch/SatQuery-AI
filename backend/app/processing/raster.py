import rasterio
import numpy as np
import os
import uuid

def read_raster_metadata(file_path: str):
    with rasterio.open(file_path) as src:
        bounds = src.bounds
        crs_str = str(src.crs) if src.crs else None
        
        # Read a small sample to get min/max without OOM
        try:
            out_shape = (max(1, src.height // 8), max(1, src.width // 8))
            band1 = src.read(1, out_shape=out_shape)
            nodata = src.nodata
            valid = band1[band1 != nodata] if nodata is not None else band1
            min_val = float(np.min(valid))
            max_val = float(np.max(valid))
            p2, p98 = np.percentile(valid, [2, 98])
            p2 = float(p2)
            p98 = float(p98)
        except Exception:
            min_val = 0.0
            max_val = 65535.0
            p2 = min_val
            p98 = max_val

        return {
            "width": src.width,
            "height": src.height,
            "bands": src.count,
            "crs": crs_str,
            "dtype": str(src.dtypes[0]) if src.count > 0 else None,
            "driver": src.driver,
            "bounds": bounds,
            "resolution": float(abs(src.res[0])),
            "min_val": min_val,
            "max_val": max_val,
            "p2": p2,
            "p98": p98
        }


from rasterio.vrt import WarpedVRT
from PIL import Image

def create_raster_preview(src_path: str, dst_path: str, vmin: float = None, vmax: float = None):
    with rasterio.open(src_path) as src:
        # Reproject to Web Mercator (EPSG:3857) to avoid Leaflet distortion
        # Downscale by 8 for performance
        out_shape = (
            max(1, src.height // 8),
            max(1, src.width // 8)
        )
        
        with WarpedVRT(src, crs='EPSG:3857') as vrt:
            band1 = vrt.read(1, out_shape=out_shape).astype('float32')
            nodata = vrt.nodata
            valid_mask = (band1 != nodata) if nodata is not None else np.ones(band1.shape, dtype=bool)
            
            valid = band1[valid_mask]
            if len(valid) == 0:
                valid = band1
                
            if vmin is None or vmax is None:
                p2, p98 = np.percentile(valid, [2, 98])
                vmin = float(p2) if vmin is None else vmin
                vmax = float(p98) if vmax is None else vmax
                
            band1 = np.clip(band1, vmin, vmax)
            range_val = vmax - vmin
            if range_val == 0:
                range_val = 1
                
            norm = ((band1 - vmin) / range_val * 255).astype('uint8')
            
            # create RGBA to mask nodata transparently
            rgba = np.zeros((norm.shape[0], norm.shape[1], 4), dtype=np.uint8)
            rgba[:, :, 0] = norm
            rgba[:, :, 1] = norm
            rgba[:, :, 2] = norm
            rgba[:, :, 3] = np.where(valid_mask, 255, 0).astype(np.uint8)
            
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            img = Image.fromarray(rgba, 'RGBA')
            img.save(dst_path)
def get_aoi_window_and_transform(src, aoi: dict):
    from rasterio.warp import transform_bounds
    from rasterio.windows import from_bounds
    from fastapi import HTTPException
    
    bbox = aoi.get('bbox', aoi) if isinstance(aoi, dict) else aoi
    if 'west' not in bbox and hasattr(aoi, 'bbox'):
        # Just in case it's an object with bbox attribute
        pass # Handle gracefully below if needed
    
    if bbox.get('west') == bbox.get('east') or bbox.get('south') == bbox.get('north'):
        raise HTTPException(status_code=400, detail="Point AOI cannot be used for NDVI. Please select a rectangle or polygon.")
        
    # aoi must have west, south, east, north in EPSG:4326
    bbox = aoi.get('bbox', aoi) if isinstance(aoi, dict) else aoi
    wgs84_bounds = [bbox['west'], bbox['south'], bbox['east'], bbox['north']]
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
    return window, src.window_transform(window)
