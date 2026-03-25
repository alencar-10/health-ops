class VivverPrincipleClient:

    def __init__(self, base_url, session):

        self.base_url = base_url
        self.session = session

    def create(self, payload):

        url = f"{self.base_url}/amx/principio_ativo"

        print("POST:", url)

        response = self.session.post(url, data=payload)

        print("POST STATUS:", response.status_code)

        return response