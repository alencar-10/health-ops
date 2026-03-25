from collections import defaultdict

from app.normalization.drug_parser import DrugParser


class CatalogPharmaIndex:

    def __init__(self, repo):

        self.repo = repo

        self.index = defaultdict(list)

        # usa o parser central
        self.parser = DrugParser(repo)

    def build(self):

        self.index.clear()

        # suporta repo.products como lista ou dict
        if isinstance(self.repo.products, dict):
            products = self.repo.products.values()
        else:
            products = self.repo.products

        for product in products:

            name = self._get_product_name(product)

            if not name:
                continue

            drug = self.parser.parse(name)

            principle = drug.primary_principle()

            # ignorar produtos sem dose farmacológica
            strength = drug.primary_strength()

            if not principle or not strength:
                continue

            form = drug.form

            key = (principle, strength, form)

            self.index[key].append(product)

    def search(self, principle=None, strength=None, form=None):

        key = (principle, strength, form)

        return self.index.get(key, [])

    def _get_product_name(self, product):

        # caso seja dict
        if isinstance(product, dict):

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