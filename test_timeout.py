import urllib.request
import json
import io

print("Testing connection to 8000...")
try:
    with urllib.request.urlopen("http://127.0.0.1:8000/docs", timeout=5) as response:
        print("Backend is responding! Status:", response.getcode())
except Exception as e:
    print(f"Error connecting: {e}")
