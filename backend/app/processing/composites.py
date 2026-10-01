import os
import rasterio
import numpy as np

from rasterio.vrt import WarpedVRT
from PIL import Image

def create_rgb_composite(red_path: str, green_path: str, blue_path: str, dst_path: str, vmins: list = None, vmaxs: list = None):
    """
    Creates an RGB composite PNG from three input GeoTIFF paths.
    vmins and vmaxs should be lists of [red_vmin, green_vmin, blue_vmin] and similarly for vmaxs.
    If not provided, robust 2nd-98th percentile stretch will be calculated independently for each band.
    """
    paths = [red_path, green_path, blue_path]
    out_bands = []
    
    # We will use WarpedVRT to reproject to Web Mercator (EPSG:3857)
    # Open all three to ensure they align
    valid_mask = None
    
    with rasterio.open(paths[0]) as src0:
        out_shape = (max(1, src0.height // 8), max(1, src0.width // 8))
        
    for i, path in enumerate(paths):
        with rasterio.open(path) as src:
            with WarpedVRT(src, crs='EPSG:3857') as vrt:
                band = vrt.read(1, out_shape=out_shape).astype('float32')
                nodata = vrt.nodata
                current_valid_mask = (band != nodata) if nodata is not None else np.ones(band.shape, dtype=bool)
                
                if valid_mask is None:
                    valid_mask = current_valid_mask
                else:
                    valid_mask = valid_mask & current_valid_mask
                    
                valid = band[valid_mask]
                if len(valid) == 0:
                    valid = band
                
                if vmins is not None and vmaxs is not None:
                    vmin = vmins[i]
                    vmax = vmaxs[i]
                else:
                    try:
                        p2, p98 = np.percentile(valid, [2, 98])
                        vmin = float(p2)
                        vmax = float(p98)
                    except Exception:
                        vmin = 0.0
                        vmax = 65535.0
                        
                band = np.clip(band, vmin, vmax)
                range_val = vmax - vmin
                if range_val == 0:
                    range_val = 1
                    
                norm = ((band - vmin) / range_val * 255).astype('uint8')
                out_bands.append(norm)
                
    # Create RGBA array
    rgba = np.zeros((out_bands[0].shape[0], out_bands[0].shape[1], 4), dtype=np.uint8)
    rgba[:, :, 0] = out_bands[0]
    rgba[:, :, 1] = out_bands[1]
    rgba[:, :, 2] = out_bands[2]
    rgba[:, :, 3] = np.where(valid_mask, 255, 0).astype(np.uint8)
    
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    img = Image.fromarray(rgba, 'RGBA')
    img.save(dst_path)
