import urllib.request
import json

req = urllib.request.Request("http://127.0.0.1:8000/api/v1/catalog/search", data=json.dumps({
    "bbox": [12.4, 41.8, 12.5, 41.9],
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
}).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(f"Got {len(data['results'])} results.")
except Exception as e:
    print(f"Error: {e}")
