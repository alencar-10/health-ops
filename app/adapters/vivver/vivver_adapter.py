from app.ports.erp_port import ERPPort


class VivverAdapter(ERPPort):

    def __init__(self,
                 principle_service,
                 product_service,
                 principle_lookup,
                 product_lookup):

        self.principle_service = principle_service
        self.product_service = product_service
        self.principle_lookup = principle_lookup
        self.product_lookup = product_lookup


    def create_principle(self, codigo, nome, codforma):

        return self.principle_service.create(
            codigo,
            nome,
            codforma
        )


    def create_product(self, codigo, nome):

        return self.product_service.create(
            codigo,
            nome
        )


    def link_principle(self, product_id, principle_id):

        return self.product_service.link_principle(
            product_id,
            principle_id
        )


    def get_product_by_code(self, codigo):

        return self.product_lookup.by_code(codigo)


    def get_principle_by_code(self, codigo):

        return self.principle_lookup.by_code(codigo)
