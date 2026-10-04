import requests
import json
print("Starting script...")

q = "Analyze vegetation"
r = requests.post("http://127.0.0.1:8000/api/v1/query/route", json={"question": q})
print("Route:", r.json())

search_req = {
    "bbox": [78.32, 17.41, 78.36, 17.45],
    "start_date": "2025-03-25",
    "end_date": "2025-04-05",
    "max_cloud_cover": 20,
    "collection": "sentinel-2-l2a",
    "limit": 1
}
search_res = requests.post("http://127.0.0.1:8000/api/v1/catalog/search", json=search_req)
scenes = search_res.json().get("results", [])
print(f"Found {len(scenes)} scenes")

if scenes:
    scene_id = scenes[0]["scene_id"]
    print("Selected scene:", scene_id)
    ndvi_req = {
        "scene_id": scene_id,
        "source_type": "stac",
        "aoi": {
            "type": "Polygon",
            "bbox": {"west": 78.32, "south": 17.41, "east": 78.36, "north": 17.45}
        }
    }
    print("Sending NDVI request...")
    ndvi_res = requests.post("http://127.0.0.1:8000/api/v1/analysis/ndvi", json=ndvi_req)
    if ndvi_res.ok:
        print("NDVI SUCCESS!")
    else:
        print("NDVI FAILED:", ndvi_res.status_code, ndvi_res.text)
