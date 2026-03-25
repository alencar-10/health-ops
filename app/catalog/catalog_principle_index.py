import re
from collections import defaultdict

from app.normalization.principle_extractor import PrincipleExtractor


class CatalogPrincipleIndex:

    def __init__(self, repo):

        self.repo = repo
        self.index = defaultdict(list)
        self.extractor = PrincipleExtractor()

    def build(self):

        # garante que o índice comece vazio
        self.index.clear()

        # repo.products pode ser lista ou dict
        if isinstance(self.repo.products, dict):
            products = self.repo.products.values()
        else:
            products = self.repo.products

        for product in products:

            name = self._get_product_name(product)

            if not name:
                continue

            principle = self.extractor.extract(name)

            if principle:
                self.index[principle].append(product)

    def search(self, principle):

        if not principle:
            return []

        principle = principle.upper().strip()

        return self.index.get(principle, [])

    def _get_product_name(self, product):

        """
        Obtém o nome do produto independentemente
        se ele for dict ou objeto Product.
        """

        # caso seja dict
        if isinstance(product, dict):

            # alguns catálogos usam campo "1" para descrição
            if "1" in product:
                return product.get("1")

            return product.get("name") or product.get("descricao")

        # caso seja objeto
        if hasattr(product, "name"):
            return product.name

        if hasattr(product, "descricao"):
            return product.descricao

        if hasattr(product, "description"):
            return product.description

        return ""