import requests


class VivverCatalogClient:

    def __init__(self, base_url, session):

        self.base_url = base_url.rstrip("/")
        self.session = session

    # ================= REQUEST BÁSICO =================

    def _get(self, endpoint, start=0, length=1000):

        url = f"{self.base_url}{endpoint}"

        params = {
            "start": start,
            "length": length
        }

        response = self.session.get(url, params=params)

        print("\n===== DEBUG VIVVER REQUEST =====")
        print("URL SOLICITADA:", url)
        print("URL FINAL:", response.url)
        print("STATUS:", response.status_code)
        print("CONTENT TYPE:", response.headers.get("content-type"))
        print("================================\n")

        response.raise_for_status()

        data = response.json()

        # Vivver usa "dados", padrão usa "data"
        if isinstance(data, dict):
            if "dados" in data:
                return data["dados"]
            if "data" in data:
                return data["data"]

        return data

    # ================= PAGINAÇÃO =================

    def _get_all_pages(self, endpoint, length=1000):

        start = 0
        all_data = []

        while True:

            data = self._get(endpoint, start=start, length=length)

            if not data:
                break

            all_data.extend(data)

            print(f"Página recebida: {len(data)} | total: {len(all_data)}")

            if len(data) < length:
                break

            start += length

        return all_data

    # ================= CATÁLOGOS =================

    def get_products(self):
        return self._get_all_pages("/amx/produto.json", length=1000)

    def get_principles(self):
        return self._get_all_pages("/amx/principio_ativo.json", length=100)

    def get_units(self):
        return self._get_all_pages("/amx/unidade_medida.json", length=1000)

    def get_forms(self):
        return self._get_all_pages("/amx/forma_farmaceutica.json", length=100)

    def get_product_units(self):
        return self._get_all_pages("/amx/unidade_produto.json", length=100)