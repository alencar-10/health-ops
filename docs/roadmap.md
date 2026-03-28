# HEALTH-OPS — Roadmap de desenvolvimento

## Fase 1 — Exploração técnica ✅ concluída

Objetivo: entender o ERP Vivver.

- descoberta do ERP e engenharia reversa de endpoints
- análise de autenticação (Playwright + cookies)
- análise de paginação da API (`dados` vs `data`)
- entendimento do modelo de produtos e princípios ativos
- mapeamento de regras de negócio do Vivver

---

## Fase 2 — Foundation Building ✅ concluída

Objetivo: construir base do sistema.

- estrutura do projeto (Clean Architecture)
- autenticação via Playwright com cache de cookies
- sessão HTTP reutilizável
- paginação automática da API
- sincronização completa do catálogo (produtos, princípios, formas, unidades)
- `CatalogRepository` em memória
- `TextNormalizer`, `PrincipleExtractor`, `StrengthParser`, `DrugMapper`
- `ProductMatcher` com fuzzy matching
- `ProductPipeline` com `DecisionEngine`
- `ReviewQueue` com persistência em JSON
- API FastAPI com `/reviews` e `/approve/{id}`
- centralização de configuração no `.env`

---

## Fase 3 — Automação de catálogo ✅ concluída

Objetivo: criar produtos e princípios ativos automaticamente no Vivver.

- criação de princípio ativo via HTTP
- criação de produto via HTTP
- extração de ID do produto a partir do HTML de resposta
- vínculo produto ↔ princípio ativo via PATCH
- resolução correta de `CODFORMA` pelo catálogo local
- sync de catálogo após cada criação para validação
- fila de revisão humana antes de executar no ERP

---

## Fase 4 — Qualidade e escala (próxima)

Objetivo: tornar o sistema robusto para uso em produção.

- [ ] persistência do catálogo em SQLite (evitar sync completo a cada operação)
- [ ] suporte a grupo e subgrupo de produto
- [ ] via de administração automática no princípio ativo
- [ ] detecção de material vs medicamento
- [ ] entrada por planilha Excel
- [ ] entrada por XML NFe
- [ ] testes automatizados (pytest)
- [ ] logs estruturados

---

## Fase 5 — Multi-tenant

Objetivo: suportar múltiplas prefeituras.

- [ ] `tenant_config.py` com configuração por cliente
- [ ] cookie cache isolado por tenant
- [ ] catálogo isolado por tenant
- [ ] `.env` por ambiente ou parametrização via CLI

Tenants previstos:
- `guaraciama-mg-tst.vivver.com`
- `montesclaros-mg-tst.vivver.com`
- `francissosa-mg.vivver.com`

---

## Fase 6 — Plataforma SaaS

Objetivo: produto vendável para prefeituras.

- [ ] dashboard operacional
- [ ] aprovação em lote
- [ ] interface web para revisão de fila
- [ ] monitoramento de automações
- [ ] logs centralizados
- [ ] gestão de tenants
- [ ] banco de dados multi-tenant

---

## Métricas do catálogo (referência)

| Item | Quantidade |
|---|---|
| Produtos | ~13.671 |
| Princípios ativos | 2.698 |
| Unidades | 80 |
| Formas farmacêuticas | 84 |
| Unidades de produto | 35 |
