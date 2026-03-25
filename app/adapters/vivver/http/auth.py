from playwright.async_api import async_playwright
from .session import create_session_from_cookies

BASE = "https://guaraciama-mg-tst.vivver.com"

USUARIO = "35304775830"
SENHA = "kloq230"


async def get_authenticated_session():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(BASE + "/desktop")

        await page.fill('input[name="conta"]', USUARIO)
        await page.fill('input[name="password"]', SENHA)

        await page.click("div.btn_entrar")

        await page.wait_for_url("**/desktop")

        print("[OK] Login realizado")

        cookies = await page.context.cookies()

        await browser.close()

    session = create_session_from_cookies(cookies)

    return session