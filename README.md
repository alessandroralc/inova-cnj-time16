# inova-cnj-time16

## A Solução

As inconsistências nas movimentações em grande parte dos processos em tramitação têm efeitos danosos nas estatísticas dos Tribunais, pois produzem dados de pouca qualidade e informações pouco confiáveis. Dessa forma, verifica-se prejuízo à gestão estratégica da Justiça e ao gerenciamento funcional dos Tribunais e suas unidades judiciárias, decorrentes da apuração incorreta de indicadores de interesse administrativo e institucional.

Isso pode até comprometer o dimensionamento da quantidade de servidores necessários, bem como a lotação dos mesmos, e a implantação e o fechamento de unidades judiciárias. Ademais, há também prejuízos aos jurisdicionados, tanto reclamantes quanto reclamados, com processos arquivados sem a devida sentença, com depósitos em conta, etc.

As detecções destas inconsistências ainda é um processo extremamente manual e laborioso, com o extenso acervo de processos esta tarefa se torna ainda mais difícil. O trabalho necessário para melhorar a qualidade destes dados acaba demanda muita atenção e esforçou por múltiplos servidores dos diferentes órgãos.

Técnicas automatizadas para a detecção destas inconsistências costumam ser bastante pontuais e sua gestão muito difícil. Boa parte disso é porque as regras a serem implementadas nestas técnicas são regras complexas do domínio jurídico e existe uma grande dificuldade em passar estas regras para os especialistas de TI para o seu desenvolvimento. Por fim, estas soluções concentram bastante a dependência no setor de TI e a alteração das regras, quando necessário, é um processo extremamente trabalhoso que precisa envolver uma equipe integrada com profissionais especialistas de diferentes áreas: jurídica, estatísticas e tecnologia da informação.

### Persona 1: Juiz e Desembargador:

O juiz Antônio é extremamente diligente. Ele possui um processo de trabalho bem definido e sua vara é bastante efetiva. Porém, ele não concorda com a forma como sua vara é vista recebendo constantes críticas quanto a sua produtividade. Sua percepção é que, os números gerados pelas estatísticas não refletem seu esforço e a realidade, este fator o deixa desestimulado.

### Persona 1: Resultados Gerados

O juiz Antônio passa a poder, por meio do comitê judiciário/estatístico, sugerir mudanças no fluxo agindo proativamente para ajuste nas estatísticas.

Se sente mais confiante que a gestão efetiva em seu gabinete se reflete nas estatísticas e em como ele é avaliado e pode perceber gratificações por produtividade. Ele ainda consegue gerar relatórios mais adequadas que o ajudam ainda mais na gestão de seu gabinete e com base nestes dados mais consistentes consegue analisar e efetivar alterações que aumentam a qualidade e produtividade do trabalho.

### Persona 2 - Servidora

Maraísa, apesar de bastante diligente, não consegue entender porque as estatísticas de sua vara no CNJ parecem tão ruins.
Ela ficou muito mais satisfeita de identificar de forma antecipada quando a movimentação processual não refletiu a realidade. Ela consegue agora fazer ajustes a tempo. Seu trabalho é mais reconhecido e ela consegue enxergar melhor pontos de melhoria nos processos de trabalho.

## Vantagens da solução

### Da Efetividade da Solução

#### A solução baseada em limpeza a partir de fluxos customizados possui uma séries de vantagens.

Por meio desta solução é possível identificar a alertar ao usuários uma gama bastante extensa de inconsistências ou fatos atípicos na movimentação processual tais quais:

- Processos baixados sem julgamento
- Processos julgados em colegiado sem uma inclusão na pauta de sessão
- Múltiplos julgamentos em um único processo quando não esperado
- Encerramentos de suspensão sem a movimentação processual indicada
- Movimentos processuais fora de ordem

#### Alta capacidade de customização (podem ser gerados fluxos customizados por justiça ou classes de processos)

A solução se baseia no fato de que as diferentes justiças ou até as diferentes classes processuais podem possuir diferentes fluxos. Para uma adequada análise das estatísticas e das inconsistências na movimentação processual é necessária uma solução que permita a customização da solução para se adequar à necessidade.

A definição do fluxo como é fácil de entender pelos especialistas jurídicos.

#### Proatividade

Possibilidade de passar para a ponta a solução para as instituições e emitir avisos proativamente.

Acredita-se que quanto mais cedo o usuário tiver a ciência da movimentação processual inconsistente ou atípica mais fácil e tempestiva é a correção da mesma.

Fácil apropriação e assim engajamento da equipe negocial (jurídica) na solução tecnológica (a solução com interface permite que o analista jurídico analise os fluxos um a um (substituir por “de cada processo”?) com alto nível de granularidade de customização).

Técnica de alta produtividade, várias inconsistências nos dados são capturadas "automaticamente" à medida que se definem os fluxos.

#### Definição de fluxo próprio com foco analítico estatístico (que diferencia dos fluxos do PJe)

Outra vantagem é que se permite definir um fluxo próprio com foco analítico. Esta possibilidade permite aos especialistas definirem fluxos específicos com o foco analítico sem terem de se preocupar com detalhes de implementação dos sistemas transacionais como o PJe ou o Saj. Esta independência permite que o foco seja de fato as estatísticas a serem geradas o que resulta num trabalho mais efetivo e acurado

### Da Qualidade da Solução

#### A solução foi toda desenvolvida com softwares livres com uso difundido na justiça.

A configuração dos fluxos foi desenvolvida com frameworks livres e containerizada para fácil implantação nos diferentes ambientes que se fizer necessário.

A interface foi desenvolvida com Angular js e a comunicação entre o frontend e o backend utilizando API rest.

O caminhamento no grafo, parte essencial da tecnologia que permite identificar os eventos inconsistentes ocorridos pelos processos, foi desenvolvido a partir de consultas SQL o que permite utilizar a solução facilmente em diferentes bancos de dados. A solução foi entregue usando o banco de dados Postgres que é o mais utilizado para instalações do PJe, o principal sistema de tramitação eletrônica da justiça trabalhista. A visualização dos fluxos de forma gráfica foi toda desenvolvida usando a biblioteca d3.js também uma ferramenta livre.

A parte essencial da tecnologia que é onde se concentram as principais regras de negócio está na definição dos fluxos de dados. Foi apresentada uma interface ao usuário para que se possa gerenciar os fluxos assim como uma interessante visualização de grafos desenvolvida em d3 para facilitar visualizar o fluxo definido. Esta solução permite que o usuário enxergue toda a lógica implementada utilizada no motor de inferências.

A solução foi desenvolvida dependendo apenas dos dados existentes no DataJud. O fluxo de dados da solução passa pelo Elastic Search e é carregado nos banco de dados Postgres. Estas ferramentas são facilmente configuradas para garantir a segurança de dados e a total aderência à LGPD.

#### Da Completude da Solução

Além do interessante motor de inferências baseado em grafos foram desenvolvidas uma interface que conduz o especialista jurídico na definição do fluxo processual.

Estas funcionalidades facilitam bastante a jornada do usuário enquanto descreve as regras de negócio dos fluxos.

Também foi desenvolvida solução em grafo altamente interativa para facilitar o entendimento e visualização do fluxo definido/modelado. O usuário consegue interagir com o fluxo e verificar quais os eventos esperados dado a situação analisada, avaliar as diferentes situações diferentes.

Para facilitar ainda mais a jornada do usuário, foram criados os grupos de situações que permitem muito mais expressividade na definição do fluxo, isto porque permite que se expresse uma série de situações de forma extremamente conciso. Como exemplo, o usuário consegue expressar regras de negócios abrangentes de forma bem facilitada. Por exemplo, ele consegue definir que dado que o processo esteja em qualquer situação considerada como pendente de julgamento, caso o processo seja julgado, a nova situação deverá ser processo julgado. Isto é realizado bastando criar um grupo "pendente de julgamento " e incluir todas as situações pertencentes a este grupo.

Basta então criar uma única transição.
Ainda foi desenvolvido um fluxo pronto para a segunda instância como exemplo de que pode ser melhorado o que torna a tarefa de definição dos fluxos muito mais facilitada.

#### Da Viabilidade da Solução

Conforme já mencionado a equipe optou por implementar uma interessante e poderosa solução com alto poder de expressividade a partir de tecnologias extremamente difundidas. O motor de caminhamento do grafo que permite encontrar as inconsistências foi desenvolvido em SQL e implantado no Postgres, banco de dados já presente em todos os tribunais que possuem o PJe.

Mesmo a ingestão de dados feita a partir do Elastic Search (ferramenta livre já disponível em vários tribunais) pode ser substituída por uma ingestão dos dados diretamente na base de dados Postgres.

Esta característica torna ainda extremamente fácil acoplar a solução a diferentes sistemas. Assim como desenvolver a solução altamente escalável.

Fácil implementação (tecnologia baseado em solução em SQL puro o que permite acoplar a solução em vários sistemas).

## Principais Requisitos

- Ele terá os fluxos baseados em movimentos, diferente do PJe que é por tarefas.
- Poderá ser aplicável a qualquer ramo, uma vez que o usuário vai poder desenhar o seu fluxo.
- Uma vez existindo um fluxo correto, os processos com desvios poderão ter os seus usuários notificados.
- O fluxo desenhado servirá como fonte de referência e mentoria para os usuários das unidades judiciárias.

## Definição do Analisador de fluxos processuais

### O que é o Analisador de fluxos processuais?

É uma solução que permite a partir dos movimentos processuais dos processos, realizar a validação desta movimentação processual.

### Quais as fases compõem o Analisador de fluxos processuais?

O Analisador de fluxos é composto das seguintes fases:

1. Preparação do fluxo processual para aquele tipo do processo (pode ser por tipo de classe, justiça)
1. Geração do histórico de eventos
1. Interpretação dos eventos

### Preparação dos fluxos processuais

O Analisador de fluxos processuais depende de uma preparação do fluxo processual para cada tipo de processo que se deseja interpretar.
Esta preparação é realizada pelos seguintes passos:

1. Definição das situações dos processos
1. Definição dos eventos dos processos
1. Definição dos grupos de situações dos processos
1. Definição do mapeamento dos movimentos processuais para eventos dos fluxos
1. Definição das transições esperadas do fluxo

### Como funciona a geração do histórico de eventos do processo?

Nesta fase da análise são verificados todos os movimentos processuais existentes para cada processo.
Estes movimentos processuais são ordenados e para cada movimento processual que possuam um mapeamento para um evento, é gerado um evento.
Ao final desta fase, tem-se um histórico de eventos do processo.
Por exemplo:

1. Distribuição
1. Suspensão ou sobrestamento
1. Encerramento ou revogação da suspensão ou sobrestamento
1. Conclusão para decisão ou voto (relatar)
1. Restituições pelo relator para remessa ao MPT
1. Recebimento do processo após envio ao MPT
1. Conclusão para decisão ou voto (relatar)
1. Recebido para incluir em pauta
1. Inclusão em Pauta
1. Decisão colegiada terminativa
1. Remessa à primeira instância

### Como funciona o interpretador de eventos da solução?

A interpretação dos eventos acontece de forma ordenada e iterativa.

A cada novo evento, verifica-se se aquele evento era esperado para a situação atual do processo e qual será a nova situação após o evento ocorrido.
As alterações de situações do processo a partir dos eventos ocorridos no processo são chamados de transições.

No exemplo anterior, após a distribuição do processo, o evento de Suspensão ou sobrestamento, altera a situação do processo para Suspenso ou Sobrestado.
Enquanto o evento (11) Remessa à primeira instância altera o processo para baixado.

## Entendendo a solução de fluxos

A solução de fluxos foi criada para facilitar a aplicação das regras de negócio dos trâmites processuais

### O que são as situações do processo?

As situações do processo no fluxo demonstram em que estágio ou condição o processo se encontra.
Servem para definir os estados do processo.
Exemplo de situações:

- Pendente de conclusão para relatar (PCR)
- Concluso para decisão ou Voto
- Aguardando pauta em secretaria

### O que são os eventos?

Os eventos definem os acontecimentos sobre o processo que tendem a alterar a situação dos mesmos.
Eles representam as ações ocorridas relacionadas ao processo.

Note que em nosso trabalho, os eventos serão gerados a partir dos movimentos processuais.

Por isto, teremos um mapeamento que definirá quais os movimentos processuais que representarão quais eventos.
Exemplos de Eventos:

- Suspensão ou Sobrestamento
- Inclusão em Pauta
- Decisão colegiada terminativa
  Obs: Algumas movimentações processuais podem não ter consequências importantes do ponto de vista analítico. Estas movimentações em geral não terão um mapeamento para um evento.

### O que são as transições?

As transições é que vão definir as regras de negócio do trâmite processual. São elas que determinam como a situação dos processos são atualizadas à medida em que acontecem os eventos. Por meio da definição das transições do fluxo, os analistas jurídicos, definirão o que se espera sobre o fluxo e sobre a situação do processo quando ocorrerem os eventos.

Do ponto de vista técnico, as transições que permitem o "caminhamento no grafo". Elas definem se um evento dada uma certa situação é consistente ou não e qual a nova situação do processo caso o evento ocorra. A definição das transições é composta da situação de origem (em qual situação o processo deve estar para que a mesma se aplique), do evento (o evento ocorrido que "disparou" a transição) e do destino, qual a nova situação do processo dado após a ocorrência do evento.

Exemplo de transição:

- Origem: Pendente de conclusão para relatar (PCR)
- Evento: Suspensão ou sobrestamento (SS)
- Destino: Processo Suspenso ou Sobrestado (PSS)
- Flag: consistente

Conforme esta transição, dado um processo na situação que está pendente de conclusão para relatar, caso ocorra uma suspensão ou sobrestamento do processo, dever-se-á atualizar a situação, de forma que o processo constará como suspenso ou sobrestado.

### Para que servem as transições inconsistentes?

As transições inconsistentes existem para que se possa definir a situação do processo mesmo que aconteça um evento inesperado. Um exemplo disto é que não se espera que ocorra a baixa de um processo que não tenha sido solucionado. Então, caso ocorra uma baixa de processo ainda pendente de conclusão para relatar, podemos decidir que a situação do processo deve ser atualizada para baixado mas que este evento é inesperado, inconsistente ou atípico.

A vantagem desta é que poderemos alertar aos interessados a ocorrência de uma transição inconsistente.

Exemplo de transição:

- Origem: Pendente de conclusão para relatar (PCR)
- Evento: Remessa à primeira instância (RPI)
- Destino: Baixado (B)
- Flag: inconsistente

### O que são os grupos de situações?

Os grupos de situações foram criados para permitir definir várias transições de forma mais concisa aumentando a possibilidade dos analistas jurídicos em definir os fluxos.

Assim, ao invés de definir uma única situação origem, pode-se definir todo um grupo de situações de origem.
Por exemplo, pode-se definir que caso o processo esteja em qualquer situação do grupo pendente de julgamento, caso ocorra uma decisão colegiada terminativa, considere o processo julgado/solucionado. Ou de forma análoga caso o processo esteja em qualquer situação do grupo pendente de baixa, caso ocorra uma remessa à primeira instância, considere o processo baixado.

Exemplo de transição de grupo:

- Origem: Grupo Pendente de baixa
- Evento: Remessa à primeira instância (RPI)
- Destino: Baixado (B)
- Flag: inconsistente

## Arquitetura da solução

![Arquitura do Sistema](doc/arquitetura.png)

### Armazenamento

#### ElasticSearch

Utilizado como base de dados NoSQL analítica. Os dados brutos dos arquivos jsons do DataJud são indexados. O dashboard contruído é exibido diretamente na aplicação. A carga da prova de conceito foi realizada com os dados disponibilizados pelo desafio.

- O dashboard foi construído com o Kibana e permite que os usuários visualizem de forma integrada a nossa aplicação as informações do seu acervo.

##### Licenciamento:

- ElasticSearch: Apache License 2.0
- Docker: Apache License 2.0

#### PostreSQL

Utilizado para dar estrutura das tabelas que suportam a lógica da aplicação. Os dados do DataJud são transformados para estrutura relacional diretamenta da base do ElasticSearch.

- O ETL importa os dados básicos do processo e a movimentação. São esses movimentos que são validados sistema.
- Ambos os componentes são instanciados e carregados com containers Dockers. Toda carga de dados e ETL é realizado automaticamente com scripts de build do sistema.

##### Licenciamento:

- PostgreSQL: use, copy, modify, and distribute.

### Backend - API Rest

#### Flask Restful API

Construída com o framework Flask que é escrito na linguagem Python. Implementa os padrões REST e totalmente desacoplada dos demais componentes, o que permite fácil escalabilidade por containers Docker e manutenção.

- A grande vantagem deste tipo de integração, por ser restful, é a possibilidade dos tribunais regionais integrar com o seus geradores de json (DataJud) ou até mesmo utilizando integração com as bases dos sistemas transacionais.

Para servir as requisições em modo concorrente foi utilizado o WSGI Gunicorn que aumenta a escabilidade e o tratamento de requisições paralelas do flask.

##### Licenciamento:

- Flask: BSD License
- Gunicorn: The MIT License

#### Task Queue

- Celery: framework Python para gestão e execução de tarefas assíncronas. Utilizado para atualização e cargas de dados. Especificamente os endpoints para: carregar e validar todos os processos de um tribunal especifico; carregar e validar um único processo. A notificação dos usuários para os processos inconsistentes também será executada como uma tarefa assincrona pelo worker celery.
- Redis: estrutura de dados em memória utilizado como message broker entre a API e as tarefas assíncronas.

A solução utilizada uma estrutura de filas assincronas, justamente para prever futuras evoluções e altas cargas de dados.
Com a existência de um gerenciador de filas, bem como containers de workers isolados, a solução é possível de ser escalada horizontalmente.

##### Licenciamento:

- Celery: BSD License
- Redis: BSD License
  Frontend

#### Documentação das APIs

Para as APIs, criamos a documentação a seguir que descreve os endpoints, métodos e exemplos:
[APIs Rest Sanjud](backend/README.md)

##### Instruções para a execução do docker-compose

1. Criar um arquivo .env na pasta docker com os propriedades abaixo:

```
FLASK_ENV=dev
APP_PORT=5002
WORKERS=4
THREADS=2
WORKER_CLASS=gthread
DATABASE_URL=postgres://sanjus_app:XXXX@postgres:5432/sanjus
GUNICORN_CMD_ARGS=--bind '0.0.0.0:5002' --workers 8 --worker-class gthread --threads 2 --config python:config_gunicorn
DEBUG=True
prometheus_multiproc_dir=/tmp
METRICS_PORT=5003
TZ=America/Sao_Paulo
HOST_ELASTIC=time16-datajud.ddns.net
PORT_ELASTIC=9200
USER_ELASTIC=elastic
PASS_ELASTIC=XXXXX
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
```

2. Automaticamente o container (sanjus_init) irá executar as migrations do banco de dados, abaixo detalhamos alguns comandos que podem ser utilizados para a geração automatizada de migrations.

Caso seja alterada alguma entidade do módulo src.entidades é necessário executar o alembic para que uma nova migration seja gerada para isso, deve-se acessar a pasta do projeto e executar o comando: `python manage.py db migrate`.
Após a execução do `migrate` será criado um novo arquivo .py dentro de migrations/versions. É recomendável a validação e atualização do arquivo antes de efetivar a migration. Para efetivar a migration o seguinte comando pode ser utilizado `python manage.py db upgrade`
Também é possível realizar downgrade e outros tipos de atualização conforme detalhamento [Documentação Alembic](https://alembic.sqlalchemy.org/en/latest/)

### Frontend

O Frontend está versionado no repositório git ![time16-frontend](https://github.com/jhcruvinel/time16)
Considerando que os fluxos dos processos são complexos, e extensos. A solução foi feita pensando no uso para desktop.
Justamente pela possível dificuldade em visualizar fluxos em dispositivos com telas reduzidas.

Desta forma a aplicação foi construída utilizando o framework Angular. Para melhorar a experiência do usuário foram utilizados os componentes da biblioteca Angular Material.

##### Licenciamento:

    ◦ Angular: The MIT License
    ◦ Angular Material: The MIT License

### Áreas de conhecimento e técnicas envolvidas

A aplicação tem caráter multidisciplinar que envolve áreas da Computação, Matemática e Direito(principalmente do Código do Processo Civil):

- O modelo conceitual que mapeia eventos e situações de processos a partir das movimentações da TPU/CNJ envolve teoria dos grafos, mais especificamente modelagem. Esse item é o que mais une as três áreas de conhecimento.
- Para possibilitar o uso da técnica é necessário agregar diversas fontes de dados (Datajud, tabelas unificadas do CNJ). Para isso foram utilizadas técnicas de ETL e modelagem de banco de dados.
- Além da conversão para construção do grafo, a ferramenta guia o usuário nas etapas necessárias para facilitar a gestão dos modelos.
- Destacamos a utilização da técnica de análise de inconsistência de grafos baseada em regras. Para possibilitar essa técnica a arquitetura do sistema utilizou de uma arquitetura assíncrona com controle de tarefas e message broker.

### Ambiente de execução

Para a disponibilização da aplicação utilizamos servidores (Droplets) da [Digital Ocean](www.digitalocean.com). Como todos os componentes da solução estão em containers, o gerenciamento, bem como o monitoramento é feito de forma automatizada e ágil.
Todo o ambiente está rodando em uma VM com 4GB, e 2 processadores.
Durante os testes e nos monitoramentos que realizamos o máximo de load que máquina chegou foi em 0,5.
![Load](doc/load-cpu.png)

Já o uso de memória RAM se mantém constante em 70%
![Memória](doc/memoria.png)

Acesso para a aplicação: [Sanjus](http://time16-sanjus.ddns.net/)

## Melhorias futuras:

A solução ora apresentada:

- Poderá ser uma fonte de convergência das regras de negócio do JN;
- Poderá integrar ao fluxo do Pje, para que os movimentos e dados da TPU estejam no cerne do PJe;
- Poderá registrar fluxos a partir de ferramentas de process mining, ou seja, podemos gerar fluxos automaticamente e o usuário somente validar (integração com o desafio 1).
