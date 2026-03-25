from bs4 import BeautifulSoup
import re


class VivverProductClient:

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def post(self, endpoint, payload):

        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, data=payload)

        print("\n===== HTTP PRODUCT CREATE =====")
        print("URL:", url)
        print("STATUS:", response.status_code)

        return response

    def extract_id(self, response) -> str | None:

        # Tentativa 1: campo hidden no HTML
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            campo = soup.find("input", {"name": "amx_produto[id]"})
            if campo and campo.get("value"):
                produto_id = campo["value"].strip()
                if produto_id:
                    print(f"✅ ID extraído (campo hidden): {produto_id}")
                    return produto_id
        except Exception as e:
            print(f"Falha extração campo hidden: {e}")

        # Tentativa 2: URL após redirect
        try:
            match = re.search(r'/amx/produto/(\d+)', response.url)
            if match:
                produto_id = match.group(1)
                print(f"✅ ID extraído (URL): {produto_id}")
                return produto_id
        except Exception as e:
            print(f"Falha extração URL: {e}")

        # Tentativa 3: regex no body
        try:
            match = re.search(
                r'amx_produto\[id\][^>]*value=["\'](\d+)["\']',
                response.text
            )
            if match:
                produto_id = match.group(1)
                print(f"✅ ID extraído (regex body): {produto_id}")
                return produto_id
        except Exception as e:
            print(f"Falha extração regex: {e}")

        print("⚠️ ID não encontrado no HTML — será capturado via sync")
        return None