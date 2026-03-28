import asyncio
from app.adapters.vivver.http.auth import get_browser_context


async def main():
    browser, context = await get_browser_context()

    page = await context.new_page()
    await page.goto("https://guaraciama-mg-tst.vivver.com/desktop")

    print("🌐 URL:", page.url)

    await browser.close()


asyncio.run(main())