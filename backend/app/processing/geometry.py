import rasterio
from rasterio.warp import transform as warp_transform

def pixel_to_geographic(image_path: str, px: float, py: float) -> tuple:
    """
    Given an image path and pixel coordinates (x, y), returns (lon, lat) in WGS84.
    If the image has no geographic transform (e.g. standard PNG), returns (None, None) 
    or handles it gracefully.
    """
    try:
        with rasterio.open(image_path) as src:
            # If the image has an identity transform, it might just be a regular image
            if src.transform.is_identity:
                return (None, None)
                
            # Convert pixel (py, px) -> (x, y) in the raster's CRS
            # rasterio.transform.xy takes (transform, row, col)
            spatial_x, spatial_y = rasterio.transform.xy(src.transform, py, px)
            
            # If the CRS is already EPSG:4326, we are done
            if src.crs and src.crs.to_string() == "EPSG:4326":
                return (spatial_x, spatial_y)
                
            # Otherwise transform from src.crs to EPSG:4326
            if src.crs:
                xs, ys = warp_transform(src.crs, 'EPSG:4326', [spatial_x], [spatial_y])
                return (xs[0], ys[0])
                
            return (None, None)
    except Exception:
        return (None, None)
