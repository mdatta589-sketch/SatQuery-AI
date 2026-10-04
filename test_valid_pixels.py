import rasterio
from rasterio.vrt import WarpedVRT
from rasterio.warp import calculate_default_transform
from rasterio.enums import Resampling
import numpy as np
import pystac_client
import planetary_computer

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace
)
search = catalog.search(collections=["sentinel-2-l2a"], ids=["S2B_MSIL2A_20260928T153929_R011_T23WMU_20260928T193237"])
item = next(search.items(), None)

if not item:
    print("Item not found.")
    exit(1)

b04_url = item.assets["B04"].href
b08_url = item.assets["B08"].href

aoi = {
    'west': -45.2,
    'south': 70.9,
    'east': -45.0,
    'north': 71.0,
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[[-45.2, 70.9], [-45.0, 70.9], [-45.0, 71.0], [-45.2, 71.0], [-45.2, 70.9]]]
    }
}

import sys
sys.path.append('backend')
from app.processing.raster import get_aoi_window_and_transform

with rasterio.Env(CPL_VSIL_CURL_ALLOWED_EXTENSIONS='tif'):
    with rasterio.open(b04_url) as src_red, rasterio.open(b08_url) as src_nir:
        window, window_transform = get_aoi_window_and_transform(src_nir, aoi)
        window_bounds = rasterio.windows.bounds(window, src_nir.transform)
        transform, width, height = calculate_default_transform(
            src_nir.crs, 'EPSG:3857', int(window.width), int(window.height), *window_bounds
        )

        vrt_options = {
            'crs': 'EPSG:3857',
            'transform': transform,
            'width': width,
            'height': height,
            'resampling': Resampling.bilinear,
        }

        # Scale output array down
        max_dim = 1024
        scale = min(1.0, max_dim / max(width, height))
        dst_width = max(1, int(width * scale))
        dst_height = max(1, int(height * scale))
        scaled_transform = transform * transform.scale((width / dst_width), (height / dst_height))

        with WarpedVRT(src_red, **vrt_options) as vrt_red, WarpedVRT(src_nir, **vrt_options) as vrt_nir:
            red_data = vrt_red.read(1, out_shape=(dst_height, dst_width), resampling=Resampling.bilinear).astype(np.float32)
            nir_data = vrt_nir.read(1, out_shape=(dst_height, dst_width), resampling=Resampling.bilinear).astype(np.float32)
            
            print("dst_shape:", red_data.shape)
            print("red_data min:", red_data.min(), "max:", red_data.max(), "mean:", red_data.mean())
            print("nir_data min:", nir_data.min(), "max:", nir_data.max(), "mean:", nir_data.mean())
            
            red_valid = (red_data > 0).sum()
            nir_valid = (nir_data > 0).sum()
            print(f"Red > 0: {red_valid} pixels")
            print(f"NIR > 0: {nir_valid} pixels")
            
            valid_mask = (red_data > 0) & (nir_data > 0)
            print(f"Combined valid_mask > 0: {valid_mask.sum()} pixels")
            
            geom_3857 = rasterio.warp.transform_geom('EPSG:4326', 'EPSG:3857', aoi['geometry'])
            import rasterio.features
            poly_mask = rasterio.features.geometry_mask(
                [geom_3857],
                out_shape=(dst_height, dst_width),
                transform=scaled_transform,
                invert=True,
                all_touched=True
            )
            
            print(f"poly_mask inside AOI (True): {poly_mask.sum()} pixels")
            
            final_mask = valid_mask & poly_mask
            print(f"final valid pixels: {final_mask.sum()} pixels")
