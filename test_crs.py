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

with rasterio.Env(CPL_VSIL_CURL_ALLOWED_EXTENSIONS='tif'):
    with rasterio.open(b04_url) as src_red, rasterio.open(b08_url) as src_nir:
        print("B04 bounds:", src_red.bounds)
        print("B04 CRS:", src_red.crs)
        print("B08 bounds:", src_nir.bounds)
        print("B08 CRS:", src_nir.crs)
