import sys
sys.path.append('backend')
from app.api.catalog import search_catalog, CatalogSearchRequest

print("Searching...")
req = CatalogSearchRequest(
    bbox=[12.4, 41.8, 12.5, 41.9],
    start_date="2023-01-01",
    end_date="2023-12-31"
)
res = search_catalog(req)
if res and res["results"]:
    scene_id = res["results"][0]["scene_id"]
    print("Found real scene_id:", scene_id)
    
    from app.api.catalog import render_true_color
    res_img = render_true_color(scene_id)
    print("Success, length of image:", len(res_img.body))
else:
    print("No results")
