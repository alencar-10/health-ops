class VivverProductLinkClient:

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url


    def link_principle(self, product_id, principle_id):

        url = f"{self.base_url}/amx/produto/{product_id}"

        payload = {
            "utf8": "✓",
            "_method": "patch",
            "workMode": "wmEdit",
            "oldWorkMode": "wmBrowse",

            "amx_produto[id]": product_id,
            "amx_produto[id_principioativo]": principle_id
        }

        print("\n===== LINK PRINCIPLE =====")
        for k, v in payload.items():
            print(k, "=", v)

        response = self.session.post(url, data=payload)

        print("POST:", url)
        print("STATUS:", response.status_code)

        if response.status_code != 200:
            print("Erro ao vincular princípio:", response.status_code)
            return "ERROR_HTTP"

        return "OK"