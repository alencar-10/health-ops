# HEALTH-OPS — Pipeline de processamento

## Pipeline principal — cadastro de medicamento

```
texto bruto
"DIPIRONA 500MG COMP"
        ↓
TextNormalizer
"DIPIRONA 500MG COMP" → "DIPIRONA 500MG COMP" (uppercase, sem acentos)
        ↓
PrincipleExtractor
→ principle: "DIPIRONA SODICA"
        ↓
StrengthParser
→ strength: 500, unit: "MG"
        ↓
DrugMapper
→ form: "COMPRIMIDO"
        ↓
Drug object
{ principle, strength, unit, form, normalized }
        ↓
ProductMatcher
(busca no catálogo local em memória)
        ↓
DecisionEngine
        ↓
┌──────────────────────────────────────┐
│ EXISTS     │ REVIEW      │ CREATE    │
│ score=100  │ score<100   │ não achou │
│            │             │           │
│ ignora     │ revisão     │ fila de   │
│            │ manual      │ aprovação │
└──────────────────────────────────────┘
        ↓ (CREATE aprovado)
ProductCreator
        ↓
┌─────────────────────────────┐
│ 1. gera código único        │
│ 2. resolve CODFORMA         │
│ 3. cria princípio ativo     │
│ 4. sync catálogo (princípio)│
│ 5. cria produto             │
│ 6. extrai ID do HTML        │
│ 7. sync catálogo (produto)  │
│ 8. vincula princípio        │
└─────────────────────────────┘
        ↓
Vivver ERP
✅ princípio + produto + vínculo
```

---

## Pipeline de sincronização de catálogo

Executado no startup e antes de cada operação de criação.

```
get_authenticated_session()
        ↓
VivverCatalogClient
        ↓
┌─────────────────────────────────┐
│ GET /amx/produto.json           │
│ GET /amx/principio_ativo.json   │
│ GET /amx/unidade_medida.json    │
│ GET /amx/forma_farmaceutica.json│
│ GET /amx/unidade_produto.json   │
└─────────────────────────────────┘
        ↓
CatalogSync.run()
        ↓
CatalogRepository (memória)
{ products, principles, units, forms, product_units }
        ↓
CatalogIndex / CatalogPharmaIndex / CatalogPrincipleIndex
(índices para busca eficiente)
```

---

## Pipeline de aprovação via API

```
POST /approve/{item_id}
        ↓
ReviewQueue.load()
        ↓
Drug object reconstruído
        ↓
ProductCreator.create(drug)
        ↓
┌─────────────────────────────┐
│ princípio ativo criado      │
│ produto criado              │
│ vínculo realizado           │
└─────────────────────────────┘
        ↓
ReviewQueue.approve(item_id)
        ↓
{ status: "approved", product: ... }
```

---

## Extração de ID do produto

O Vivver retorna status 200 com HTML após criação. O ID é extraído do HTML:

```
POST /amx/produto
        ↓
response HTML
        ↓
BeautifulSoup
→ <input name="amx_produto[id]" value="14253">
        ↓
produto_id = "14253"
```

Fallback: se não encontrado no HTML, captura via sync do catálogo.

---

## Detecção de forma farmacêutica

```
texto: "DIPIRONA 500MG COMPRIMIDO"
        ↓
DrugMapper.detect_form()
        ↓
1. busca alias: COMP → COMPRIMIDO
2. busca no catálogo local por nome exato
        ↓
form: "COMPRIMIDO"
        ↓
CatalogRepository.get_form_code("COMPRIMIDO")
        ↓
CODFORMA: "6"
```
