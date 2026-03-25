from playwright.sync_api import sync_playwright
import pandas as pd
import time

class DiscriminadorPlaywrightService:

    def processar_planilha(self, arquivo_excel):

        df = pd.read_excel(arquivo_excel)

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=False)

            page = browser.new_page()

            page.goto("https://guaraciama-mg-tst.vivver.com/desktop")

            input("Faça login manual e pressione ENTER...")

            page.goto("URL_DA_TELA_DISCRIMINADOR")

            for _, row in df.iterrows():

                self.criar_discriminador(page, row)

            browser.close()


    def criar_discriminador(self, page, row):

        page.click("button:has-text('Novo')")

        page.fill("input[name='codigo']", str(row["CODIGO"]))

        page.fill("input[name='descricao']", row["DESCRICAO"])

        page.click("button:has-text('Salvar')")

        time.sleep(1)