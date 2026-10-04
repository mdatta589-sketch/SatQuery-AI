import requests

payload = {
    "image_before_id": "S2B_MSIL2A_20250328T050659_R019_T44QKE_20250328T072008",
    "image_after_id": "S2C_MSIL2A_20250402T050711_R019_T44QKE_20250402T101606",
    "question": "how much of the area changed?",
    "aoi": {
        "geometry_type": "Polygon",
        "type": "Polygon",
        "bbox": {
            "west": 78.32,
            "north": 17.45,
            "east": 78.36,
            "south": 17.41
        }
    }
}

try:
    res = requests.post("http://127.0.0.1:8000/api/v1/change/vqa", json=payload)
    data = res.json()
    print("ANSWER:", data.get("answer"))
except Exception as e:
    print("FAILED:", e)
