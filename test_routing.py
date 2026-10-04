import requests

tests = [
    ("compare the images and tell me the difference", "change_vqa"),
    ("how much of the area changed?", "change_vqa"),
    ("analyze vegetation", "ndvi"),
    ("calculate NDVI", "ndvi"),
    ("show me the water bodies", "grounding"),
    ("detect buildings", "grounding"),
    ("is there water in this image?", "vqa"),
    ("is this area urban?", "vqa"),
    ("what is the weather tomorrow?", "unknown")
]

passed = 0
for q, expected in tests:
    try:
        res = requests.post("http://127.0.0.1:8000/api/v1/query/route", json={"question": q})
        task = res.json().get("task")
        if task == expected:
            passed += 1
            print(f"PASS: '{q}' -> {task}")
        else:
            print(f"FAIL: '{q}' -> expected {expected}, got {task}")
    except Exception as e:
        print(f"ERROR on '{q}': {e}")

print(f"\nRESULTS: {passed}/{len(tests)} passed.")
