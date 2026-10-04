import asyncio
from fastapi.testclient import TestClient
from app.main import app
import os

# Set dummy URL that is unreachable
os.environ["SATQUERY_VQA_PROVIDER"] = "remote"
os.environ["SATQUERY_VQA_URL"] = "http://localhost:9999/doesnotexist"
os.environ["SATQUERY_VQA_TIMEOUT"] = "1" # fast timeout

client = TestClient(app)

def test_endpoints():
    print("Testing /api/v1/query/route")
    res1 = client.post("/api/v1/query/route", json={"question": "What is in this image?"})
    print(res1.status_code, res1.json())
    
    print("\nTesting /api/v1/vqa/query")
    res2 = client.post("/api/v1/vqa/query", json={
        "image_id": "test_upload.tif",
        "image_type": "raster",
        "source": "user",
        "modality": "optical",
        "representation": "rgb",
        "question": "What is in this image?"
    })
    print(res2.status_code)
    import json
    print(json.dumps(res2.json(), indent=2))

if __name__ == "__main__":
    test_endpoints()
