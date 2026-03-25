class ProductDecisionEngine:

    def decide(self, exact, similar, score):

        if exact:

            return {
                "action": "exists",
                "product": exact
            }

        if similar:

            if score >= 95:

                return {
                    "action": "exists",
                    "product": similar
                }

            if score >= 80:

                return {
                    "action": "review",
                    "product": similar,
                    "score": score
                }

        return {
            "action": "create"
        }
