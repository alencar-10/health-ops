import re


class StrengthParser:

    SIMPLE_PATTERN = r'(\d+)\s?(MG|G|ML)'
    COMBO_PATTERN = r'(\d+)\s?\+\s?(\d+)\s?(MG|G|ML)'

    def parse(self, text):

        text = text.upper()

        combo = re.search(self.COMBO_PATTERN, text)

        if combo:

            return {
                "strengths": [int(combo.group(1)), int(combo.group(2))],
                "unit": combo.group(3)
            }

        simple = re.search(self.SIMPLE_PATTERN, text)

        if simple:

            return {
                "strengths": [int(simple.group(1))],
                "unit": simple.group(2)
            }

        return None
