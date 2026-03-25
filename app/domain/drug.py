class Drug:

    def __init__(self, raw_description):

        # descrição original
        self.raw = raw_description

        # texto normalizado
        self.normalized = None

        # princípios ativos
        self.principles = []

        # dosagens
        self.strengths = []

        # unidade farmacológica
        self.unit = None

        # forma farmacêutica
        self.form = None
        self.codforma = None

        # via (futuro)
        self.route = None

    # -------------------------
    # helpers farmacológicos
    # -------------------------

    def primary_principle(self):

        if not self.principles:
            return None

        return self.principles[0]

    def primary_strength(self):

        if not self.strengths:
            return None

        return self.strengths[0]

    # -------------------------
    # debug
    # -------------------------

    def __repr__(self):

        return (
            f"Drug("
            f"principles={self.principles}, "
            f"strengths={self.strengths}, "
            f"unit={self.unit}, "
            f"form={self.form}"
            f")"
        )