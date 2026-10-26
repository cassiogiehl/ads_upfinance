
# 1. Objetivo da Sprint
---------------------

A Sprint 3 tem como objetivo refinar os requisitos funcionais da **UPFinance** por meio da modelagem de casos de uso da UML e da especificação detalhada das interações esperadas entre o usuário e o sistema.
Os casos de uso foram derivados dos requisitos funcionais de alto nível definidos no Documento de Visão do Produto, que contemplam cadastro de movimentações, categorização, visualização, análise segundo a regra 50-30-20, alertas, leitura de faturas em PDF e identificação de pagamentos recorrentes.

* * *

# 2. Identificação dos atores
===========================

2.1 Ator principal — Usuário
----------------------------

O **Usuário** é o único ator diretamente identificado no escopo atual da UPFinance.
É a pessoa que utiliza a aplicação para registrar e acompanhar suas informações financeiras, visualizar a distribuição dos gastos e receber as interpretações e alertas gerados pelo sistema.
O usuário pode:
*   cadastrar entradas e saídas;
*   categorizar movimentações;
*   visualizar seus gastos;
*   consultar a distribuição financeira;
*   consultar a interpretação baseada na regra 50-30-20;
*   receber alertas de limite;
*   enviar uma fatura de cartão em PDF;
*   receber informações provenientes da interpretação da fatura;
*   receber alertas sobre pagamentos recorrentes.

2.2 Atores externos
-------------------

Não foram definidos atores externos nesta versão.
A UPFinance não possui, no escopo atual, integração automática com bancos, cartões ou serviços de LLM.

* * *

# 3. Casos de uso identificados
=============================

| ID | Caso de Uso | Objetivo | RF relacionado |
| --- | --- | --- | --- |
| UC01 | Cadastrar movimentação | Registrar uma entrada ou saída | RF001 |
| UC02 | Categorizar movimentação | Associar uma movimentação a uma categoria | RF002 / RF003 |
| UC03 | Visualizar movimentações | Consultar os registros financeiros | RF004 |
| UC04 | Apresentar distribuição 50-30-20 | Apresentar a distribuição dos gastos nos pilares | RF005 |
| UC05 | Interpretar situação financeira | Interpretar a situação financeira segundo a regra | RF006 |
| UC06 | Emitir alerta de limite | Informar que um pilar ultrapassou seu limite | RF007 |
| UC07 | Enviar fatura do cartão | Permitir o envio de uma fatura PDF | RF008 |
| UC08 | Interpretar fatura do cartão | Ler e interpretar os dados da fatura | RF009 |
| UC09 | Identificar pagamentos recorrentes | Identificar recorrências no histórico | RF010 |
| UC10 | Emitir alerta de pagamento recorrente | Informar o usuário sobre recorrências identificadas | RF011 |

Os dez casos de uso correspondem aos onze requisitos funcionais porque o cadastro e a categorização de uma movimentação são tratados como etapas relacionadas do mesmo processo de registro.

* * *

# 4. Diagrama de Casos de Uso UML
===============================

O diagrama representa o comportamento funcional esperado da UPFinance e os relacionamentos entre o ator e os casos de uso. O original utiliza `include` para comportamentos obrigatórios e `extend` para o alerta condicional de limite. Pasted text

![Screenshot From 2026-10-06 07-19-35.png](/.attachments/Screenshot%20From%202026-10-06%2007-19-35-226271d6-a9c6-4aa4-8efc-5a023f17ed9b.png)

4.1 Interpretação dos relacionamentos
-------------------------------------

| Origem | Relacionamento | Destino | Interpretação |
| --- | --- | --- | --- |
| UC01 | `<<include>>` | UC02 | Ao cadastrar uma movimentação, sua categorização faz parte do processo de organização da informação. |
| UC05 | `<<include>>` | UC04 | A interpretação da situação financeira utiliza a distribuição dos gastos entre os pilares como base para a análise. |
| UC06 | `<<extend>>` | UC05 | O alerta ocorre somente quando os gastos ultrapassam o limite correspondente. |
| UC07 | `<<include>>` | UC08 | Quando o usuário envia uma fatura em PDF, o sistema realiza sua leitura e interpretação. |
| UC09 | `<<include>>` | UC10 | Após identificar uma recorrência, o sistema alerta o usuário sobre o pagamento recorrente. |

* * *

# 5. Especificação dos Casos de Uso
=================================

UC01 — Cadastrar movimentação
-----------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Permitir que o usuário registre uma movimentação financeira de entrada ou saída. |
| **Ator principal** | Usuário |
| **Pré-condições** | O usuário deve estar utilizando a aplicação; os dados necessários para o registro devem estar disponíveis. |
| **Pós-condições** | A movimentação é registrada, fica disponível para consulta e pode ser associada a uma categoria. |
| **Regras de negócio** | RN002 e RN003 |
| **Requisito relacionado** | RF001 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O usuário acessa a opção de cadastro de movimentação. |
| 2 | O sistema solicita os dados da movimentação. |
| 3 | O usuário informa a descrição. |
| 4 | O usuário informa o valor. |
| 5 | O usuário informa o tipo da movimentação: entrada ou saída. |
| 6 | O usuário seleciona uma categoria. |
| 7 | O sistema associa a categoria ao respectivo pilar. |
| 8 | O sistema registra a movimentação. |
| 9 | O sistema disponibiliza a movimentação para consulta. |

### Fluxos alternativos

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Dados incompletos | O sistema não conclui o cadastro e solicita o preenchimento das informações necessárias. |
| FA02 | Valor inválido | O sistema identifica a inconsistência e solicita a correção do valor. |

* * *

UC02 — Categorizar movimentação
-------------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Associar uma movimentação financeira a uma categoria disponibilizada pelo sistema. |
| **Ator principal** | Usuário |
| **Pré-condições** | Deve existir uma movimentação a ser categorizada e as categorias devem estar disponíveis. |
| **Pós-condições** | A movimentação possui uma categoria e esta determina o pilar correspondente. |
| **Regra de negócio** | RN002 |
| **Requisitos relacionados** | RF002 e RF003 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O usuário seleciona uma movimentação. |
| 2 | O sistema apresenta as categorias disponíveis. |
| 3 | O usuário seleciona uma categoria. |
| 4 | O sistema identifica o pilar associado à categoria. |
| 5 | O sistema registra a categorização. |

### Fluxo alternativo

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Categoria não selecionada | O sistema solicita a seleção de uma categoria antes da conclusão da categorização. |

* * *

UC03 — Visualizar movimentações
-------------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Permitir que o usuário consulte suas movimentações financeiras registradas. |
| **Ator principal** | Usuário |
| **Pré-condições** | Devem existir movimentações cadastradas para exibição. |
| **Pós-condições** | O usuário visualiza as movimentações registradas. |
| **Requisito relacionado** | RF004 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O usuário acessa a área de movimentações. |
| 2 | O sistema consulta os registros existentes. |
| 3 | O sistema apresenta as movimentações. |
| 4 | O usuário visualiza descrição, valor, tipo e categoria. |

### Fluxo alternativo

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Nenhuma movimentação registrada | O sistema informa que não há movimentações cadastradas. |

* * *

UC04 — Apresentar distribuição 50-30-20
---------------------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Apresentar a distribuição dos gastos entre os pilares Essencial, Pessoal e Futuro. |
| **Ator principal** | Usuário |
| **Pré-condições** | Devem existir informações financeiras e a renda utilizada nos cálculos deve estar disponível. |
| **Pós-condições** | A distribuição dos gastos é apresentada ao usuário. |
| **Regras de negócio** | RN001 e RN004 |
| **Requisito relacionado** | RF005 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O usuário acessa a análise financeira. |
| 2 | O sistema consulta as movimentações registradas. |
| 3 | O sistema identifica o pilar associado a cada categoria. |
| 4 | O sistema totaliza os gastos de cada pilar. |
| 5 | O sistema compara os valores com a distribuição 50-30-20. |
| 6 | O sistema apresenta a distribuição ao usuário. |

### Fluxo alternativo

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Ausência de movimentações | O sistema informa que são necessários registros financeiros para realizar uma análise completa. |

* * *

UC05 — Interpretar situação financeira
--------------------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Apresentar uma interpretação da situação financeira baseada na distribuição 50-30-20. |
| **Ator principal** | Usuário |
| **Pré-condições** | Devem existir dados financeiros, a distribuição deve poder ser calculada e a renda deve estar disponível. |
| **Pós-condições** | O usuário recebe uma interpretação da sua situação financeira. |
| **Regras de negócio** | RN001, RN003 e RN004 |
| **Requisito relacionado** | RF006 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O usuário solicita a análise financeira. |
| 2 | O sistema obtém os valores registrados. |
| 3 | O sistema classifica os gastos de acordo com seus pilares. |
| 4 | O sistema calcula a distribuição dos gastos. |
| 5 | O sistema compara a distribuição com a regra 50-30-20. |
| 6 | O sistema identifica a situação de cada pilar. |
| 7 | O sistema apresenta a interpretação ao usuário. |

### Fluxos alternativos

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Pilar dentro do limite | O sistema apresenta o pilar como dentro do limite. |
| FA02 | Pilar acima do limite | O sistema classifica o limite como excedido e permite a emissão do alerta correspondente. |

* * *

UC06 — Emitir alerta de limite
------------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Informar o usuário quando os gastos de um pilar ultrapassarem o limite estabelecido. |
| **Ator principal** | Usuário |
| **Pré-condições** | Gastos registrados, renda disponível e distribuição calculada. |
| **Pós-condições** | O usuário é informado sobre o pilar que ultrapassou seu limite. |
| **Regra de negócio** | RN003 |
| **Requisito relacionado** | RF007 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O sistema calcula o limite de cada pilar. |
| 2 | O sistema compara os gastos com seus limites. |
| 3 | O sistema identifica um limite ultrapassado. |
| 4 | O sistema gera o alerta. |
| 5 | O usuário recebe a informação. |

### Fluxo alternativo

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Nenhum limite excedido | Nenhum alerta é emitido. |

* * *

UC07 — Enviar fatura do cartão
------------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Permitir o envio de uma fatura de cartão de crédito em PDF. |
| **Ator principal** | Usuário |
| **Pré-condições** | O usuário deve possuir uma fatura em formato PDF. |
| **Pós-condições** | O arquivo é recebido e disponibilizado para interpretação. |
| **Requisito relacionado** | RF008 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O usuário acessa a opção de envio da fatura. |
| 2 | O usuário seleciona o arquivo PDF. |
| 3 | O sistema recebe o arquivo. |
| 4 | O sistema verifica o arquivo enviado. |
| 5 | O sistema encaminha a fatura para interpretação. |

### Fluxo alternativo

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Arquivo incompatível | O sistema solicita o envio de uma fatura em formato PDF. |

* * *

UC08 — Interpretar fatura do cartão
-----------------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Ler e interpretar as informações presentes na fatura PDF. |
| **Ator principal** | Usuário |
| **Pré-condições** | Uma fatura PDF deve ter sido enviada. |
| **Pós-condições** | As informações identificadas ficam disponíveis para o controle financeiro. |
| **Requisito relacionado** | RF009 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O sistema recebe a fatura. |
| 2 | O sistema realiza a leitura do arquivo. |
| 3 | O sistema identifica as informações dos gastos. |
| 4 | O sistema interpreta os dados encontrados. |
| 5 | O sistema disponibiliza as informações para o controle financeiro. |

### Fluxo alternativo

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Formato não interpretado | O sistema informa que a fatura não pôde ser interpretada. |

> **Risco:** a interpretação de diferentes formatos de fatura PDF é uma incerteza identificada no projeto e deverá ser validada durante o desenvolvimento.

* * *

UC09 — Identificar pagamentos recorrentes
-----------------------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Identificar pagamentos que ocorrem repetidamente no histórico financeiro. |
| **Ator principal** | Usuário |
| **Pré-condições** | Devem existir movimentações registradas no histórico. |
| **Pós-condições** | Pagamentos recorrentes são identificados pelo sistema. |
| **Requisito relacionado** | RF010 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O sistema consulta o histórico de movimentações. |
| 2 | O sistema analisa as movimentações registradas. |
| 3 | O sistema identifica padrões de repetição. |
| 4 | O sistema identifica os pagamentos recorrentes. |
| 5 | O sistema registra a identificação da recorrência. |

### Fluxo alternativo

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Nenhuma recorrência identificada | O sistema não gera identificação de pagamento recorrente. |

Exemplos previstos no glossário: contas de água, luz e internet.

* * *

UC10 — Emitir alerta de pagamento recorrente
--------------------------------------------

| Campo | Especificação |
| --- | --- |
| **Objetivo** | Informar o usuário sobre pagamentos recorrentes identificados no histórico. |
| **Ator principal** | Usuário |
| **Pré-condições** | O sistema deve ter identificado um pagamento recorrente. |
| **Pós-condições** | O usuário é informado sobre o pagamento recorrente. |
| **Requisito relacionado** | RF011 |

### Fluxo principal

| Passo | Ação |
| --- | --- |
| 1 | O sistema identifica um pagamento recorrente. |
| 2 | O sistema gera um alerta relacionado à recorrência. |
| 3 | O sistema apresenta o alerta ao usuário. |
| 4 | O usuário visualiza a informação. |

### Fluxo alternativo

| ID | Situação | Comportamento |
| --- | --- | --- |
| FA01 | Nenhum pagamento recorrente | Nenhum alerta é emitido. |

* * *

# 6. Regras de negócio
====================

| ID | Regra | Descrição |
| --- | --- | --- |
| **RN001** | Distribuição 50-30-20 | 50% da renda para gastos Essenciais, 30% para gastos Pessoais e 20% para o Futuro. |
| **RN002** | Associação de categorias | Cada categoria deve estar previamente associada a Essencial, Pessoal ou Futuro. |
| **RN003** | Limite dos pilares | Os limites são calculados em relação à renda. Ao ultrapassar o percentual correspondente, o limite é considerado excedido. |
| **RN004** | Percentuais fixos | A distribuição 50-30-20 permanecerá fixa na primeira versão. |

* * *

# 7. Matriz de rastreabilidade dos casos de uso
=============================================

| Requisito | Caso de uso | Necessidade atendida |
| --- | --- | --- |
| RF001 | UC01 | Reduzir o esforço manual de controle |
| RF002 | UC02 | Organizar os gastos |
| RF003 | UC02 | Organizar gastos nos pilares |
| RF004 | UC03 | Visualizar gastos registrados |
| RF005 | UC04 | Visualizar distribuição financeira |
| RF006 | UC05 | Compreender a situação financeira |
| RF007 | UC06 | Ser informado sobre limites excedidos |
| RF008 | UC07 | Reduzir esforço com gastos do cartão |
| RF009 | UC08 | Interpretar gastos da fatura |
| RF010 | UC09 | Acompanhar pagamentos recorrentes |
| RF011 | UC10 | Receber alertas sobre recorrências |

Essa rastreabilidade mantém a ligação entre o que foi identificado na elicitação, o requisito funcional e o comportamento esperado do sistema. Pasted text

* * *

# 8. Consistência do modelo
=========================

O modelo de casos de uso foi elaborado seguindo quatro princípios:
1.  **Um ator principal:** o usuário é o único ator diretamente envolvido nesta versão.
2.  **Casos de uso derivados dos requisitos:** cada funcionalidade representada possui correspondência com os requisitos funcionais.
3.  **Relacionamentos com significado funcional:** `<<include>>` representa comportamento obrigatório de outro fluxo, enquanto `<<extend>>` representa o comportamento condicional do alerta de limite.
4.  **Respeito ao escopo:** não foram incluídos pagamentos, transferências, integração bancária automática ou serviços de LLM.

* * *

# 9. Resultado da Sprint 3
========================

Ao final da Sprint 3, a UPFinance possui:
*   identificação do ator principal;
*   identificação dos casos de uso;
*   relacionamento entre ator e casos de uso;
*   relacionamentos `<<include>>` e `<<extend>>`;
*   especificação dos fluxos principais;
*   especificação dos fluxos alternativos;
*   pré-condições;
*   pós-condições;
*   regras de negócio;
*   requisitos relacionados;
*   matriz de rastreabilidade.
O refinamento transforma os requisitos funcionais de alto nível em uma representação mais detalhada do comportamento esperado da UPFinance, criando uma base para as próximas etapas de especificação e desenvolvimento
