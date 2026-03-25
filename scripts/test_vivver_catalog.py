import asyncio

from app.adapters.vivver.http.catalog import VivverCatalogClient
from app.adapters.vivver.http.auth import get_authenticated_session


BASE_URL = "https://guaraciama-mg-tst.vivver.com"


async def run():

    session = await get_authenticated_session()

    client = VivverCatalogClient(BASE_URL, session)

    products = client.get_products()

    print("Produtos recebidos:", len(products))


if __name__ == "__main__":
    asyncio.run(run())