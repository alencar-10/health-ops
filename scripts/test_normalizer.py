from app.normalization.text_normalizer import TextNormalizer


text = "Dipirona Sódica 500mg comprimido"

normalized = TextNormalizer.normalize(text)

print(normalized)