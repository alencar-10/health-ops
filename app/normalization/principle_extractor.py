import re


class PrincipleExtractor:

    def extract(self, text):

        text = text.upper()

        # remove doses
        text = re.sub(r'\d+\s?(MG|G|ML)', '', text)

        # remove formas farmacêuticas
        text = re.sub(
            r'COMPRIMIDO|COMP|COMPR|CAPSULA|CAPS|CAP|AMPOLA|AMP|SOLUCAO|SOL|XAROPE',
            '',
            text
        )

        # remove separadores de combinação
        text = text.replace('+', ' ')

        # remove espaços duplicados
        text = re.sub(r'\s+', ' ', text)

        return text.strip()