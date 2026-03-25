from app.domain.drug import Drug

from app.normalization.text_normalizer import TextNormalizer
from app.normalization.principle_extractor import PrincipleExtractor
from app.normalization.strength_parser import StrengthParser
from app.normalization.drug_mapper import DrugMapper

from app.review.review_queue import ReviewQueue

review_queue = ReviewQueue()


class ProductPipeline:

    def __init__(self, matcher, product_service, decision_engine, repo):

        self.matcher = matcher
        self.product_service = product_service
        self.decision_engine = decision_engine

        # parsers
        self.principle_extractor = PrincipleExtractor()
        self.strength_parser = StrengthParser()
        self.form_mapper = DrugMapper(repo)

    async def process(self, raw_description):

        print("\n--- PIPELINE INICIADO ---")

        drug = Drug(raw_description)

        # normalização
        drug.normalized = TextNormalizer.normalize(drug.raw)

        print("Descrição normalizada:", drug.normalized)

        # princípio ativo
        principle = self.principle_extractor.extract(drug.normalized)

        if principle:
            drug.principles = [principle]

        # dose
        strength = self.strength_parser.parse(drug.normalized)

        if strength:
            drug.strengths = strength["strengths"]
            drug.unit = strength["unit"]

        # forma farmacêutica
        drug.form = self.form_mapper.detect_form(drug.normalized)

        # MATCH
        print("\nDrug gerado:")
        print("principle:", drug.primary_principle())
        print("strength:", drug.primary_strength())
        print("form:", drug.form)

        product, score = self.matcher.match(drug)

        # DECISÃO
        if not product:
            decision = "CREATE"
        elif score == 100:
            decision = "EXISTS"
        else:
            decision = "REVIEW"

        # EXISTS
        if decision == "EXISTS":

            print("Produto já existe:", product.description)
            print("DECISÃO: EXISTS")

            return {
                "status": "exists",
                "product": product
            }

        # REVIEW
        if decision == "REVIEW":

            print("Produto semelhante encontrado:", product.description)
            print("Score:", score)
            print("DECISÃO: REVIEW")

            return {
                "status": "review",
                "product": product,
                "score": score
            }

        # CREATE
        if decision == "CREATE":

            print("Produto não encontrado no catálogo")
            print("DECISÃO: CREATE")

            review_queue.add({
                "descricao_original": raw_description,
                "drug": {
                    "principle": drug.primary_principle(),
                    "strength": drug.primary_strength(),
                    "form": drug.form
                },
                "status": "PENDING"
            })

            print("Produto enviado para fila de revisão")

            return {
                "status": "queued_for_review",
                "description": drug.normalized
            }