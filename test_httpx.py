import httpx
import asyncio

async def main():
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post('http://127.0.0.1:8000/api/v1/vqa/query', json={
                "image_id": "test", "image_type": "raster", "source": "unknown", 
                "modality": "optical", "representation": "rgb", "question": "test", "mode": "vqa"
            })
            print(resp.status_code)
            print(resp.text)
    except Exception as e:
        print(f"Exception: {e}")

asyncio.run(main())
