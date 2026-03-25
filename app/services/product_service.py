class ProductService:

    def __init__(self, client, link_client, dry_run=False):
        self.client = client
        self.link_client = link_client
        self.dry_run = dry_run

    def create(self, codigo, nome, catmat=""):

        if not str(codigo).isdigit():
            return "ERROR_VALIDACAO", codigo, None

        if not nome:
            return "ERROR_VALIDACAO", codigo, None

        codigo = str(int(codigo))

        payload = {
            "utf8": "✓",
            "workMode": "wmInsert",
            "oldWorkMode": "wmBrowse",

            "amx_produto[codproduto]": codigo,
            "amx_produto[nomproduto]": nome,
            "amx_produto[codcatmat]": catmat,

            "amx_produto[inddatvalidade]": "S",
            "amx_produto[indlote]": "S",

            "amx_produto[codunidadeproduto]": "1",
            "amx_produto[valunidadeproduto]": "1",
            "amx_produto[codunidademedida]": "1",

            "amx_produto[indcontrolesigaf]": "N",
            "amx_produto[indativo]": "S",
            "amx_produto[indpublicarproduto]": "S",
        }

        if self.dry_run:
            return "DRY_RUN", codigo, None

        response = self.client.post("/amx/produto", payload)

        if response.status_code != 200:
            response = self.client.post("/amx/produto", payload)

        if response.status_code != 200:
            return "ERROR_HTTP", codigo, None

        produto_id = self.client.extract_id(response)

        if produto_id:
            print(f"✅ PRODUTO CRIADO — ID: {produto_id}")
            return "CREATED", codigo, produto_id

        print("⚠️ PRODUTO CRIADO SEM ID — tentará capturar via sync")
        return "CREATED_NO_ID", codigo, None

    def link_principle(self, product_id, principle_id):
        return self.link_client.link_principle(product_id, principle_id)