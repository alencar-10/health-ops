class CatalogSync:

    def __init__(self, client, repository):

        self.client = client
        self.repo = repository

    def run(self):

        print("Sincronizando catálogo...")

        products = self.client.get_products()
        principles = self.client.get_principles()
        units = self.client.get_units()
        forms = self.client.get_forms()
        product_units = self.client.get_product_units()

        self.repo.clear()

        self.repo.save_products(products)
        self.repo.save_principles(principles)
        self.repo.save_units(units)
        self.repo.save_forms(forms)
        self.repo.save_product_units(product_units)

        print("Catálogo sincronizado.")