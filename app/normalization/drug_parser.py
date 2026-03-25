from app.domain.drug import Drug

from app.normalization.text_normalizer import TextNormalizer
from app.normalization.strength_parser import StrengthParser
from app.normalization.drug_mapper import DrugMapper
from app.normalization.principle_extractor import PrincipleExtractor


class DrugParser:

    def __init__(self, repo):

        self.strength_parser = StrengthParser()
        self.drug_mapper = DrugMapper(repo)
        self.principle_extractor = PrincipleExtractor()

    def parse(self, text):

        normalized = TextNormalizer.normalize(text)

        drug = Drug(text)

        drug.normalized = normalized

        # principle
        principle = self.principle_extractor.extract(normalized)

        if principle:
            drug.principles = [principle]

        # strength
        strength_data = self.strength_parser.parse(normalized)

        if strength_data:

            drug.strengths = strength_data["strengths"]
            drug.unit = strength_data["unit"]

        # form
        form_data = self.drug_mapper.detect_form(normalized)

        if form_data:

            drug.form = form_data

        return drug