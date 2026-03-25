from collections import defaultdict
from app.normalization.text_normalizer import TextNormalizer


class CatalogIndex:

    def __init__(self, repository):

        self.repo = repository
        self.index = defaultdict(list)

    def build(self):

        for product in self.repo.products.values():

            name = product.description


            normalized = TextNormalizer.normalize(name)

            tokens = normalized.split()

            if not tokens:
                continue

            key = tokens[0]  # primeira palavra

            self.index[key].append(product)

    def search(self, description):

        normalized = TextNormalizer.normalize(description)

        tokens = normalized.split()

        if not tokens:
            return []

        key = tokens[0]

        return self.index.get(key, [])