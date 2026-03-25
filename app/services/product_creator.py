import time


class ProductCreator:

    def __init__(self,
                 principle_service,
                 product_service,
                 principle_lookup,
                 product_lookup,
                 code_generator):

        self.principle_service = principle_service
        self.product_service = product_service
        self.principle_lookup = principle_lookup
        self.product_lookup = product_lookup
        self.code_generator = code_generator

    def create(self, drug):

        print("\n===== PRODUCT CREATOR =====")

        codigo = str(self.code_generator.next_code())  # força string desde o início
        print("Código gerado:", codigo)

        # ================= FORMA =================

        codforma = self.principle_lookup.repo.get_form_code(drug.form)

        print("FORMA:", drug.form)
        print("CODFORMA RESOLVIDO:", codforma)
        # deve imprimir FORMA: COMPRIMIDO / CODFORMA RESOLVIDO: 6

        # ================= CREATE PRINCIPLE =================

        print("\n===== CREATE PRINCIPLE =====")

        self.principle_service.create(codigo, drug.principle, codforma)

        # ================= SYNC PRINCIPLE =================

        principle_id = None

        for i in range(5):

            print(f"Tentativa {i+1}/5 (principle)")

            self.principle_lookup.repo.clear()

            from app.catalog.catalog_sync import CatalogSync
            from app.adapters.vivver.http.catalog import VivverCatalogClient

            catalog_client = VivverCatalogClient(
                self.principle_service.client.base_url,
                self.principle_service.client.session
            )

            sync = CatalogSync(catalog_client, self.principle_lookup.repo)
            sync.run()
                       
            # DEBUG TEMPORÁRIO
            print("CHAVES NO CATÁLOGO:", list(self.principle_lookup.repo.principles.keys())[:10])
            print("BUSCANDO POR:", codigo, type(codigo))
           
            principle = self.principle_lookup.by_code(codigo)

            if principle:
                principle_id = principle.get("DT_RowId")
                print(f"Princípio encontrado! ID: {principle_id}")
                break   

            time.sleep(1)

        if not principle_id:
            print("❌ Princípio não encontrado após sync — abortando")
            return None

        # ================= CREATE PRODUCT =================

        print("\n===== CREATE PRODUCT =====")

        status, _, produto_id = self.product_service.create(
            codigo,
            drug.normalized
        )

        print("STATUS CREATE PRODUCT:", status)

        # ================= SYNC PRODUCT =================

        product = None

        for i in range(5):

            print(f"Tentativa {i+1}/5 (product)")

            self.product_lookup.repo.clear()

            from app.catalog.catalog_sync import CatalogSync
            from app.adapters.vivver.http.catalog import VivverCatalogClient

            catalog_client = VivverCatalogClient(
                self.product_service.client.base_url,
                self.product_service.client.session
            )

            sync = CatalogSync(catalog_client, self.product_lookup.repo)
            sync.run()

            product = self.product_lookup.by_code(codigo)

            if product:
                # fallback: se HTTP não retornou ID, pega do catálogo
                if not produto_id and product.id:
                    produto_id = product.id
                    print(f"ID capturado via sync: {produto_id}")
                print("Produto encontrado!")
                break

            time.sleep(1)

        # ================= LINK PRINCIPLE =================

        if produto_id and principle_id:

            print(f"\n===== LINK PRINCIPLE =====")
            print(f"produto_id: {produto_id} | principle_id: {principle_id}")

            link_status = self.product_service.link_principle(
                produto_id,
                principle_id
            )

            print(f"STATUS VÍNCULO: {link_status}")

            if link_status == "OK":
                print("✅ PRODUTO CRIADO E VINCULADO")
            else:
                print("⚠️ PRODUTO CRIADO MAS VÍNCULO FALHOU")

        else:
            print(f"❌ Vínculo não executado — produto_id: {produto_id} | principle_id: {principle_id}")

        return product