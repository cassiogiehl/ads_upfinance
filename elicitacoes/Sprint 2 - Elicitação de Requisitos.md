# 1- Introdução

A Sprint 2 tem como objetivo elicitar, analisar e documentar os requisitos da UPFinance, identificando as necessidades do usuário e transformando-as em requisitos funcionais, requisitos não funcionais e histórias de usuário.

A UPFinance é uma aplicação Web de gerenciamento financeiro pessoal criada para reduzir o esforço manual do controle financeiro realizado atualmente por meio de planilhas e auxiliar o usuário na interpretação de sua situação financeira. A análise da situação financeira será baseada na regra 50-30-20.


# 2 - Elicitação e análise dos requisitos

A elicitação dos requisitos da UPFinance parte da identificação do problema enfrentado pelo usuário e das necessidades relacionadas ao controle financeiro pessoal.

Atualmente, o usuário realiza o controle de seus gastos por meio de planilhas Excel. Esse processo exige atualizações manuais frequentes e pode levar ao esquecimento ou adiamento dos registros. Além disso, a planilha não auxilia diretamente na interpretação da distribuição dos gastos.

A partir desse contexto, foram identificadas as principais necessidades:

* reduzir o esforço manual para manter o controle financeiro;
* compreender se a distribuição dos gastos está adequada à renda;
* visualizar os gastos organizados nos pilares Essencial, Pessoal e Futuro;
* reduzir o esforço para registrar gastos realizados no cartão;
* receber alertas quando os limites da regra 50-30-20 forem ultrapassados;
* acompanhar pagamentos recorrentes e seus vencimentos.

Os requisitos são então derivados dessas necessidades e organizados de forma que possam ser posteriormente verificados e rastreados.



# 3 - Requisitos Funcionais

Requisitos funcionais representam aquilo que o sistema deverá fazer.

### RF001 — Cadastrar movimentações financeiras

O sistema deverá permitir o cadastro de movimentações financeiras de entrada e saída.

Cada movimentação deverá possuir informações como descrição, valor, tipo e categoria.

RF002 — Categorizar movimentações

O sistema deverá permitir que as movimentações sejam associadas às categorias disponibilizadas pelo sistema.

RF003 — Associar categorias aos pilares

Cada categoria deverá estar previamente associada a um dos pilares da regra 50-30-20:

* Essencial;
* Pessoal;
* Futuro.

RF004 — Visualizar movimentações

O sistema deverá permitir ao usuário visualizar as movimentações e os gastos registrados.

RF005 — Apresentar distribuição dos gastos

O sistema deverá apresentar a distribuição dos gastos do usuário conforme a regra 50-30-20.

RF006 — Interpretar a situação financeira

O sistema deverá interpretar a situação financeira do usuário com base na distribuição dos gastos entre os pilares Essencial, Pessoal e Futuro.

A interpretação será determinística e baseada na regra 50-30-20, não utilizando serviços de IA ou LLM na primeira versão.

RF007 — Emitir alertas de limite

O sistema deverá emitir alertas quando os gastos de determinado pilar ultrapassarem o limite estabelecido pela regra 50-30-20.

RF008 — Enviar fatura do cartão

O sistema deverá permitir o envio opcional de uma fatura de cartão de crédito em formato PDF.

RF009 — Interpretar fatura do cartão

O sistema deverá ler e interpretar as informações presentes na fatura de cartão de crédito enviada pelo usuário.

RF010 — Identificar pagamentos recorrentes

O sistema deverá utilizar o histórico de movimentações financeiras para identificar pagamentos recorrentes.

RF011 — Alertar sobre pagamentos recorrentes

O sistema deverá alertar o usuário sobre pagamentos recorrentes identificados a partir do histórico.

Os requisitos funcionais acima correspondem aos requisitos funcionais de alto nível definidos no Documento de Visão do Produto.



# 4 - Requisitos Não Funcionais

Requisitos não funcionais definem características, restrições ou condições relacionadas à qualidade e à operação do sistema, e não uma função específica que o usuário executará.

RNF001 — Acesso Web

O sistema deverá ser acessível por meio de um navegador Web.

RNF002 — Responsividade

O sistema deverá apresentar uma interface responsiva, permitindo sua utilização em computadores e dispositivos móveis.

Esses são os requisitos não funcionais de alto nível atualmente definidos no Documento de Visão do Produto.

Observação: não foram definidos nos documentos atuais valores específicos para tempo de resposta, disponibilidade, acessibilidade, criptografia ou outros atributos de qualidade. Portanto, esses itens não serão inventados nesta Sprint.



# 5 -Diferença entre requisitos funcionais e não funcionais

Para evitar ambiguidades durante a especificação:

| Tipo                    | Descrição                                                         | Exemplo na UPFinance                  |
| ----------------------- | ----------------------------------------------------------------- | ------------------------------------- |
| Requisito funcional     | Define o que o sistema deve fazer                                 | Cadastrar uma movimentação financeira |
| Requisito não funcional | Define uma característica, condição ou restrição de funcionamento | Ser acessível por navegador Web       |
| Regra de negócio        | Define uma regra que deve ser respeitada no domínio               | Utilizar a distribuição 50-30-20      |

Na UPFinance, por exemplo, "o sistema deverá cadastrar uma movimentação" é uma função. Já "o sistema deverá ser acessível através de navegador Web" representa uma característica/condição do produto. A regra que determina 50% para Essencial, 30% para Pessoal e 20% para Futuro é uma regra de negócio.



# 6 - Regras de negócio

RN001 — Distribuição 50-30-20

A interpretação da situação financeira deverá utilizar:

* 50% da renda para gastos Essenciais;
* 30% para gastos Pessoais;
* 20% para o Futuro.

RN002 — Associação das categorias

Cada categoria disponibilizada pelo sistema deverá estar previamente associada a um dos três pilares.

RN003 — Limite dos pilares

O limite de cada pilar deverá ser calculado em relação à renda do usuário.

Quando os gastos de determinado pilar ultrapassarem o percentual correspondente, o limite será considerado excedido.

Exemplo: para uma renda de R$ 10.000, o limite do pilar Essencial será de R$ 5.000.

RN004 — Percentuais fixos

A distribuição 50-30-20 permanecerá fixa na primeira versão do produto.



# 7 - Persona

A persona foi construída a partir do perfil de usuário definido no Documento de Visão do Produto.

Persona — Rafael

Idade: 25 anos
Ocupação: profissional em início de carreira
Conhecimento financeiro: básico
Ferramenta atual: planilha Excel
Objetivo: organizar melhor sua vida financeira e entender para onde seu dinheiro está indo.

Perfil:

Rafael recebe uma renda mensal e utiliza uma planilha para registrar seus gastos. Apesar de conseguir registrar as informações, ele possui dificuldade para interpretar se está gastando valores adequados em cada área da sua vida financeira.

Principais dificuldades:

* esquece de registrar alguns gastos;
* precisa atualizar a planilha manualmente;
* tem dificuldade para interpretar os dados;
* não sabe facilmente quando ultrapassou determinado limite;
* possui dificuldade para acompanhar pagamentos recorrentes.

Necessidades:

* registrar entradas e saídas de forma simples;
* categorizar os gastos;
* visualizar a distribuição financeira;
* compreender sua situação financeira;
* receber alertas;
* acompanhar pagamentos recorrentes.

A persona representa o usuário principal descrito nos documentos: uma pessoa que utiliza planilhas para controle financeiro, mas não possui conhecimento de educação financeira suficiente para interpretar adequadamente sua situação.



# 8 - Jornada do usuário
Etapa	Ação do usuário	Necessidade	Resposta esperada da UPFinance
1. Acesso	Acessa a aplicação	Ter acesso ao controle financeiro	Disponibilizar a aplicação Web
2. Registro	Cadastra sua renda e movimentações	Registrar sua situação financeira	Armazenar entradas e saídas
3. Organização	Categoriza os gastos	Organizar as movimentações	Associar categorias aos pilares
4. Visualização	Consulta seus gastos	Entender onde está gastando	Apresentar movimentações e distribuição
5. Análise	Consulta sua situação financeira	Saber se os gastos estão equilibrados	Interpretar os gastos pela regra 50-30-20
6. Alerta	Recebe um alerta	Saber quando ultrapassou um limite	Informar o pilar que excedeu o limite
7. Cartão	Envia uma fatura PDF, se desejar	Reduzir o trabalho de registrar gastos do cartão	Ler e interpretar a fatura
8. Recorrências	Consulta pagamentos recorrentes	Acompanhar contas que se repetem	Identificar e alertar sobre recorrências

Essa jornada representa o fluxo principal previsto para o produto: o usuário fornece suas informações, a UPFinance organiza e analisa os dados segundo a regra 50-30-20 e apresenta informações, interpretações e alertas.

# 9 - Histórias de Usuário

As histórias de usuário foram elaboradas utilizando a estrutura:

Como usuário, quero registrar minhas movimentações financeiras, para extrair inteligência a partir dos meus dados.

US01 — Registrar movimentação

Como usuário da UPFinance,
quero cadastrar uma entrada ou saída financeira,
para manter meu controle financeiro atualizado.

Relacionamento: RF001

US02 — Categorizar gasto

Como usuário da UPFinance,
quero categorizar meus gastos,
para organizá-los de acordo com os pilares financeiros.

Relacionamento: RF002 e RF003

US03 — Visualizar gastos

Como usuário da UPFinance,
quero visualizar minhas movimentações e gastos registrados,
para acompanhar minha situação financeira.

Relacionamento: RF004

US04 — Analisar distribuição financeira

Como usuário da UPFinance,
quero visualizar a distribuição dos meus gastos entre Essencial, Pessoal e Futuro,
para compreender como minha renda está sendo utilizada.

Relacionamento: RF005 e RF006

US05 — Receber alerta de limite

Como usuário da UPFinance,
quero receber um alerta quando ultrapassar o limite de um pilar,
para identificar que preciso melhorar a distribuição dos meus gastos.

Relacionamento: RF007

US06 — Importar fatura

Como usuário da UPFinance,
quero enviar minha fatura do cartão em PDF,
para reduzir o esforço necessário para registrar meus gastos do cartão.

Relacionamento: RF008

US07 — Interpretar fatura

Como usuário da UPFinance,
quero que o sistema leia minha fatura enviada,
para obter as informações dos gastos sem precisar registrar tudo manualmente.

Relacionamento: RF009

US08 — Identificar pagamentos recorrentes

Como usuário da UPFinance,
quero que o sistema identifique pagamentos recorrentes no meu histórico,
para acompanhar contas que se repetem ao longo do tempo.

Relacionamento: RF010

US09 — Receber alerta de recorrência

Como usuário da UPFinance,
quero ser alertado sobre pagamentos recorrentes identificados,
para acompanhar seus vencimentos.

Relacionamento: RF011

# 10 - Critérios de Aceitação

Os critérios de aceitação determinam as condições que precisam ser atendidas para que uma história de usuário seja considerada concluída.

US01 — Registrar movimentação

Critérios de aceitação:

O usuário deve conseguir registrar uma entrada.
O usuário deve conseguir registrar uma saída.
A movimentação deve possuir descrição, valor, tipo e categoria.
A movimentação registrada deve ficar disponível para consulta.
US02 — Categorizar gasto

Critérios de aceitação:

O usuário deve conseguir selecionar uma categoria disponibilizada pelo sistema.
A categoria selecionada deve estar associada a um dos pilares.
O gasto deve ser contabilizado no pilar correspondente.
US03 — Visualizar gastos

Critérios de aceitação:

O sistema deve apresentar as movimentações registradas.
O usuário deve conseguir identificar os valores e categorias das movimentações.
As informações apresentadas devem corresponder aos registros realizados.
US04 — Analisar distribuição financeira

Critérios de aceitação:

O sistema deve calcular a distribuição dos gastos entre os três pilares.
O sistema deve utilizar os percentuais 50%, 30% e 20%.
O sistema deve apresentar uma interpretação da situação financeira.
A interpretação deve ser baseada nos dados registrados pelo usuário.
US05 — Receber alerta de limite

Critérios de aceitação:

O sistema deve calcular o limite de cada pilar com base na renda.
O sistema deve identificar quando um pilar ultrapassar seu limite.
O sistema deve informar o usuário sobre o limite excedido.
O limite deve respeitar os percentuais fixos da regra 50-30-20.
US06 — Importar fatura

Critérios de aceitação:

O usuário deve conseguir enviar uma fatura em formato PDF.
O sistema deve receber o arquivo enviado.
A fatura deve ser encaminhada para leitura e interpretação.
US07 — Interpretar fatura

Critérios de aceitação:

O sistema deve realizar a leitura das informações presentes na fatura.
Os gastos identificados devem poder ser utilizados no controle financeiro.
O sistema deve considerar os formatos de fatura contemplados pelo projeto.

Observação: a leitura de diferentes formatos de PDF é uma incerteza identificada no projeto e deverá ser validada durante o desenvolvimento.

US08 — Identificar pagamentos recorrentes

Critérios de aceitação:

O sistema deve analisar o histórico de movimentações.
Deve identificar movimentações que apresentem recorrência.
Pagamentos como água, luz e internet podem ser identificados como exemplos de recorrência.
US09 — Receber alerta de recorrência

Critérios de aceitação:

O sistema deve informar quando identificar um pagamento recorrente.
O alerta deve estar relacionado a uma recorrência identificada no histórico.

# 11 - Product Backlog

O Product Backlog organiza as histórias de usuário que serão desenvolvidas, priorizando as necessidades mais importantes para o produto.

ID	História de usuário	Prioridade	Requisito relacionado
US01	Registrar movimentação	Alta	RF001
US02	Categorizar gasto	Alta	RF002/RF003
US04	Analisar distribuição financeira	Alta	RF005/RF006
US05	Receber alerta de limite	Alta	RF007
US03	Visualizar gastos	Alta	RF004
US06	Importar fatura	Média	RF008
US07	Interpretar fatura	Média	RF009
US08	Identificar pagamentos recorrentes	Média	RF010
US09	Receber alerta de recorrência	Média	RF011

A priorização considera as necessidades já identificadas no Documento de Visão: compreender a distribuição dos gastos e reduzir o esforço de controle são necessidades de alta prioridade, enquanto a redução do esforço com gastos do cartão e o acompanhamento de pagamentos recorrentes foram classificados como prioridades médias.

# 12 - Rastreabilidade

A rastreabilidade permite relacionar as necessidades dos usuários aos requisitos e, posteriormente, às histórias de usuário e aos critérios de aceitação.

| Necessidade | Requisito | User Story | Critério de aceitação |
| --- | --- | --- | --- |
| Reduzir esforço de controle | RF001 | US01 | Movimentação cadastrada |
| Organizar gastos | RF002/RF003 | US02 | Categoria associada ao pilar |
| Visualizar situação financeira | RF004/RF005 | US03/US04 | Gastos e distribuição apresentados |
| Compreender distribuição | RF006 | US04 | Interpretação 50-30-20 |
| Ser informado sobre excessos | RF007 | US05 | Alerta de limite excedido |
| Reduzir esforço com cartão | RF008/RF009 | US06/US07 | Fatura enviada e interpretada |
| Acompanhar recorrências | RF010/RF011 | US08/US09 | Recorrência identificada e alerta emitido |
Dessa forma, cada necessidade identificada pode ser relacionada a uma funcionalidade e posteriormente validada por meio de critérios de aceitação.

# 13 - Como garantir qualidade dos requisitos

Para garantir que os requisitos da UPFinance sejam claros, completos, consistentes, verificáveis e rastreáveis, serão adotados os seguintes critérios:

Clareza: cada requisito deve apresentar uma única interpretação possível.

Completude: os requisitos devem contemplar as principais necessidades identificadas para o usuário.

Consistência: os requisitos não devem entrar em conflito entre si ou com as regras de negócio do produto.

Verificabilidade: cada requisito deve possuir uma forma de verificar se foi atendido, utilizando testes ou critérios de aceitação.

Rastreabilidade: cada requisito deve estar relacionado a uma necessidade, história de usuário e critério de aceitação.

Aderência ao escopo: os requisitos devem respeitar as limitações definidas para a primeira versão da UPFinance.

Um exemplo é a regra 50-30-20: ela deve permanecer fixa nesta versão e não poderá ser personalizada pelo usuário. Da mesma forma, não fazem parte do escopo inicial integrações automáticas com bancos ou cartões, realização de pagamentos ou transferências e integração com serviços de LLM.

# 14 - Conclusão

A Sprint 2 estruturou os principais requisitos da UPFinance a partir das necessidades identificadas para o usuário. Os requisitos funcionais definem as capacidades que o sistema deverá oferecer, enquanto os requisitos não funcionais estabelecem características e condições gerais da aplicação.

As histórias de usuário transformam essas necessidades em objetivos compreensíveis do ponto de vista do usuário, enquanto os critérios de aceitação permitem verificar se cada história foi corretamente implementada.

O backlog organiza essas histórias por prioridade e a matriz de rastreabilidade estabelece uma ligação entre necessidades, requisitos, histórias e critérios de aceitação. Dessa forma, o processo de elicitação proporciona uma base para as próximas etapas do desenvolvimento da UPFinance, mantendo os requisitos alinhados ao problema e ao escopo definidos para o produto.
