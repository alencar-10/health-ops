import asyncio

from app.adapters.vivver.http.catalog import VivverCatalogClient
from app.adapters.vivver.http.auth import get_authenticated_session

from app.catalog.catalog_repository import CatalogRepository
from app.catalog.catalog_sync import CatalogSync
from app.catalog.catalog_index import CatalogIndex

from app.matching.product_matcher import ProductMatcher

from app.config.settings import BASE_URL


async def run():

    session = await get_authenticated_session()

    client = VivverCatalogClient(BASE_URL, session)

    repo = CatalogRepository()

    sync = CatalogSync(client, repo)
    sync.run()

    # construir índice
    index = CatalogIndex(repo)
    index.build()

    # criar matcher
    matcher = ProductMatcher(repo, index)

    product = "DIPIRONA SODICA 500 MG COMPRIMIDO"

    match = matcher.find_exact(product)

    if match:
        print("Match exato encontrado:", match.description)
    else:
        print("Match exato não encontrado")

    similar, score = matcher.find_similar(product)

    if similar:
        print("Match aproximado:", similar.description, "score:", score)


if __name__ == "__main__":
    asyncio.run(run())
