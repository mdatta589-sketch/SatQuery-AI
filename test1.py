import requests

BASE_URL = "http://127.0.0.1:8000"

print("--- 1. Testing /health ---")
r = requests.get(f"{BASE_URL}/health")
print("Health:", r.status_code, r.text)

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
for q, expected in queries.items():
    r = requests.post(f"{BASE_URL}/api/v1/query/route", json={"question": q})
    actual = r.json().get("task")
    print(f"Q: '{q}' -> Actual: {actual} | Expected: {expected}")
