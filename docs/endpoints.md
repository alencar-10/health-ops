# HEALTH-OPS — Endpoints Vivver

Base URL:

```
https://{tenant}.vivver.com
```

---

## Autenticação

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/login` | página de login (CSRF token) |
| POST | `/login/valida_presenca_termo` | valida credenciais |
| POST | `/login/create` | cria sessão autenticada |

Fluxo automatizado via Playwright. Cookies extraídos e reutilizados via `requests.Session`.

---

## Catálogo (leitura)

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/amx/produto.json` | lista de produtos |
| GET | `/amx/principio_ativo.json` | lista de princípios ativos |
| GET | `/amx/unidade_medida.json` | unidades de medida |
| GET | `/amx/forma_farmaceutica.json` | formas farmacêuticas |
| GET | `/amx/unidade_produto.json` | unidades de produto |

Parâmetros de paginação:

```
?start=0&length=1000
```

Formato de resposta (Vivver):

```json
{
  "dados": [...],
  "Total de registros": 2698,
  "registrosFiltrados": 2698
}
```

Atenção: o Vivver usa `"dados"` (português) em vez do padrão `"data"` do DataTables.

---

## Princípio ativo (escrita)

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/amx/principio_ativo` | cria princípio ativo |

Campos obrigatórios no payload:

```
workMode: wmInsert
amx_principio_ativo[codprincipio]: código
amx_principio_ativo[nomprincipio]: nome
amx_principio_ativo[codforma]: código da forma farmacêutica
amx_principio_ativo[indativo]: S
```

---

## Produto (escrita)

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/amx/produto` | cria produto |
| POST | `/amx/produto/{id}` | atualiza produto (PATCH via `_method=patch`) |

Campos obrigatórios no payload (criação):

```
workMode: wmInsert
amx_produto[codproduto]: código
amx_produto[nomproduto]: nome
amx_produto[inddatvalidade]: S
amx_produto[indlote]: S
amx_produto[indativo]: S
```

A resposta é HTML (status 200). O ID do produto criado está em:

```html
<input name="amx_produto[id]" value="14253">
```

Payload para vínculo com princípio ativo:

```
_method: patch
workMode: wmEdit
amx_produto[id]: id_do_produto
amx_produto[id_principioativo]: id_do_principio
```

---

## Regra de negócio — ordem de criação

```
1. criar princípio ativo (CODFORMA obrigatório)
2. criar produto (mesmo código do princípio)
3. vincular produto ao princípio (PATCH)
   → após vínculo, CODFORMA é herdado do princípio pelo produto
```

---

## API interna (FastAPI)

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/reviews` | lista itens pendentes de revisão |
| POST | `/approve/{item_id}` | aprova e executa criação no ERP |

Swagger disponível em: `http://127.0.0.1:8000/docs`
