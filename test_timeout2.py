import urllib.request
import json

print("Testing connection to 8000...")
try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/v1/catalog/search", data=json.dumps({
        "bbox": [12.4, 41.8, 12.5, 41.9],
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }).encode('utf-8'), headers={'Content-Type': 'application/json'}, timeout=5) as response:
        print("Backend is responding! Status:", response.getcode())
except Exception as e:
    print(f"Error connecting: {e}")
