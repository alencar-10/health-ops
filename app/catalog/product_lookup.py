class ProductLookup:

    def __init__(self, repository):

        self.repo = repository


    def by_code(self, codigo):

        return self.repo.products.get(str(codigo))
