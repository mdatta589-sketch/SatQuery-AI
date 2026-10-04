import rasterio
import pystac_client
import planetary_computer
from rasterio.windows import Window

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace
)
search = catalog.search(collections=["sentinel-2-l2a"], ids=["S2B_MSIL2A_20260928T153929_R011_T23WMU_20260928T193237"])
item = next(search.items(), None)

b04_url = item.assets["B04"].href

with rasterio.Env(CPL_VSIL_CURL_ALLOWED_EXTENSIONS='tif'):
    with rasterio.open(b04_url) as src_red:
        center_x = src_red.width // 2
        center_y = src_red.height // 2
        window = Window(col_off=center_x - 50, row_off=center_y - 50, width=100, height=100)
        
        red_raw = src_red.read(1, window=window)
        print("Center window red min:", red_raw.min(), "max:", red_raw.max())
