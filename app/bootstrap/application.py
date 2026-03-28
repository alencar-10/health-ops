from app.adapters.vivver.http.catalog import VivverCatalogClient
from app.adapters.vivver.http.auth import get_authenticated_session
from app.adapters.vivver.http.product_client import VivverProductClient
from app.adapters.vivver.http.product_link_client import VivverProductLinkClient
from app.adapters.vivver.http.principle_client import VivverPrincipleClient

from app.catalog.catalog_repository import CatalogRepository
from app.catalog.catalog_sync import CatalogSync

from app.catalog.principle_lookup import PrincipleLookup
from app.catalog.product_lookup import ProductLookup

from app.services.principle_service import PrincipleService
from app.services.product_service import ProductService
from app.services.product_creator import ProductCreator

from app.builders.principle_payload_builder import PrinciplePayloadBuilder
from app.utils.code_generator import CodeGenerator

from app.config.settings import BASE_URL  # ← único import necessário


async def create_application():

    session = await get_authenticated_session()

    catalog_client = VivverCatalogClient(BASE_URL, session)

    repo = CatalogRepository()

    sync = CatalogSync(catalog_client, repo)
    sync.run()

    principle_lookup = PrincipleLookup(repo)
    product_lookup = ProductLookup(repo)

    product_client = VivverProductClient(session, BASE_URL)
    principle_client = VivverPrincipleClient(BASE_URL, session)
    link_client = VivverProductLinkClient(session, BASE_URL)

    payload_builder = PrinciplePayloadBuilder()

    principle_service = PrincipleService(
        principle_client,
        payload_builder
    )

    product_service = ProductService(
        product_client,
        link_client
    )

    code_generator = CodeGenerator(repo)

    creator = ProductCreator(
        principle_service,
        product_service,
        principle_lookup,
        product_lookup,
        code_generator
    )

    return creator