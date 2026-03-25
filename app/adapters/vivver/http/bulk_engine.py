import asyncio


class BulkEngine:

    def __init__(self, workers: int = 5):
        self.workers = workers

    async def executar(self, ids, func):
        """
        Executa operações em lote com controle de concorrência
        e tratamento individual de erro.

        Args:
            ids (list): Lista de IDs a processar.
            func (callable): Função async que recebe (id).

        Returns:
            list[dict]: Resultado estruturado por item.
        """

        semaphore = asyncio.Semaphore(self.workers)
        resultados = []

        async def worker(pid):
            async with semaphore:
                try:
                    response = await func(pid)

                    return {
                        "id": pid,
                        "success": True,
                        "status_code": getattr(response, "status_code", None),
                        "error": None
                    }

                except Exception as e:
                    return {
                        "id": pid,
                        "success": False,
                        "status_code": None,
                        "error": str(e)
                    }

        tasks = [worker(pid) for pid in ids]

        results = await asyncio.gather(*tasks)

        return results