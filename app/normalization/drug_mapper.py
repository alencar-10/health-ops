class DrugMapper:

    def __init__(self, repo):
        self.repo = repo

        # mapa simples de abreviações
        self.alias = {
            "COMP": "COMPRIMIDO",
            "COMPR": "COMPRIMIDO",
            "CAPS": "CAPSULA",
            "CAP": "CAPSULA",
            "AMP": "AMPOLA",
            "SOL": "SOLUCAO",
            "INJ": "INJETAVEL",
            "XAROPE": "XAROPE"
        }

    def detect_form(self, text: str):

        text = text.upper()

        # procura alias primeiro
        for key, value in self.alias.items():
            if key in text:
                return value

        # procura diretamente no catálogo
        for code, form in self.repo.forms.items():

            if isinstance(form, dict):
                name = form.get("descricao", "")
            else:
                name = str(form)

            if name.upper() in text:
                return name

        return None