"""
Engine genérica para módulos AMX do Vivver.

Este módulo define a abstração base para qualquer entidade
que siga o padrão /amx/<nome> no sistema Vivver.
"""

from typing import Optional, Dict, List
from requests import Response


class ModuleEngine:
    """
    Engine base para manipulação de módulos AMX.

    Esta classe encapsula operações comuns como:

    - listagem
    - listagem de ativos/inativos
    - ativação
    - inativação

    Args:
        client: Instância de VivverClient autenticado.
        nome (str): Nome do módulo (ex: "produto").

    Attributes:
        client: Cliente HTTP autenticado.
        nome (str): Nome do endpoint AMX.
        campo (str): Prefixo padrão do módulo (ex: amx_produto).
    """

    def __init__(self, client, nome: str):

        if not nome:
            raise ValueError("O nome do módulo não pode ser vazio.")

        self.client = client
        self.nome = nome
        self.campo = f"amx_{nome}"

    # ================= LISTAGEM =================

    def listar(self, filtros: Optional[Dict] = None) -> List[str]:
        """
        Lista registros do módulo via grid.

        Args:
            filtros (dict | None): Parâmetros adicionais de filtro.

        Returns:
            list[str]: Lista de IDs encontrados.
        """
        return self.client.listar_grid(self.nome, filtros)

    def listar_ativos(self) -> List[str]:
        """
        Lista apenas registros ativos.

        Returns:
            list[str]: Lista de IDs ativos.
        """
        filtros = {
            f"{self.campo}[indativo]": "S"
        }
        return self.listar(filtros)

    def listar_inativos(self) -> List[str]:
        """
        Lista apenas registros inativos.

        Returns:
            list[str]: Lista de IDs inativos.
        """
        filtros = {
            f"{self.campo}[indativo]": "N"
        }
        return self.listar(filtros)

    # ================= ALTERAÇÃO DE STATUS =================

    def ativar(self, registro_id: str) -> Response:
        """
        Ativa um registro do módulo.

        Args:
            registro_id (str): ID do registro.

        Returns:
            requests.Response: Resposta HTTP da operação.
        """
        if not registro_id:
            raise ValueError("registro_id não pode ser vazio.")

        payload = {
            f"{self.campo}[id]": registro_id,
            f"{self.campo}[indativo]": "S"
        }

        return self.client.post(f"/amx/{self.nome}", payload)

    def inativar(self, registro_id: str) -> Response:
        """
        Inativa um registro do módulo.

        Args:
            registro_id (str): ID do registro.

        Returns:
            requests.Response: Resposta HTTP da operação.
        """
        if not registro_id:
            raise ValueError("registro_id não pode ser vazio.")

        payload = {
            f"{self.campo}[id]": registro_id,
            f"{self.campo}[indativo]": "N"
        }

        return self.client.post(f"/amx/{self.nome}", payload)