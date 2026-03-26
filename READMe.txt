No arquivo ZIP contém:

Enfim funcionou o cadastro de principio + cadastro de produto + vinculo!
forma farmacêutica errado, sem grupo e subgrupo

sem origem XML/Planilha

Rodando
Rodar pipeline no PC::
python -m uvicorn app.api.server:app

vai chamar o fastApi, na tela digite: 
http://127.0.0.1:8000/docs
1 - em GET - Clicar em tryout
2 - execute
Curl

curl -X 'GET' \
  'http://127.0.0.1:8000/reviews' \
  -H 'accept: application/json'

3 - Em POST - Clicar em Tryout
4 - em item ID (colocar 1)
5 - execute

Vai criar principio, criar produto, depois fazer o vinculo de principio com produto!
TOP VOCÊ CONSEGUIU!

PS C:\Users\alenc\OneDrive\Documentos\health-ops> 

no próximo passo estamos resolvendo formafarmaceutica
