import pystac_client
import planetary_computer

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace
)
search = catalog.search(collections=["sentinel-2-l2a"], ids=["S2C_MSIL2A_20260928T095031_R079_T33UXQ_20260928T131313"])
item = next(search.items(), None)
print("Item found:", item is not None)
