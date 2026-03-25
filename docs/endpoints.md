# Endpoints Vivver descobertos

Base URL:

```
https://{tenant}.vivver.com
```

Endpoints identificados:

```
/amx/produto.json
/amx/principio_ativo.json
/amx/unidade_medida.json
/amx/forma_farmaceutica.json
/amx/unidade_produto.json
```

Parâmetros utilizados:

```
start
length
```

Exemplo:

```
/amx/produto.json?start=0&length=1000
```

Formato de resposta:

DataTables server-side:

```
{
  draw,
  recordsTotal,
  recordsFiltered,
  data: [...]
}
```
