import requests

print("Testing Router...")
r = requests.post("http://127.0.0.1:8000/api/v1/query/route", json={"question": "Use optical and SAR together"})
print(r.json())
assert r.json()["task"] == "cross_modal"

print("Testing validation...")
r = requests.post("http://127.0.0.1:8000/api/v1/cross-modal/analyze", json={
    "optical_image_id": "",
    "sar_image_id": "sar-1",
    "question": "test",
    "aoi": {"type": "Polygon", "bbox": {"west": 78.32, "south": 17.41, "east": 78.36, "north": 17.45}}
})
print(r.json())
assert r.status_code == 400

print("All tests passed!")
