import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
        
        await page.goto('http://127.0.0.1:8080')
        await page.wait_for_timeout(2000)
        
        print("ERRORS FOUND:")
        for e in errors:
            print(e)
            
        await browser.close()

asyncio.run(main())
