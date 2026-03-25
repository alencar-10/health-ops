from app.domain.product import Product


class VivverProductMapper:

    @staticmethod
    def from_json(row):

        product_id = row.get("DT_RowId")

        code = row.get("0")
        description = row.get("1")

        active = True

        return Product(
            id=product_id,
            code=code,
            description=description,
            active=active
        )