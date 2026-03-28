# HEALTH-OPS — Diagrama do sistema

## Fluxo principal

```
┌──────────────────────────────┐
│        INPUT (texto)         │
│  "DIPIRONA 500MG COMP"       │
└──────────────┬───────────────┘
               │
               ▼
      ┌─────────────────┐
      │   DrugParser    │
      │  normalização   │
      │  farmacológica  │
      └────────┬────────┘
               │
               ▼
        ┌─────────────┐
        │    Drug     │
        │  { princ,  │
        │  strength, │
        │  form }    │
        └──────┬──────┘
               │
               ▼
      ┌──────────────────┐
      │  ProductMatcher  │
      │  catálogo local  │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │  DecisionEngine  │
      └────────┬─────────┘
               │
   ┌───────────┼───────────┐
   │           │           │
   ▼           ▼           ▼
EXISTS      REVIEW       CREATE
   │           │           │
ignora     revisão    ReviewQueue
           manual         │
                          ▼
                   ┌─────────────┐
                   │   FastAPI   │
                   │  /reviews   │
                   └──────┬──────┘
                          │
                   POST /approve
                          │
                          ▼
                 ┌────────────────┐
                 │ ProductCreator │
                 └───────┬────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
   cria princípio   cria produto   vincula
   ativo            (extrai ID     princípio
   (CODFORMA)       do HTML)       ao produto
          │              │              │
          └──────────────┴──────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Vivver ERP  │
                  │  ✅ criado   │
                  └──────────────┘
```

---

## Arquitetura de camadas

```
┌─────────────────────────────────────┐
│              API (FastAPI)          │
│         /reviews  /approve          │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│            Services                 │
│  ProductCreator  ProductService     │
│  PrincipleService                   │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│            Adapters                 │
│  VivverProductClient                │
│  VivverPrincipleClient              │
│  VivverProductLinkClient            │
│  VivverCatalogClient                │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│           Vivver ERP                │
│  HTTP /amx/*   +   Playwright UI    │
└─────────────────────────────────────┘
```

---

## Sincronização de catálogo

```
┌─────────────────┐
│   Vivver API    │
│  /amx/*.json    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CatalogSync    │
│  paginação      │
│  automática     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│     CatalogRepository       │
│  products    principles     │
│  units       forms          │
│  product_units              │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  CatalogIndex               │
│  CatalogPharmaIndex         │
│  CatalogPrincipleIndex      │
│  (busca eficiente O(1))     │
└─────────────────────────────┘
```

---

## Autenticação

```
┌──────────────┐
│  Playwright  │
│  login único │
└──────┬───────┘
       │ cookies
       ▼
┌──────────────────────┐
│  .vivver_cookies.json│
│  (cache em disco)    │
└──────┬───────────────┘
       │ reutiliza
       ▼
┌──────────────────────┐
│  requests.Session    │
│  todas as requisições│
└──────────────────────┘
```
