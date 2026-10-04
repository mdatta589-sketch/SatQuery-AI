import sys; sys.path.append('backend')
from app.main import app
from fastapi.testclient import TestClient
import urllib.request
import base64

# download a real image
req = urllib.request.urlopen('https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png')
img_bytes = req.read()
b64 = base64.b64encode(img_bytes).decode('ascii')
payload = {'image_data': 'data:image/png;base64,' + b64}

client = TestClient(app)
r = client.post('/api/v1/export/pdf', json=payload)
print('STATUS:', r.status_code)
if r.status_code != 200:
    print(r.text)
