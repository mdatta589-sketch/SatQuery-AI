import requests

req_data = {
    "scene_id": "S2B_MSIL2A_20260928T153929_R011_T23WMU_20260928T193237",
    "source_type": "stac",
    "aoi": {
        "type": "bbox",
        "shape": "Rectangle",
        "area": 1000000,
        "north": 71.0,
        "south": 70.9,
        "east": -47.4,
        "west": -47.6,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[-47.6, 70.9], [-47.4, 70.9], [-47.4, 71.0], [-47.6, 71.0], [-47.6, 70.9]]]
        }
    }
}

res = requests.post("http://127.0.0.1:8000/api/v1/analysis/ndvi", json=req_data)
print("Status:", res.status_code)
print("Response:", res.text)
