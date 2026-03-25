import unicodedata
import re


class TextNormalizer:

    @staticmethod
    def normalize(text: str) -> str:

        if not text:
            return ""

        # maiúsculo
        text = text.upper()

        # remover acentos
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ASCII", "ignore").decode("ASCII")

        # remover caracteres especiais
        text = re.sub(r"[^A-Z0-9\s]", " ", text)

        # remover espaços duplicados
        text = re.sub(r"\s+", " ", text).strip()

        return text