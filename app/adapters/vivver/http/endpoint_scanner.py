class EndpointScanner:

    def __init__(self, client):

        self.client = client


    def testar_endpoint(self, modulo):

        url = f"/amx/{modulo}.json"

        try:

            r = self.client.session.get(
                self.client.session.headers["Origin"] + url,
                params={"length": 1}
            )

            if r.status_code == 200 and "data" in r.text:

                print(f"[OK] {modulo}")

                return True

        except Exception:
            pass

        return False


    def scan(self, modulos):

        encontrados = []

        for m in modulos:

            if self.testar_endpoint(m):

                encontrados.append(m)

        return encontrados