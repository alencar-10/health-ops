from playwright.async_api import async_playwright
from .session import create_session_from_cookies
from app.config.settings import VIVVER_BASE_URL, VIVVER_USERNAME, VIVVER_PASSWORD


async def get_authenticated_session():

    if not VIVVER_BASE_URL or not VIVVER_USERNAME or not VIVVER_PASSWORD:
        raise ValueError("Configuração inválida: verifique VIVVER_BASE_URL, VIVVER_USERNAME, VIVVER_PASSWORD no .env")

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(f"{VIVVER_BASE_URL}/desktop")

        await page.fill('input[name="conta"]', VIVVER_USERNAME)
        await page.fill('input[name="password"]', VIVVER_PASSWORD)

        await page.click("div.btn_entrar")

        await page.wait_for_url("**/desktop")

        print("✅ Login realizado")

        cookies = await page.context.cookies()

        await browser.close()

    return create_session_from_cookies(cookies)