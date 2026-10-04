import pystac_client
import planetary_computer

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace
)

search = catalog.search(
    collections=["sentinel-1-grd"],
    bbox=[78.32, 17.41, 78.36, 17.45],
    datetime="2025-03-01/2025-04-10",
    max_items=1
)
items = list(search.items())
if items:
    print(list(items[0].assets.keys()))
else:
    print("No items")
