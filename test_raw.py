import rasterio
import pystac_client
import planetary_computer

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace
)
search = catalog.search(collections=["sentinel-2-l2a"], ids=["S2B_MSIL2A_20260928T153929_R011_T23WMU_20260928T193237"])
item = next(search.items(), None)

b04_url = item.assets["B04"].href
b08_url = item.assets["B08"].href

aoi = {
    'west': -45.2,
    'south': 70.9,
    'east': -45.0,
    'north': 71.0,
}

import sys
sys.path.append('backend')
from app.processing.raster import get_aoi_window_and_transform

with rasterio.Env(CPL_VSIL_CURL_ALLOWED_EXTENSIONS='tif'):
    with rasterio.open(b04_url) as src_red, rasterio.open(b08_url) as src_nir:
        window, window_transform = get_aoi_window_and_transform(src_nir, aoi)
        print("Raw native window:", window)
        
        red_raw = src_red.read(1, window=window)
        nir_raw = src_nir.read(1, window=window)
        
        print("red_raw min:", red_raw.min(), "max:", red_raw.max())
        print("nir_raw min:", nir_raw.min(), "max:", nir_raw.max())
