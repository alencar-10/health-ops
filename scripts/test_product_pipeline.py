import asyncio

from app.adapters.vivver.http.catalog import VivverCatalogClient
from app.adapters.vivver.http.auth import get_authenticated_session

from app.catalog.catalog_repository import CatalogRepository
from app.catalog.catalog_sync import CatalogSync
from app.catalog.catalog_index import CatalogIndex
from app.catalog.catalog_principle_index import CatalogPrincipleIndex
from app.catalog.catalog_pharma_index import CatalogPharmaIndex

from app.matching.product_matcher import ProductMatcher
from app.pipelines.product_pipeline import ProductPipeline

from app.adapters.vivver.http.product_client import VivverProductClient
from app.adapters.vivver.http.product_link_client import VivverProductLinkClient

from app.services.product_service import ProductService
from app.services.product_decision_engine import ProductDecisionEngine

from app.normalization.drug_mapper import DrugMapper
from app.normalization.strength_parser import StrengthParser
from app.normalization.principle_extractor import PrincipleExtractor


from app.config.settings import BASE_URL


async def run():

    # =============================
    # AUTH
    # =============================

    session = await get_authenticated_session()

    # =============================
    # CATÁLOGO
    # =============================

    client = VivverCatalogClient(BASE_URL, session)

    repo = CatalogRepository()

    sync = CatalogSync(client, repo)
    sync.run()

    # =============================
    # ÍNDICES
    # =============================

    pharma_index = CatalogPharmaIndex(repo)
    pharma_index.build()

    principle_index = CatalogPrincipleIndex(repo)
    principle_index.build()

    print("\n===== TESTE PRINCIPLE INDEX =====")

    results = principle_index.search("DIPIRONA SODICA")

    print("Produtos encontrados:", len(results))

    # =============================
    # TESTE DRUG MAPPER
    # =============================

    mapper = DrugMapper(repo)

    print("\n===== TESTE DRUG MAPPER =====")

    mapper_tests = [
        "DIPIRONA 500MG COMP",
        "AMOXICILINA 500MG CAPS",
        "CEFTRIAXONA 1G AMP",
        "PARACETAMOL 200MG/ML SOL",
        "DEXCLORFENIRAMINA XAROPE"
    ]

    for t in mapper_tests:
        result = mapper.detect_form(t)
        print(t, "→", result)

    # =============================
    # TESTE STRENGTH PARSER
    # =============================

    parser = StrengthParser()

    print("\n===== TESTE STRENGTH PARSER =====")

    strength_tests = [
        "DIPIRONA 500MG COMP",
        "PARACETAMOL 200MG/ML",
        "AMOXICILINA + CLAVULANATO 500+125 MG"
    ]

    for t in strength_tests:
        result = parser.parse(t)
        print(t, "→", result)

    # =============================
    # TESTE PRINCIPLE EXTRACTOR
    # =============================

    extractor = PrincipleExtractor()

    print("\n===== TESTE PRINCIPLE EXTRACTOR =====")

    result = extractor.extract(
        "DIPIRONA SODICA 500 MG COMPRIMIDO"
    )

    print(result)

    # =============================
    # ÍNDICE DE PRODUTOS
    # =============================

    index = CatalogIndex(repo)
    index.build()

    pharma_index = CatalogPharmaIndex(repo)
    pharma_index.build()

    # =============================
    # MATCHER
    # =============================

    matcher = ProductMatcher(pharma_index)

    # =============================
    # CLIENTES ERP
    # =============================

    vivver_client = VivverProductClient(session, BASE_URL)

    link_client = VivverProductLinkClient(session, BASE_URL)

    product_service = ProductService(
        vivver_client,
        link_client
    )

    # =============================
    # DECISION ENGINE
    # =============================

    decision_engine = ProductDecisionEngine()

    # =============================
    # PIPELINE
    # =============================

    pipeline = ProductPipeline(
        matcher,
        product_service,
        decision_engine,
        repo
    )

    # =============================
    # TESTE
    # =============================

    await pipeline.process(
        "DIPIRONA SODICA 123 MG COMPRIMIDO TESTE"
    )


if __name__ == "__main__":
    asyncio.run(run())