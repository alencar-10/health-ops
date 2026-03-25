"""
Módulo de cliente HTTP do Vivver SDK.

Este módulo contém a implementação do cliente responsável por
toda comunicação autenticada com o sistema Vivver.
"""

import requests
from bs4 import BeautifulSoup
import unicodedata

# ================= CONFIGURAÇÃO BASE =================

BASE = "https://guaraciama-mg-tst.vivver.com"


class VivverClient:
    """
    Cliente HTTP autenticado para comunicação com o sistema Vivver.

    Este cliente:

    - Inicializa uma sessão HTTP com cookies autenticados
    - Obtém automaticamente tokens CSRF
    - Encapsula chamadas GET e POST
    - Fornece métodos auxiliares para consulta de dados via grid

    Attributes:
        session (requests.Session): Sessão HTTP persistente autenticada.
        authenticity_token (str): Token necessário para requisições POST.
    """

    def __init__(self, cookies: list[dict]):
        """
        Inicializa o cliente com cookies previamente obtidos via login.

        Args:
            cookies (list[dict]): Lista de cookies no formato:
                [{"name": "...", "value": "..."}]

        Raises:
            Exception: Se não for possível obter tokens CSRF.
        """
        self.session = requests.Session()

        for c in cookies:
            self.session.cookies.set(
                name=c["name"],
                value=c["value"]
            )

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": BASE,
            "Referer": BASE + "/amx/produto"
        })

        self._csrf()

    # ================= NORMALIZAÇÃO =================

    @staticmethod
    def normalizar(texto: str) -> str:
        """
        Normaliza texto removendo acentos e convertendo para caixa alta.

        Args:
            texto (str): Texto original.

        Returns:
            str: Texto normalizado (uppercase, sem acentuação).
        """
        texto = str(texto).upper().strip()
        texto = unicodedata.normalize("NFD", texto)
        texto = texto.encode("ascii", "ignore").decode("utf-8")
        return texto

    # ================= OBTENÇÃO CSRF =================

    def _csrf(self) -> None:
        """
        Obtém tokens CSRF necessários para requisições POST.

        Este método:
        - Carrega uma página AMX
        - Extrai meta csrf-token
        - Extrai authenticity_token
        - Atualiza headers da sessão

        Raises:
            Exception: Se não for possível localizar os tokens na página.
        """
        r = self.session.get(BASE + "/amx/principio_ativo")

        if r.status_code != 200:
            raise Exception("Erro ao carregar tela para CSRF.")

        soup = BeautifulSoup(r.text, "html.parser")

        meta = soup.find("meta", {"name": "csrf-token"})
        if not meta:
            raise Exception("CSRF meta não encontrado.")

        self.session.headers["x-csrf-token"] = meta["content"]

        input_token = soup.find("input", {"name": "authenticity_token"})
        if not input_token:
            raise Exception("authenticity_token não encontrado.")

        self.authenticity_token = input_token["value"]

        print("[OK] CSRF e authenticity_token carregados")

    # ================= BUSCAR MAPA DE VIAS =================

    def obter_mapa_vias(self) -> dict[str, str]:
        """
        Obtém o mapa de vias de administração disponíveis no sistema.

        Returns:
            dict[str, str]: Dicionário no formato:
                { "NOME_NORMALIZADO": "CODIGO" }

        Raises:
            Exception: Se a requisição HTTP falhar.
        """
        url = BASE + "/fwk/lookup_edit_v3"

        params = {
            "query": "",
            "page": 1,
            "limit": 200,
            "model": "Amx::ViaAdministracao",
            "scope": "",
            "key": "codviaadministracao",
            "name": "desviaadministracao",
            "type": "name",
            "where": "",
            "columns": "codviaadministracao,desviaadministracao,codviaadministracao",
            "sort_by": "",
            "similarity": "false",
            "cache": "true",
            "cache_expires": ""
        }

        r = self.session.get(url, params=params)

        if r.status_code != 200:
            raise Exception("Erro ao buscar vias via API.")

        data = r.json()
        mapa = {}

        for item in data.get("rows", []):
            codigo = str(item.get("codviaadministracao"))
            nome_original = item.get("desviaadministracao", "")
            nome_normalizado = self.normalizar(nome_original)

            if codigo and nome_normalizado:
                mapa[nome_normalizado] = codigo

        return mapa

    # ================= LISTAR GRID GENÉRICO =================

    def listar_grid(self, modulo: str, filtros: dict | None = None) -> list[str]:
        """
        Lista registros de um módulo via grid JSON paginado.

        Args:
            modulo (str): Nome do endpoint AMX (ex: "produto").
            filtros (dict | None): Parâmetros adicionais de filtro.

        Returns:
            list[str]: Lista de IDs (DT_RowId) encontrados.
        
        Raises:
            Exception: Se a requisição HTTP falhar.
        """
        start = 0
        length = 100
        ids = []

        if filtros is None:
            filtros = {}

        while True:
            params = {
                "draw": 1,
                "start": start,
                "length": length,
                "search[value]": "",
                "search[regex]": "false",
                "order[0][column]": 0,
                "order[0][dir]": "desc",
                "workMode": "wmSearchResult",
                "oldWorkMode": "wmSearch"
            }

            params.update(filtros)

            url = f"{BASE}/amx/{modulo}.json"

            r = self.session.get(url, params=params)

            if r.status_code != 200:
                raise Exception(f"Erro ao buscar grid {modulo}")

            data = r.json()
            rows = data.get("data", [])

            if not rows:
                break

            for row in rows:
                pid = row.get("DT_RowId")
                if pid:
                    ids.append(pid)

            start += length

            print(f"{modulo}: carregados {len(ids)} registros...")

        return ids

    # ================= POST =================

   
    def post(self, path: str, payload: dict) -> requests.Response:
        """
        Executa requisição POST autenticada.

        Args:
            path (str): Caminho relativo (ex: "/amx/produto").
            payload (dict): Dados do formulário a serem enviados.

        Returns:
            requests.Response: Objeto de resposta HTTP.

        Raises:
            requests.RequestException: Se ocorrer erro de conexão.
        """
        payload["authenticity_token"] = self.authenticity_token

        r = self.session.post(
            BASE + path,
            data=payload,
            timeout=30
        )

        return r