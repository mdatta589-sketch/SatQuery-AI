
import asyncio
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
import httpx
from PIL import Image

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
load_dotenv(".env")

image_id = "S2A_MSIL2A_20260930T095041_R079_T33UXQ_20260930T145647"

async def test():
    sys.path.insert(0, ".")
    from app.models.vqa.preprocessing import prepare_image
    print("Preparing image...")
    image_path = prepare_image(image_id, "satellite_scene")
    
    print(f"\n[VQA DIAGNOSTIC]")
    print(f"Image sent: {image_path}")
    print(f"File size: {os.path.getsize(image_path)} bytes")
    with Image.open(image_path) as img:
        print(f"Dimensions: {img.size}")
        print(f"Mode: {img.mode}")
    
    question = "Is there a road in the image?"
    print(f"Question sent: '{question}'")

    grounding_url = os.getenv("SATQUERY_GROUNDING_URL")

    print(f"\n[GROUNDING DIAGNOSTIC]")
    print(f"URL: {grounding_url}")
    prompt = "road"
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            files = {"image": (os.path.basename(image_path), image_bytes, "image/png")}
            data = {
                "text": prompt,
                "box_threshold": "0.30",
                "text_threshold": "0.25",
                "image_id": image_id,
                "modality": "optical",
                "representation": "true-color"
            }
            resp = await client.post(grounding_url, data=data, files=files)
            print(f"HTTP Status: {resp.status_code}")
            print(f"Response text: {resp.text[:500]}")
    except Exception as e:
        print(f"Exception: {type(e).__name__} - {str(e)}")

asyncio.run(test())

