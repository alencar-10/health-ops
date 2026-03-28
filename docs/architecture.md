# HEALTH-OPS — Arquitetura do Sistema

## Visão geral

HEALTH-OPS é uma plataforma de automação para o ERP Vivver usada por prefeituras.
O sistema automatiza operações administrativas como:

- cadastro de princípios ativos
- cadastro de produtos
- vínculo entre princípio ativo e produto
- organização e sincronização de catálogo
- preparação para automação de nota fiscal

O foco atual é o módulo de **farmácia**, mas a arquitetura foi projetada para suportar outros módulos do ERP e múltiplos tenants (prefeituras).

---

## Princípios arquiteturais

- **Clean Architecture** — separação entre domínio, serviços, adaptadores e infraestrutura
- **Ports and Adapters (Hexagonal)** — o domínio não conhece o ERP; adaptadores traduzem
- **Pipeline Processing** — dados fluem por etapas bem definidas até a execução no ERP

---

## Fluxo principal

```
Fonte de dados
(texto / XML / planilha)
        ↓
DrugParser
(normalização farmacêutica)
        ↓
Drug object
(princípio, dose, forma)
        ↓
ProductMatcher
(matching com catálogo local)
        ↓
DecisionEngine
(EXISTS / REVIEW / CREATE)
        ↓
ReviewQueue
(aprovação humana via API)
        ↓
ProductCreator
(cria princípio → produto → vínculo no ERP)
        ↓
Vivver ERP
```

---

## Estrutura de diretórios

```
app/
├── adapters/
│   └── vivver/
│       ├── http/
│       │   ├── auth.py               # autenticação via Playwright + cache de cookies
│       │   ├── catalog.py            # download do catálogo do ERP
│       │   ├── client.py             # cliente HTTP base
│       │   ├── principle_client.py   # criação de princípio ativo
│       │   ├── product_client.py     # criação de produto + extração de ID
│       │   ├── product_link_client.py# vínculo produto ↔ princípio
│       │   ├── product_mapper.py     # mapeamento JSON → objeto Product
│       │   └── session.py            # criação de sessão requests com cookies
│       ├── ui/
│       │   ├── discriminador_playwright_service.py
│       │   └── entrada_direta_playwright_service.py
│       └── vivver_adapter.py         # orquestra os serviços via ERPPort
├── api/
│   └── server.py                     # FastAPI: /reviews e /approve/{id}
├── bootstrap/
│   └── application.py                # composição de todos os objetos
├── builders/
│   └── principle_payload_builder.py  # monta payload do princípio ativo
├── catalog/
│   ├── catalog_repository.py         # armazenamento em memória
│   ├── catalog_sync.py               # sincronização com o ERP
│   ├── catalog_index.py              # índice de busca de produtos
│   ├── catalog_pharma_index.py       # índice farmacológico
│   ├── catalog_principle_index.py    # índice de princípios ativos
│   ├── principle_lookup.py           # busca de princípio por código
│   └── product_lookup.py             # busca de produto por código
├── config/
│   └── settings.py                   # leitura de variáveis do .env
├── domain/
│   ├── drug.py                       # objeto Drug (princípio, dose, forma)
│   └── product.py                    # objeto Product
├── matching/
│   └── product_matcher.py            # matching com catálogo local
├── normalization/
│   ├── drug_mapper.py                # detecta forma farmacêutica
│   ├── drug_parser.py                # parser principal
│   ├── principle_extractor.py        # extrai princípio ativo
│   ├── strength_parser.py            # extrai dose e unidade
│   └── text_normalizer.py            # normalização de texto
├── pipelines/
│   └── product_pipeline.py           # orquestra o fluxo completo
├── ports/
│   └── erp_port.py                   # interface abstrata do ERP
├── review/
│   └── review_queue.py               # fila de revisão humana
├── services/
│   ├── principle_service.py          # cria princípio ativo no ERP
│   ├── product_creator.py            # orquestra criação completa
│   ├── product_decision_engine.py    # decide EXISTS/REVIEW/CREATE
│   └── product_service.py            # cria produto e faz vínculo
├── tenants/
│   └── tenant_config.py              # configuração por tenant (futuro)
└── utils/
    └── code_generator.py             # geração de código único
data/
    review_queue.json                 # fila persistida em disco
docs/                                 # documentação do projeto
scripts/                              # scripts de teste e utilitários
```

---

## Autenticação

O sistema usa **Playwright apenas para login**. Após o login, os cookies são extraídos e uma `requests.Session` é criada para todas as requisições HTTP subsequentes.

Cookies são salvos em `.vivver_cookies.json` e reutilizados nas execuções seguintes. Se a sessão estiver expirada, o login é refeito automaticamente.

```
Playwright → login → cookies → requests.Session → HTTP
```

---

## Configuração

Todas as credenciais e URLs são lidas do arquivo `.env`:

```
VIVVER_BASE_URL=https://{tenant}.vivver.com
VIVVER_USERNAME=seu_usuario
VIVVER_PASSWORD=sua_senha
```

O `settings.py` expõe `BASE_URL`, `USERNAME` e `PASSWORD` para o restante do projeto.

---

## Integração com o Vivver

### HTTP (principal)

Endpoints `/amx/*` para leitura e escrita.

Resposta do Vivver usa campo `"dados"` (não `"data"` padrão DataTables).

### UI Automation (fallback)

Playwright para operações sem endpoint HTTP disponível.

---

## Regras de negócio do Vivver

1. Criar princípio ativo com `CODFORMA` obrigatório
2. Criar produto com mesmo código do princípio
3. Vincular produto ao princípio via PATCH — após vínculo, `CODFORMA` é herdado pelo produto

---

## Geração de código

Códigos gerados pelo sistema usam faixa reservada:

```
novo_codigo = max_codigo_existente + 1
```

Garante não conflitar com cadastros manuais.

---

## Estratégia multi-tenant (planejado)

Cada prefeitura será um tenant independente com:

- `base_url` própria
- credenciais próprias
- catálogo isolado
- cookie cache isolado
