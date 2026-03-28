from playwright.async_api import async_playwright
from .session import create_session_from_cookies
from app.config.settings import (
    VIVVER_BASE_URL,
    VIVVER_USERNAME,
    VIVVER_PASSWORD,
)
from app.adapters.vivver.http.session_storage import save_cookies, load_cookies
import requests


def is_session_valid(session):
    try:
        response = session.get(f"{VIVVER_BASE_URL}/desktop", timeout=10)

        # 🔥 valida pelo conteúdo
        if "form-signin" in response.text.lower():
            return False

        if "login" in response.text.lower():
            return False

        return True

    except Exception:
        return False


def get_session_from_disk():
    try:
        cookies = load_cookies()
        print("♻️ Reutilizando sessão salva")
        return create_session_from_cookies(cookies)
    except Exception:
        print("⚠️ Nenhuma sessão salva encontrada")
        return None


async def get_authenticated_session():

    if not VIVVER_BASE_URL or not VIVVER_USERNAME or not VIVVER_PASSWORD:
        raise ValueError(
            "Configuração inválida: verifique VIVVER_BASE_URL, VIVVER_USERNAME, VIVVER_PASSWORD no .env"
        )

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)  # headless=True para rodar sem abrir o navegador

        # ✅ cria contexto corretamente
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(f"{VIVVER_BASE_URL}/login")

        # login
        await page.fill('input[name="conta"]', VIVVER_USERNAME)
        await page.fill('input[name="password"]', VIVVER_PASSWORD)

        await page.click("div.btn_entrar")

        # ✅ espera mínima segura
        await page.wait_for_timeout(3000)

        # ✅ valida erro
        if await page.locator("text=Usuário ou senha inválidos").count() > 0:
            await browser.close()
            raise Exception("Login inválido")

        print("✅ Login realizado")

        cookies = await context.cookies()

        # ✅ salva cookies
        save_cookies(cookies)

        await browser.close()

    return create_session_from_cookies(cookies)