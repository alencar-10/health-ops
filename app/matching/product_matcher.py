from rapidfuzz import fuzz


class ProductMatcher:

    def __init__(self, pharma_index):

        self.index = pharma_index

    def match(self, drug):

        principle = drug.primary_principle()
        strength = drug.primary_strength()
        form = drug.form

        candidates = self.index.search(
            principle,
            strength,
            form
        )

        if not candidates:
            return None, 0

        if len(candidates) == 1:
            return candidates[0], 100

        # fallback fuzzy
        best = None
        best_score = 0

        for product in candidates:

            name = product.description

            score = fuzz.ratio(
                drug.normalized,
                name
            )

            if score > best_score:

                best_score = score
                best = product

        return best, best_score