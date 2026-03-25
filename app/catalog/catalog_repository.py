from app.adapters.vivver.http.product_mapper import VivverProductMapper

class CatalogRepository:

    def __init__(self):
        self.products = {}
        self.principles = {}
        self.units = {}
        self.forms = {}
        self.product_units = {}

    def clear(self):
        self.products.clear()
        self.principles.clear()
        self.units.clear()
        self.forms.clear()
        self.product_units.clear()

    def save_products(self, products):
        for row in products:
            product = VivverProductMapper.from_json(row)
            self.products[product.code] = product

    def save_principles(self, principles):
        for p in principles:
            code = p.get("0") or p.get("codigo")
            if code is not None:
                self.principles[str(code)] = p

    def save_units(self, units):
        for u in units:
            code = u.get("1") or u.get("codigo")
            if code is not None:
                self.units[str(code)] = u

    def save_forms(self, forms):
        for f in forms:
            code = f.get("1")
            if code is not None:
                self.forms[str(code)] = f
                print("FORMA DO VIVVER:", f)

    def save_product_units(self, product_units):
        for u in product_units:
            code = u.get("1") or u.get("codigo")
            if code is not None:
                self.product_units[str(code)] = u

    def get_form_code(self, form_name):

        if not form_name:
            return None

        form_name = str(form_name).strip().upper()

        for code, form in self.forms.items():
            name = form.get("2")
            if not name:
                continue
            if str(name).strip().upper() == form_name:
                return code

        return None

        form_name = str(form_name).strip().upper()

        for code, form in self.forms.items():

            name = (
                form.get("1")
                or form.get("nome")
                or form.get("descricao")
            )

            if not name:
                continue

            name = str(name).strip().upper()

            if name == form_name:
                return code

        return None