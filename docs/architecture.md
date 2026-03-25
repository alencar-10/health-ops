# HEALTH-OPS — Arquitetura do Sistema

## Visão geral

HEALTH-OPS é uma plataforma de automação para o ERP Vivver usada por prefeituras.
O sistema automatiza operações administrativas como:

* cadastro de produtos
* cadastro de princípios ativos
* organização de catálogo
* preparação para entrada de nota fiscal
* automação de rotinas operacionais

Inicialmente o foco é o módulo de **farmácia**, mas a arquitetura foi projetada para suportar **outros módulos do ERP**.

---

# Arquitetura geral

O sistema segue princípios de:

* Clean Architecture
* Ports and Adapters (Hexagonal)
* Pipeline Processing

Fluxo geral:

```
Fonte de dados
(XML / planilha / integração)

        ↓

Parser de fonte

        ↓

Normalização de dados

        ↓

Matching com catálogo existente

        ↓

Decisão de criação ou atualização

        ↓

Integração com Vivver (HTTP / UI)
```

---

# Estrutura do projeto

```
C:.
│   .gitignore
│
├───api
│       server.py
│
├───app
│   ├───adapters
│   │   │   registry.py
│   │   │   __init__.py
│   │   │
│   │   ├───base
│   │   │       system_client.py
│   │   │       __init__.py
│   │   │
│   │   ├───sigaf
│   │   │   │   __init__.py
│   │   │   │
│   │   │   └───http
│   │   │           __init__.py
│   │   │
│   │   ├───vivver
│   │   │   │   vivver_adapter.py
│   │   │   │   __init__.py
│   │   │   │
│   │   │   ├───http
│   │   │   │   │   auth.py
│   │   │   │   │   bulk_engine.py
│   │   │   │   │   catalog.py
│   │   │   │   │   client(other_project).py
│   │   │   │   │   client.py
│   │   │   │   │   endpoint_scanner.py
│   │   │   │   │   entrada_api.py
│   │   │   │   │   module_engine.py
│   │   │   │   │   principle_client.py
│   │   │   │   │   products.py
│   │   │   │   │   product_client.py
│   │   │   │   │   product_link_client.py
│   │   │   │   │   product_mapper.py
│   │   │   │   │   produto_api.py
│   │   │   │   │   session.py
│   │   │   │   │   __init__.py
│   │   │   │   │
│   │   │   │   └───__pycache__
│   │   │   │           auth.cpython-313.pyc
│   │   │   │           catalog.cpython-313.pyc
│   │   │   │           principle_client.cpython-313.pyc
│   │   │   │           product_client.cpython-313.pyc
│   │   │   │           product_mapper.cpython-313.pyc
│   │   │   │           session.cpython-313.pyc
│   │   │   │           __init__.cpython-313.pyc
│   │   │   │
│   │   │   ├───ui
│   │   │   │       browser.py
│   │   │   │       discriminador_playwright_service.py
│   │   │   │       entrada_direta_playwright_service.py
│   │   │   │       entrada_direta_ui.py
│   │   │   │       playwright_driver.py
│   │   │   │       product_ui.py
│   │   │   │       __init__.py
│   │   │   │
│   │   │   └───__pycache__
│   │   │           __init__.cpython-313.pyc
│   │   │
│   │   └───__pycache__
│   │           __init__.cpython-313.pyc
│   │
│   ├───api
│   │   │   server.py
│   │   │
│   │   └───__pycache__
│   │           server.cpython-313.pyc
│   │
│   ├───automation
│   ├───builders
│   │       principle_payload_builder.py
│   │
│   ├───catalog
│   │   │   catalog_index.py
│   │   │   catalog_pharma_index.py
│   │   │   catalog_principle_index.py
│   │   │   catalog_repository.py
│   │   │   catalog_sync.py
│   │   │   principle_lookup.py
│   │   │   product_lookup.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           catalog_index.cpython-313.pyc
│   │           catalog_pharma_index.cpython-313.pyc
│   │           catalog_principle_index.cpython-313.pyc
│   │           catalog_repository.cpython-313.pyc
│   │           catalog_sync.cpython-313.pyc
│   │           principle_lookup.cpython-313.pyc
│   │           product_lookup.cpython-313.pyc
│   │           __init__.cpython-313.pyc
│   │
│   ├───config
│   ├───core
│   ├───domain
│   │   │   drug.py
│   │   │   product.py
│   │   │
│   │   └───__pycache__
│   │           drug.cpython-313.pyc
│   │           product.cpython-313.pyc
│   │
│   ├───infra
│   ├───matching
│   │   │   product_matcher.py
│   │   │
│   │   └───__pycache__
│   │           product_matcher.cpython-313.pyc
│   │
│   ├───normalization
│   │   │   drug_mapper.py
│   │   │   drug_parser.py
│   │   │   drug_validator.py
│   │   │   principle_extractor.py
│   │   │   strength_parser.py
│   │   │   text_normalizer.py
│   │   │
│   │   └───__pycache__
│   │           drug_mapper.cpython-313.pyc
│   │           drug_parser.cpython-313.pyc
│   │           principle_extractor.cpython-313.pyc
│   │           strength_parser.cpython-313.pyc
│   │           text_normalizer.cpython-313.pyc
│   │
│   ├───pipelines
│   │   │   product_pipeline.py
│   │   │
│   │   └───__pycache__
│   │           product_pipeline.cpython-313.pyc
│   │
│   ├───ports
│   │       erp_port.py
│   │
│   ├───review
│   │   │   review_queue.py
│   │   │
│   │   └───__pycache__
│   │           review_queue.cpython-313.pyc
│   │
│   ├───services
│   │   │   principle_service.py
│   │   │   product_creator.py
│   │   │   product_decision_engine.py
│   │   │   product_service.py
│   │   │
│   │   └───__pycache__
│   │           principle_service.cpython-313.pyc
│   │           product_creator.cpython-313.pyc
│   │           product_decision_engine.cpython-313.pyc
│   │           product_service.cpython-313.pyc
│   │
│   ├───tenants
│   │       tenant_config.py
│   │
│   └───utils
│       │   code_generator.py
│       │
│       └───__pycache__
│               code_generator.cpython-313.pyc
│
├───data
│       review_queue.json
│
├───docs
│       architecture.md
│       decisions.md
│       endpoints.md
│       pipeline.md
│       README_DEV.md
│       roadmap.md
│
├───scripts
│   │   generate_endpoint_client.py
│   │   scan_vivver_endpoints.py
│   │   test_catalog_sync.py
│   │   test_normalizer.py
│   │   test_product_matcher.py
│   │   test_product_pipeline.py
│   │   test_vivver_catalog.py
│   │
│   └───__pycache__
│           test_catalog_sync.cpython-313.pyc
│           test_normalizer.cpython-313.pyc
│           test_product_matcher.cpython-313.pyc
│           test_product_pipeline.cpython-313.pyc
│           test_vivver_catalog.cpython-313.pyc
│
├───tests
├───tools
│   └───vivver_mapper
│           endpoint_discovery.py
│           form_parser.py
│           relation_mapper.py
│           schema_extractor.py
│
└───workers
PS C:\Users\alenc\OneDrive\Documentos\health-ops>
```

---

# Pipeline principal do sistema

Pipeline de cadastro de produto:

```
entrada de produto
        ↓
text_normalizer
        ↓
product_matcher
        ↓
verificar catálogo
        ↓
produto existe?
   ↓           ↓
sim           não
 ↓             ↓
ignorar    criar princípio ativo
             ↓
           criar produto
             ↓
           vincular princípio ativo
```

---

# Sincronização de catálogo

O sistema mantém um catálogo local em memória para evitar consultas repetidas ao ERP.

Fluxo:

```
Vivver API
   ↓
catalog_sync
   ↓
catalog_repository (memória)
   ↓
catalog_index
```

Dados sincronizados:

* produtos
* princípios ativos
* unidades
* formas farmacêuticas
* unidades de produto

---

# Estratégia de matching

Matching ocorre em duas etapas:

### 1 — normalização de texto

```
Dipirona Sódica 500mg comprimido
↓
DIPIRONA SODICA 500MG COMPRIMIDO
```

### 2 — fuzzy matching

Utiliza RapidFuzz para detectar similaridade entre descrições.

---

# Estratégia de geração de código

Produtos e princípios ativos compartilham o mesmo código.

Estratégia atual:

```
novo_codigo = max_codigo_existente + 1
```

Isso garante compatibilidade com o padrão do Vivver.

---

# Estratégia multi-tenant

Cada prefeitura será um tenant independente.

Configuração por tenant:

```
base_url
usuário
senha
configurações específicas
```

---

# Integração com Vivver

A integração ocorre por dois meios:

### HTTP

Endpoints `/amx/*.json`

Usado para:

* leitura de catálogo
* criação de entidades

### UI automation

Playwright

Usado quando não existe endpoint HTTP disponível.

---

# Próximos módulos planejados

* parser de XML de nota fiscal
* automação de entrada de nota
* expansão para outros módulos do ERP
* dashboard SaaS
* gestão multi-tenant completa
