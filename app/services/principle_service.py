class PrincipleService:

    def __init__(self, client, payload_builder):
        self.client = client
        self.payload_builder = payload_builder

    def create(self, codigo, nome, codforma):

        payload = self.payload_builder.build(
            codigo,
            nome,
            codforma
        )

        response = self.client.create(payload)

        if response.status_code == 200:
            return "CREATED"

        return "ERROR"