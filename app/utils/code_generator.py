class CodeGenerator:

    def __init__(self, repository, start=8000000):

        self.repo = repository
        self.start = start


    def next_code(self):

        max_code = self.start

        # verifica códigos de produtos
        for code in self.repo.products.keys():

            try:
                code_int = int(code)

                if code_int > max_code:
                    max_code = code_int

            except:
                continue

        # verifica códigos de princípios
        for code in self.repo.principles.keys():

            try:
                code_int = int(code)

                if code_int > max_code:
                    max_code = code_int

            except:
                continue

        return max_code + 1
