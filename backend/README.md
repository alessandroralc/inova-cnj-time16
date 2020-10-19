# Detalhamento dos serviços Rest disponíveis

## Tribunal

|HTTP Method|Action|Examples|
|---|---|---|
|GET|Retorna todos os Tribunais que possuem fluxo|/api/v1.0/tribunal|
---
## Grau

|HTTP Method|Action|Examples|
|---|---|---|
|GET|Retorna todos os graus com fluxo disponíveis para um determinado Tribunal|api/v1.0/grau/`<string:cod_tribunal>`|
---
## Situações do processo

*Subsituindo o serviço antigo*: `/situacoes`

|HTTP Method|Action|Examples|
|---|---|---|
|GET|Obter todas as situações|/api/v1.0/situacao|
|GET|Obter uma situação especifica|/api/v1.0/situacao/`<int:id_situacao>`|
|GET|Obter situações de um determinado Tribunal e Grau|/api/v1.0/situacao/`<string:cod_tribunal>`/`<string:cod_instancia>`|
|POST|Persistir uma nova situação|/api/v1.0/situacao|
|DELETE|Remover uma situação|/api/v1.0/situacao|

Para o `POST` e o `DELETE` o conteúdo deverá ser enviado como um json no body.
Exemplo de json para o `POST`:
```
{"ind_principal": "S", 
"ds_situacao": "Início de fluxo", 
"sg_tribunal": "TRT3", 
"ind_ri": "S", 
"cd_situacao": "I",
"sg_grau": "G2"}
```
Exemplo de json para o `DELETE`:
```
{"id_situacao": 1}
```
---
## Eventos

*Subsituindo o serviço antigo*: `/eventos`

|HTTP Method|Action|Examples|
|---|---|---|
|GET|Obter todos os eventos|/api/v1.0/evento|
|GET|Obter um evento especifico|/api/v1.0/evento`<int:id_evento>`|
|POST|Persistir um novo evento|/api/v1.0/evento|
|DELETE|Remover um evento|/api/v1.0/evento|

Para o `POST` e o `DELETE` o conteúdo deverá ser enviado como um json no body.
Exemplo de json para o `POST`:
```
{"cd_evento": "CP", 
"ind_tipo_especial": "P", 
"ind_fluxo_ri": "N", 
"ds_evento": "Conclusão para o presidente"}
```
Exemplo de json para o `DELETE`:
```
{"id_evento": 1}
```
---
## Fluxo

*Subsituindo o serviço antigo*: `/fluxo/*`

|HTTP Method|Action|Examples|
|---|---|---|
|GET|Obter todas os fluxos|/api/v1.0/fluxo|
|GET|Obter um fluxo especifico|/api/v1.0/fluxo`<int:id_fluxo>`|
|GET|Obter os fluxos de um determinado Tribunal e Grau|/api/v1.0/fluxo/`<string:cd_tribunal>`/`<string:cd_grau>`|
|GET|Obter os fluxos de um determinado Tribunal e Grau, que sejam consistententes ou não (formato gráfico de rede)|/api/v1.0/fluxo/rede/`<string:cd_tribunal>`/`<string:cd_grau>`/`<string:ind_consistente>`|
|POST|Persistir um novo fluxo|/api/v1.0/fluxo|
|DELETE|Remover um fluxo|/api/v1.0/fluxo|

Para o `POST` e o `DELETE` o conteúdo deverá ser enviado como um json no body.
Exemplo de json para o `POST`:
```
{"id_evento": 28, 
"ind_consistente": "N", 
"ind_fluxo_ri": "N", 
"sg_tribunal": "TRT3", 
"id_situacao_destino": 141, 
"id_situacao_origem": 61, 
"ind_efetiva": "S", 
"id_grupo": 10, 
"sg_grau": "G2"}
```
Exemplo de json para o `DELETE`:
```
{"id_fluxo_movimento": 1}
```