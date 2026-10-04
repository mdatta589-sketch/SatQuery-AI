import requests
import json
with open('out.txt', 'w') as f:
    f.write("Starting script...\n")

    try:
        q = "Analyze vegetation"
        r = requests.post("http://127.0.0.1:8000/api/v1/query/route", json={"question": q})
        f.write(f"Route: {r.json()}\n")

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
        f.write(f"Found {len(scenes)} scenes\n")

        if scenes:
            scene_id = scenes[0]["scene_id"]
            f.write(f"Selected scene: {scene_id}\n")
            ndvi_req = {
                "scene_id": scene_id,
                "source_type": "stac",
                "aoi": {
                    "type": "Polygon",
                    "bbox": {"west": 78.32, "south": 17.41, "east": 78.36, "north": 17.45}
                }
            }
            f.write("Sending NDVI request...\n")
            f.flush()
            ndvi_res = requests.post("http://127.0.0.1:8000/api/v1/analysis/ndvi", json=ndvi_req)
            if ndvi_res.ok:
                f.write(f"NDVI SUCCESS: {ndvi_res.json()}\n")
            else:
                f.write(f"NDVI FAILED: {ndvi_res.status_code} {ndvi_res.text}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
