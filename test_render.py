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
        if len(data) > 0:
            scene_id = data[0]["scene_id"]
            print(f"Found scene: {scene_id}")
            
            try:
                res2 = urllib.request.urlopen(f"http://127.0.0.1:8000/api/v1/catalog/scene/{scene_id}")
                print(f"Metadata status: {res2.getcode()}")
            except Exception as e:
                print(f"Metadata error: {e}")
                
            try:
                res3 = urllib.request.urlopen(f"http://127.0.0.1:8000/api/v1/catalog/scene/{scene_id}/true-color/preview")
                print(f"True color preview status: {res3.getcode()}")
            except Exception as e:
                print(f"True color error: {e}")
                if hasattr(e, 'read'):
                    print(e.read().decode())
except Exception as e:
    print(f"Error: {e}")
