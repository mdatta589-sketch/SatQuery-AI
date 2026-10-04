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

with rasterio.Env(CPL_VSIL_CURL_ALLOWED_EXTENSIONS='tif'):
    with rasterio.open(b04_url) as src_red:
        # read the whole array, but heavily downsampled
        red_raw = src_red.read(1, out_shape=(1, src_red.height // 100, src_red.width // 100))
        print("Downsampled entire image min:", red_raw.min(), "max:", red_raw.max())
