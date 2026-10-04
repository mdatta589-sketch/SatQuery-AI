import requests
res = requests.post("http://127.0.0.1:8000/api/v1/query/route", json={"question": "Is there any visible water in the image?"})
print(res.json())
