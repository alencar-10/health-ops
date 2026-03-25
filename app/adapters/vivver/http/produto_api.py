class ProdutoAPI:

    def __init__(self, client):
        self.client = client

    def cadastrar(self, payload):

        return self.client.post_amx(
            "produto",
            payload
        )