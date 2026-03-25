class Product:

    def __init__(
        self,
        code: str,
        description: str,
        active: bool = True,
        id: int | None = None
    ):

        self.id = id
        self.code = code
        self.description = description
        self.active = active

    def __repr__(self):

        return f"<Product id={self.id} code={self.code} {self.description}>"