class PrincipleLookup:

    def __init__(self, repository):

        self.repo = repository


    def by_code(self, codigo):

        return self.repo.principles.get(str(codigo))


    def by_name(self, nome):

        for principle in self.repo.principles.values():

            if principle["descricao"] == nome:
                return principle

        return None
