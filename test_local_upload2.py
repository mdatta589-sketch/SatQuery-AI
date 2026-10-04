import urllib.request
import json
import io

print("Getting uploaded dataset ID...")
try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/v1/datasets") as response:
        datasets = json.loads(response.read().decode('utf-8'))
        print(datasets)
except Exception as e:
    print(f"Error: {e}")
