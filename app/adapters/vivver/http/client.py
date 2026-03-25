import requests


class VivverHTTPClient:

    def __init__(self, base_url: str, usuario: str, senha: str):
        self.base_url = base_url
        self.usuario = usuario
        self.senha = senha
        self.session = requests.Session()

    def login(self):

        payload = {
            "username": self.usuario,
            "password": self.senha
        }

        response = self.session.post(
            f"{self.base_url}/desktop/login",
            data=payload
        )

        response.raise_for_status()

        return response

    def post_amx(self, endpoint: str, payload: dict):

        url = f"{self.base_url}/amx/{endpoint}"

        response = self.session.post(url, data=payload)

        response.raise_for_status()

        return response.json()