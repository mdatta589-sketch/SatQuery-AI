import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_endpoints():
    print("Testing /api/v1/change/analyze with missing images")
    res1 = client.post("/api/v1/change/analyze", json={
        "image_before_id": "nonexistent1.tif",
        "image_after_id": "nonexistent2.tif",
        "aoi": None
    })
    print(res1.status_code, res1.json())
    
    # Check if we have two test images
    # We saw test2.png and test3.png in the backend folder earlier
    print("\nTesting /api/v1/change/analyze with actual images")
    import shutil
    os.makedirs("temp/uploads", exist_ok=True)
    if os.path.exists("test2.png") and os.path.exists("test3.png"):
        shutil.copy("test2.png", "temp/uploads/test2.png")
        shutil.copy("test3.png", "temp/uploads/test3.png")
        
        res2 = client.post("/api/v1/change/analyze", json={
            "image_before_id": "test2.png",
            "image_after_id": "test3.png",
            "aoi": None
        })
        print(res2.status_code)
        import json
        print(json.dumps(res2.json(), indent=2))
    else:
        print("Test images test2.png and test3.png not found for full test.")

if __name__ == "__main__":
    test_endpoints()
