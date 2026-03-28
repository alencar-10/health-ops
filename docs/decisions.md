# HEALTH-OPS — Decisões técnicas

Registro de decisões arquiteturais relevantes.

---

## 001 — Playwright apenas para login

**Decisão:** usar Playwright somente para autenticação. Todo o restante usa `requests.Session`.

**Motivo:** o Vivver usa `token_random` gerado por JavaScript no login, impossível de reproduzir via HTTP puro. Após o login, cookies são suficientes para todas as operações.

**Implementação:** `auth.py` faz login via Playwright, extrai cookies, retorna `requests.Session`. Cookies salvos em `.vivver_cookies.json` e reutilizados nas execuções seguintes.

---

## 002 — Cache de cookies em arquivo

**Decisão:** salvar cookies em `.vivver_cookies.json` e reutilizar entre execuções.

**Motivo:** evitar abrir browser a cada execução. Playwright é lento e instável como dependência primária.

**Implementação:** ao iniciar, tenta carregar cookies do arquivo e valida com GET em `/desktop`. Se sessão inválida ou arquivo inexistente, refaz o login.

---

## 003 — Catálogo em memória

**Decisão:** manter catálogo completo em memória durante a execução.

**Motivo:** evitar chamadas HTTP repetidas ao ERP durante matching e resolução de códigos. Busca em O(1) via dicionário.

**Trade-off:** sync completo a cada startup. Com 2.698 princípios e 13.671 produtos, o tempo é aceitável agora. Futuramente migrar para SQLite com sync incremental.

---

## 004 — Revisão humana antes de executar no ERP

**Decisão:** toda criação passa por fila de revisão antes de ser executada.

**Motivo:** evitar duplicidade, erro farmacológico e inconsistência de dados no ERP de prefeituras.

**Implementação:** `ReviewQueue` persiste em `data/review_queue.json`. API FastAPI expõe `/reviews` e `/approve/{id}`.

---

## 005 — Mesmo código para princípio e produto

**Decisão:** princípio ativo e produto compartilham o mesmo código no Vivver.

**Motivo:** regra de negócio do próprio ERP. O vínculo entre eles usa o código como referência.

**Implementação:** `CodeGenerator` gera `max_codigo_existente + 1` considerando todos os produtos e princípios do catálogo.

---

## 006 — Extração de ID do HTML de resposta

**Decisão:** extrair o ID do produto criado a partir do HTML retornado pelo POST.

**Motivo:** o Vivver retorna status 200 com HTML (não JSON) após criação. O ID está em campo hidden `<input name="amx_produto[id]" value="...">`.

**Fallback:** se não encontrado no HTML, captura o ID via sync do catálogo após criação.

---

## 007 — Chave do CODFORMA é campo "1", não "0"

**Decisão:** usar campo `"1"` do dicionário de formas farmacêuticas como código.

**Motivo:** campo `"0"` é o índice da linha (DT_RowId sequencial). Campo `"1"` é o código real que o Vivver usa no campo `CODFORMA`. Bug identificado e corrigido em `catalog_repository.py`.

---

## 008 — VIVVER_USERNAME no .env (não USERNAME)

**Decisão:** usar `VIVVER_USERNAME` como nome da variável de ambiente.

**Motivo:** `USERNAME` é variável reservada do sistema operacional Windows. `os.getenv("USERNAME")` retornava o usuário do Windows (`alenc`) em vez do valor do `.env`.

---

## 009 — Campo "dados" na resposta da API Vivver

**Decisão:** tratar campo `"dados"` como lista de resultados (não `"data"` padrão DataTables).

**Motivo:** o Vivver usa `"dados"` em português em vez do padrão `"data"`. Bug identificado que impedia paginação correta e fazia o sync retornar só os primeiros 100 registros.

**Implementação:** `_get()` em `catalog.py` verifica `"dados"` primeiro, depois `"data"` como fallback.
