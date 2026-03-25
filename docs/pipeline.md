# Pipeline de processamento

## Pipeline de cadastro de produto

```
fonte (XML / planilha)
        ↓
parser
        ↓
text_normalizer
        ↓
product_matcher
        ↓
verificação no catálogo
        ↓
criar princípio ativo (se necessário)
        ↓
criar produto
        ↓
vincular princípio ativo
```

---

## Pipeline de sincronização de catálogo

```
login vivver
        ↓
download endpoints
        ↓
catalog_sync
        ↓
catalog_repository
        ↓
catalog_index
```
