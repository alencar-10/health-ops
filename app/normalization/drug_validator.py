import re

PATTERN = r".+\s\d+\s(MG|G|ML)\s.+"

def is_valid_drug_name(name):

    return bool(re.match(PATTERN, name))
