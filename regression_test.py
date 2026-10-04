import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

results = {}

print("--- 1. Testing /health ---")
try:
    r = requests.get(f"{BASE_URL}/health")
    print("Health:", r.status_code, r.text)
    results["health"] = "PASS" if r.ok else "FAIL"
except Exception as e:
    print("Health failed:", e)
    results["health"] = "FAIL"

print("\n--- 2. Testing Router ---")
queries = {
    "Analyze vegetation": "ndvi",
    "Calculate NDVI": "ndvi",
    "Show me the water bodies": "grounding",
    "Detect buildings": "grounding",
    "Is there any visible water in the image?": "vqa",
    "Is this area urban?": "vqa",
    "Compare these images": "change_vqa",
    "Compare the images and tell me what changed": "change_vqa",
    "What is the weather tomorrow?": "unknown"
}
router_pass = True
for q, expected in queries.items():
    try:
        r = requests.post(f"{BASE_URL}/api/v1/query/route", json={"question": q})
        actual = r.json().get("task")
        print(f"Q: '{q}' -> Actual: {actual} | Expected: {expected}")
        if actual != expected:
            router_pass = False
    except Exception as e:
        print(f"Q: '{q}' -> Error: {e}")
        router_pass = False
results["router"] = "PASS" if router_pass else "FAIL"


print("\n--- 3. Testing STAC Search ---")
stac_pass = False
scene_id_1 = None
scene_id_2 = None
try:
    search_req = {
        "bbox": [78.32, 17.41, 78.36, 17.45],
        "start_date": "2025-03-01",
        "end_date": "2025-04-10",
        "max_cloud_cover": 20,
        "collection": "sentinel-2-l2a",
        "limit": 5
    }
    r = requests.post(f"{BASE_URL}/api/v1/catalog/search", json=search_req)
    scenes = r.json().get("results", [])
    print(f"Found {len(scenes)} scenes")
    if len(scenes) >= 2:
        scene_id_1 = scenes[0]["scene_id"]
        scene_id_2 = scenes[1]["scene_id"]
        print(f"Scene 1: {scene_id_1} (Date: {scenes[0]['datetime']}, Cloud: {scenes[0]['cloud_cover']})")
        print(f"Scene 2: {scene_id_2} (Date: {scenes[1]['datetime']}, Cloud: {scenes[1]['cloud_cover']})")
        if "2025-03-28" not in scene_id_1 and "2025-04-02" not in scene_id_1:
             stac_pass = True
    else:
        print("Not enough scenes found!")
except Exception as e:
    print("STAC Search failed:", e)
results["stac_search"] = "PASS" if stac_pass else "FAIL"


print("\n--- 4. Testing NDVI End-to-End ---")
ndvi_pass = False
if scene_id_1:
    try:
        ndvi_req = {
            "scene_id": scene_id_1,
            "source_type": "stac",
            "aoi": {
                "type": "Polygon",
                "bbox": {"west": 78.32, "south": 17.41, "east": 78.36, "north": 17.45}
            }
        }
        r = requests.post(f"{BASE_URL}/api/v1/analysis/ndvi", json=ndvi_req)
        if r.ok:
            data = r.json()
            stats = data.get("statistics", {})
            print("NDVI Min:", stats.get("min"))
            print("NDVI Max:", stats.get("max"))
            print("NDVI Mean:", stats.get("mean"))
            print("NDVI Median:", stats.get("median"))
            print("Valid Pixels:", stats.get("valid_pixel_count"))
            print("Veg %:", stats.get("vegetation_area_percentage"))
            print("Image URL:", data.get("image_url"))
            if stats.get("mean") is not None and data.get("image_url"):
                ndvi_pass = True
        else:
            print("NDVI error:", r.status_code, r.text)
    except Exception as e:
        print("NDVI testing failed:", e)
results["ndvi"] = "PASS" if ndvi_pass else "FAIL"


print("\n--- 5. Testing VQA ---")
vqa_pass = False
if scene_id_1:
    try:
        vqa_req = {
            "image_id": scene_id_1,
            "image_type": "optical",
            "source": "stac",
            "modality": "optical",
            "representation": "true_color",
            "question": "Is there any visible water in the image?",
            "mode": "vqa",
            "aoi": {
                "type": "Polygon",
                "bbox": {"west": 78.32, "south": 17.41, "east": 78.36, "north": 17.45}
            }
        }
        r = requests.post(f"{BASE_URL}/api/v1/vqa/query", json=vqa_req)
        if r.ok:
            print("VQA Response:", r.json())
            vqa_pass = True
        else:
            print("VQA Error:", r.status_code, r.text)
    except Exception as e:
        print("VQA testing failed:", e)
results["vqa"] = "PASS" if vqa_pass else "FAIL"


print("\n--- 6. Testing Grounding ---")
grounding_pass = False
if scene_id_1:
    try:
        grounding_req = {
            "image_id": scene_id_1,
            "image_type": "optical",
            "source": "stac",
            "modality": "optical",
            "representation": "true_color",
            "question": "Show me the water bodies",
            "mode": "grounding",
            "aoi": {
                "type": "Polygon",
                "bbox": {"west": 78.32, "south": 17.41, "east": 78.36, "north": 17.45}
            }
        }
        r = requests.post(f"{BASE_URL}/api/v1/vqa/query", json=grounding_req)
        if r.ok:
            print("Grounding Response:", r.json())
            grounding_pass = True
        else:
            print("Grounding Error:", r.status_code, r.text)
    except Exception as e:
        print("Grounding testing failed:", e)
results["grounding"] = "PASS" if grounding_pass else "FAIL"


print("\n--- 7. Testing Change-VQA ---")
change_pass = False
if scene_id_1 and scene_id_2:
    try:
        change_req = {
            "image_before_id": scene_id_1,
            "image_after_id": scene_id_2,
            "question": "Compare the images and tell me what changed",
            "aoi": {
                "type": "Polygon",
                "bbox": {"west": 78.32, "south": 17.41, "east": 78.36, "north": 17.45}
            }
        }
        r = requests.post(f"{BASE_URL}/api/v1/change/vqa", json=change_req)
        if r.ok:
            data = r.json()
            print("Change %:", data.get("change_percentage"))
            print("Changed pixels:", data.get("changed_pixel_count"))
            print("Valid pixels:", data.get("total_valid_pixel_count"))
            print("Before:", data.get("before_scene"))
            print("After:", data.get("after_scene"))
            if data.get("change_percentage") is not None:
                change_pass = True
        else:
            print("Change-VQA error:", r.status_code, r.text)
    except Exception as e:
        print("Change-VQA testing failed:", e)
results["change_vqa"] = "PASS" if change_pass else "FAIL"


print("\n=== FINAL RESULTS ===")
print(json.dumps(results, indent=2))
