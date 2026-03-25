# HEALTH-OPS — Roadmap de desenvolvimento

## Fase 1 — Exploração técnica (concluída)

Objetivo: entender o ERP Vivver.

Concluído:

* descoberta do ERP
* engenharia reversa de endpoints
* análise de autenticação
* análise de paginação da API
* entendimento do modelo de produtos
* entendimento de princípios ativos

---

## Fase 2 — Foundation Building (em andamento)

Objetivo: construir base do sistema.

### Concluído

* estrutura inicial do projeto
* cliente HTTP Vivver
* autenticação
* sessão autenticada
* paginação automática da API
* download completo do catálogo
* catalog_repository em memória
* catalog_sync
* text_normalizer
* product_matcher inicial
* sincronização de 13k produtos

---

### Em desenvolvimento

* catalog_index (índice de busca)
* product_pipeline
* normalização farmacêutica
* modelagem de domínio (Product)

---

## Fase 3 — Automação de catálogo

Planejado:

* criação automática de princípio ativo
* criação automática de produto
* vinculação produto ↔ princípio ativo
* prevenção de duplicidade

---

## Fase 4 — Automação de nota fiscal

Planejado:

* parser XML NFe
* matching de produtos
* criação automática de produtos faltantes
* automação de entrada de nota

---

## Fase 5 — Plataforma SaaS

Planejado:

* suporte multi-tenant
* armazenamento em banco de dados
* interface administrativa
* monitoramento de automações
* logs centralizados

---

# Métricas atuais do sistema

Catálogo carregado:

* Produtos: 13.671
* Princípios ativos: 2.672
* Unidades: 80
* Formas farmacêuticas: 84
* Unidades produto: 35

---

# Visão de longo prazo

Transformar o HEALTH-OPS em uma plataforma de automação para ERPs públicos.

Inicialmente focado no Vivver, mas com arquitetura extensível para outros sistemas.
