import asyncio
from playwright.async_api import async_playwright
from app.config.settings import BASE_URL

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(BASE_URL)
        print(await page.title())
        
        await browser.close()

asyncio.run(main())