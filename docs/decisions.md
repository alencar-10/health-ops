# Architecture Decisions

## ADR-001 — Catálogo em memória

Decisão:

O catálogo do ERP será carregado em memória durante a execução do sistema.

Motivação:

* catálogo pequeno
* consultas muito mais rápidas
* reduzir chamadas ao ERP

Plano futuro:

Migrar para SQLite quando o sistema se tornar multi-tenant.

---

## ADR-002 — Matching baseado em texto

Decisão:

Matching inicial baseado em normalização de texto + fuzzy matching.

Biblioteca escolhida:

RapidFuzz

Motivação:

* alta performance
* precisão em comparação textual

---

## ADR-003 — Código compartilhado produto/princípio ativo

Decisão:

Produto e princípio ativo utilizarão o mesmo código.

Motivação:

Compatibilidade com padrão utilizado no Vivver.

---

## ADR-004 — Integração híbrida

Decisão:

Utilizar dois mecanismos de integração:

* HTTP API
* UI automation

Motivação:

Algumas operações não possuem endpoint disponível.
