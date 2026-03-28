import json
from pathlib import Path
from playwright.async_api import async_playwright
from app.adapters.vivver.http.session import create_session_from_cookies
from app.config.settings import BASE_URL, USERNAME, PASSWORD

COOKIES_FILE = Path(".vivver_cookies.json")


async def get_authenticated_session():

    if not BASE_URL or not USERNAME or not PASSWORD:
        raise ValueError("Configuração inválida: verifique BASE_URL, VIVVER_USERNAME, VIVVER_PASSWORD no .env")

    # tenta reutilizar cookies salvos
    if COOKIES_FILE.exists():
        print("♻️ Tentando reutilizar sessão salva...")
        try:
            cookies = json.loads(COOKIES_FILE.read_text())
            session = create_session_from_cookies(cookies)
            if _session_valida(session):
                print("✅ Sessão reutilizada com sucesso")
                return session
            print("🔄 Sessão inválida, refazendo login...")
        except Exception as e:
            print(f"⚠️ Erro ao carregar cookies: {e}")

    # faz login via Playwright
    cookies = await _login_playwright()

    COOKIES_FILE.write_text(json.dumps(cookies))
    print("💾 Cookies salvos em disco")

    return create_session_from_cookies(cookies)


def _session_valida(session) -> bool:
    try:
        response = session.get(f"{BASE_URL}/desktop", allow_redirects=False)
        if response.status_code in (301, 302):
            location = response.headers.get("Location", "")
            if "/login" in location:
                return False
        return response.status_code == 200
    except Exception:
        return False


async def _login_playwright() -> list:

    print("🔐 Iniciando login via Playwright...")

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(f"{BASE_URL}/desktop")

        await page.fill('input[name="conta"]', USERNAME)
        await page.fill('input[name="password"]', PASSWORD)

        await page.click("div.btn_entrar")

        await page.wait_for_url("**/desktop")

        print("✅ Login realizado")

        cookies = await page.context.cookies()

        await browser.close()

    return cookies