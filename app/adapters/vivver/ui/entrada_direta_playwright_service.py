import pandas as pd
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.franciscosa-mg.vivver.com"
LOGIN_URL = f"{BASE_URL}/desktop"

USUARIO = "35304775830"
SENHA = "kloq230"


class EntradaDiretaPlaywrightService:

    def processar_planilha(self, arquivo_excel):

        print("ARQUIVO CARREGADO:", __file__)

        df = pd.read_excel(arquivo_excel)
        print("Colunas encontradas:", list(df.columns))

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                geolocation={"latitude": 0, "longitude": 0},
                permissions=[]
            )
            page = context.new_page()

            # ================= LOGIN =================

            page.goto(LOGIN_URL)

            page.wait_for_selector(
                "input[placeholder='Insira sua Conta']",
                timeout=15000
            )

            page.fill("input[placeholder='Insira sua Conta']", USUARIO)
            page.fill("input[placeholder='Senha']", SENHA)

            page.locator("div.btn_entrar").click()

            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(3000)

            print("[LOGIN] OK")

            # ================= ABRIR TELA =================

            page.goto(BASE_URL + "/amx/entrada_direta_produto")

            page.wait_for_selector(
                "#amx_entrada_direta_produto_insert",
                timeout=20000
            )

            print("[TELA] OK")

            # ================= CLICAR NOVO (+) =================

            page.locator("#amx_entrada_direta_produto_insert").click()
            page.wait_for_timeout(1500)

            print("[NOVO] OK")

            # ================= MOTIVO DE ENTRADA =================

            print("\n=== FRAMES ATUAIS ===")
            for f in page.frames:
                print("FRAME:", f.name, " | URL:", f.url)
            print("=====================\n")

            print("[MOTIVO] Setando via JS...")

            page.evaluate("""
            () => {
                const input = document.querySelector('#amx_entrada_direta_produto_codmotivoentr');
                input.value = '9';
                input.dispatchEvent(new Event('change', { bubbles: true }));
                input.dispatchEvent(new Event('blur', { bubbles: true }));
            }
            """)

            print("[MOTIVO] OK")

            # ================= INSERIR ITENS =================

            for index, row in df.iterrows():

                print(f"Incluindo item {index + 1}")

                # ================= PRODUTO =================

                print("[PRODUTO] Inserindo código direto...")

                page.evaluate("""
                (codigo) => {
                    const input = document.querySelector('#amx_entrada_direta_produto_codproduto');
                    input.value = codigo;
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    input.dispatchEvent(new Event('blur', { bubbles: true }));
                }
                """, str(row["COD_PRODUTO"]))

                page.keyboard.press("Tab")
                page.wait_for_timeout(1000)

                print("[PRODUTO] OK")

                # ================= FABRICANTE =================

                print("[FABRICANTE] Inserindo código direto...")

                page.evaluate("""
                (codigo) => {
                    const input = document.querySelector('#amx_entrada_direta_produto_codfabricante');
                    input.value = codigo;
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    input.dispatchEvent(new Event('blur', { bubbles: true }));
                }
                """, str(row["COD_FABRICANTE"]))

                page.keyboard.press("Tab")
                page.wait_for_timeout(1000)

                print("[FABRICANTE] OK")

                # ================= CAMPOS SIMPLES =================

                page.locator(
                    "#amx_entrada_direta_produto_numlote"
                ).fill(str(row["LOTE"]))

                page.locator(
                    "#amx_entrada_direta_produto_qdeentrada"
                ).fill(str(row["QUANTIDADE"]))

                page.locator(
                    "#amx_entrada_direta_produto_prcunitario"
                ).fill(str(row["PRECO_UNITARIO"]))

                # ================= VALIDADE =================

                data = row["DT_VALIDADE"]

                if pd.isna(data):
                    data_validade = ""
                elif isinstance(data, datetime):
                    data_validade = data.strftime("%d/%m/%Y")
                else:
                    try:
                        data_validade = pd.to_datetime(data).strftime("%d/%m/%Y")
                    except:
                        data_validade = str(data)

                campo_validade = page.locator(
                    "#amx_entrada_direta_produto_datvalidade"
                )

                campo_validade.click()
                campo_validade.fill(data_validade)

                page.keyboard.press("Enter")

                page.wait_for_timeout(800)

                # ================= BOTÃO AZUL =================

                print("[ITEM] Clicando botão adicionar...")

                page.locator("a:has(i.fa-arrow-down)").click()

                page.wait_for_timeout(1500)

                print("✔ Item incluído")

            # ================= FINAL =================

            print("\nItens inseridos. Confira na tela antes de salvar.")

            input("Pressione ENTER quando terminar a conferência...")

            print("Encerrando automação.")

            browser.close()