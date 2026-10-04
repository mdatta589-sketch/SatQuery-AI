import requests

def test_query(q):
    print(f"--- Query: {q}")
    r1 = requests.post('http://127.0.0.1:8000/api/v1/query/route', json={'question': q})
    print("Router:", r1.json())
    task = r1.json()['task']
    if task == 'vqa':
        try:
            r2 = requests.post('http://127.0.0.1:8000/api/v1/vqa/query', json={
                'image_id': 'fake', 'image_type': 'raster', 'source': 'local', 'modality': 'visual', 'representation': 'rgb', 'question': q, 'mode': task
            })
            print("VQA:", r2.json())
        except Exception as e:
            print("VQA Error:", e)

test_query("Is there any visible water in the image?")
test_query("Show me the water bodies")
test_query("Analyze vegetation.")
