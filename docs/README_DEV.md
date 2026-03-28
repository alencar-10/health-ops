# HEALTH-OPS — Guia para desenvolvedores

## Pré-requisitos

- Python 3.13+
- pip
- Playwright instalado (`playwright install chromium`)

---

## Configuração inicial

1. Cria o arquivo `.env` na raiz do projeto:

```
VIVVER_BASE_URL=https://{tenant}.vivver.com
VIVVER_USERNAME=seu_usuario
VIVVER_PASSWORD=sua_senha
```

2. Instala dependências:

```bash
pip install -r requirements.txt
```

3. Instala o browser do Playwright:

```bash
playwright install chromium
```

---

## Executar o servidor

```bash
python -m uvicorn app.api.server:app --loop asyncio
```

Swagger disponível em: `http://127.0.0.1:8000/docs`

Atenção (Windows): clicar na janela do PowerShell pausa a execução. Pressione qualquer tecla para continuar.

---

## Scripts de teste

```bash
# testa autenticação e cache de cookies
python -m scripts.test_auth

# testa sincronização do catálogo
python -m scripts.test_catalog_sync

# testa normalização farmacêutica
python -m scripts.test_normalizer

# testa matching de produtos
python -m scripts.test_product_matcher

# testa pipeline completo
python -m scripts.test_product_pipeline

# testa catálogo Vivver
python -m scripts.test_vivver_catalog
```

---

## Fluxo de uso

1. Sobe o servidor
2. Acessa `http://127.0.0.1:8000/docs`
3. Chama `GET /reviews` para ver itens pendentes
4. Chama `POST /approve/{id}` para aprovar e criar no ERP

---

## Arquivos importantes

| Arquivo | Função |
|---|---|
| `app/bootstrap/application.py` | composição de todos os objetos |
| `app/config/settings.py` | leitura do `.env` |
| `app/adapters/vivver/http/auth.py` | autenticação |
| `app/services/product_creator.py` | orquestra criação completa |
| `app/catalog/catalog_repository.py` | catálogo em memória |
| `data/review_queue.json` | fila de revisão persistida |
| `.vivver_cookies.json` | cache de cookies (não commitar) |

---

## Arquivos que não devem ir para o Git

```
.env
.vivver_cookies.json
state.json
```

Verifique se estão no `.gitignore`.

---

## Dependências principais

```
fastapi
uvicorn
requests
playwright
beautifulsoup4
rapidfuzz
python-dotenv
pandas
openpyxl
```

---

## Convenções

- Variáveis de ambiente: prefixo `VIVVER_` para evitar conflito com variáveis do sistema operacional
- Códigos gerados: faixa `max_existente + 1`
- Chaves do catálogo: sempre `str` (nunca `int`)
- Forma farmacêutica: campo `"1"` do dicionário é o `CODFORMA` real
