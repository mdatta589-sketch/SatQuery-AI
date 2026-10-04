import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        responses = []
        page.on('response', lambda res: responses.append(res) if 'export/pdf' in res.url else None)
        
        print("Navigating...")
        await page.goto('http://127.0.0.1:8080')
        await page.wait_for_timeout(2000)
        
        print("Bypassing UI to click export button directly...")
        await page.evaluate('document.getElementById("btn-generate-report").click()')
        await page.wait_for_timeout(2000)
        
        print(f"Found {len(responses)} responses.")
        for res in responses:
            print(f"URL: {res.url}")
            print(f"Status: {res.status}")
            try:
                body = await res.text()
                print(f"Body: {body[:500]}")
            except Exception as e:
                print(f"Could not read body: {e}")
                
        await browser.close()

asyncio.run(main())
