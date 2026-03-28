import asyncio
from app.adapters.vivver.http.auth import get_browser_context


async def main():
    playwright, browser, context = await get_browser_context()

    try:
        page = await context.new_page()
        await page.goto("https://guaraciama-mg-tst.vivver.com/desktop")

        print("🌐 URL:", page.url)

    finally:
        await context.close()
        await browser.close()
        await playwright.stop()


if __name__ == "__main__":
    asyncio.run(main())