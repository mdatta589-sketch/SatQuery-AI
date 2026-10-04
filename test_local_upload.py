import urllib.request
import json
import io

print("Getting uploaded dataset ID...")
try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/v1/datasets") as response:
        datasets = json.loads(response.read().decode('utf-8'))
        
    if not datasets:
        print("No datasets uploaded.")
    else:
        dataset_id = datasets[0]['id']
        print(f"Testing dataset: {dataset_id}")
        
        url = f"http://127.0.0.1:8000/api/v1/datasets/{dataset_id}/preview?band=B04"
        print("Fetching preview URL:", url)
        
        try:
            with urllib.request.urlopen(url) as img_resp:
                img_data = img_resp.read()
                print(f"Success! Image size: {len(img_data)} bytes")
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.code} - {e.read().decode()}")
except Exception as e:
    print(f"Error: {e}")
