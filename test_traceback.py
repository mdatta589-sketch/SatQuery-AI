import subprocess
import time
import urllib.request
import json
import base64

# A valid 1x1 png
b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
img_data = 'data:image/png;base64,' + b64

payload = {
    'layer': {'name': 'Test Layer', 'id': 'stac:123', 'stac_properties': {}},
    'aoi': {'type': 'Polygon', 'area': 100, 'bounds': {'north': 10, 'south': 5, 'east': 10, 'west': 5}},
    'ndvi': {
        'analysis': 'NDVI',
        'statistics': {'min': 0, 'max': 1, 'mean': 0.5, 'median': 0.5, 'total_pixel_count': 100, 'valid_pixel_count': 100, 'nodata_pixel_count': 0},
        'formula': '(NIR - Red) / (NIR + Red)'
    },
    'vqa': {
        'question': 'Test',
        'answer': 'Test',
        'confidence_status': 'calibrated',
        'execution': {'model': 'test-model'}
    },
    'image_data': img_data
}

p = subprocess.Popen(['backend/.venv/Scripts/python', '-m', 'uvicorn', 'app.main:app', '--port', '8005'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, cwd='backend')
time.sleep(3)

req = urllib.request.Request(
    'http://127.0.0.1:8005/api/v1/export/pdf',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        print('STATUS:', response.status)
except urllib.error.HTTPError as e:
    print('STATUS:', e.code)
    print(e.read().decode('utf-8'))
except Exception as e:
    print('ERROR:', e)

p.terminate()
stdout, stderr = p.communicate()
print('--- STDERR ---')
print(stderr)
