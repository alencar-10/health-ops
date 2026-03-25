import asyncio

from app.adapters.vivver.http.auth import get_authenticated_session
from app.adapters.vivver.http.catalog import VivverCatalogClient

from app.catalog.catalog_repository import CatalogRepository
from app.catalog.catalog_sync import CatalogSync


BASE_URL = "https://guaraciama-mg-tst.vivver.com"


async def run():

    print("Realizando login...")

    session = await get_authenticated_session()

    print("Sessão criada.")

    client = VivverCatalogClient(BASE_URL, session)

    repo = CatalogRepository()

    sync = CatalogSync(client, repo)

    sync.run()

    print("\n===== RESUMO =====")

    print("Produtos:", len(repo.products))
    print("Princípios ativos:", len(repo.principles))
    print("Unidades:", len(repo.units))
    print("Formas:", len(repo.forms))
    print("Unidades produto:", len(repo.product_units))


if __name__ == "__main__":
    asyncio.run(run())