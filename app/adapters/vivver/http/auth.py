from playwright.async_api import async_playwright
from app.config.settings import (
    VIVVER_BASE_URL,
    VIVVER_USERNAME,
    VIVVER_PASSWORD,
)
import os

STATE_PATH = "state.json"


async def login_and_save_state():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(f"{VIVVER_BASE_URL}/login")

        await page.fill('input[name="conta"]', VIVVER_USERNAME)
        await page.fill('input[name="password"]', VIVVER_PASSWORD)

        await page.click("div.btn_entrar")
        await page.wait_for_timeout(3000)

        print("✅ Login realizado")

        # 🔥 salva sessão completa
        await context.storage_state(path=STATE_PATH)

        await browser.close()


async def get_browser_context():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        if os.path.exists(STATE_PATH):
            print("♻️ Reutilizando sessão salva")
            context = await browser.new_context(storage_state=STATE_PATH)
        else:
            print("🔄 Sessão não encontrada, realizando login...")
            await login_and_save_state()
            context = await browser.new_context(storage_state=STATE_PATH)

        return browser, context