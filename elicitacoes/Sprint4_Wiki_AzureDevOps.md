# Sprint 4 - Diagramas de Atividades e Diagrama de Classes (UML)

## 1. Objetivo da Sprint

A Sprint 4 tem como objetivo aprofundar a modelagem da UPFinance em duas perspectivas complementares da UML:

- **Comportamental (dinâmica):** diagramas de atividades que representam o fluxo de trabalho dos casos de uso especificados na Sprint 3, incluindo decisões, fluxos alternativos, paralelismo e fluxo de objetos.
- **Estrutural (estática):** diagrama de classes que representa os conceitos do domínio da UPFinance, seus atributos, operações e relacionamentos.

Os diagramas foram derivados diretamente dos requisitos funcionais (Sprint 2) e da especificação dos casos de uso (Sprint 3), mantendo a rastreabilidade RF → UC → Diagrama de Atividades → Classes.

---

## 2. Diagramas de Atividades

> **Legenda dos diagramas (Mermaid):** círculo preto = estado inicial; círculo preto com borda grossa = estado final; losango = decisão/merge; caixa preta *fork*/*join* = bifurcação/união; retângulo reto = objeto ou «datastore»; seta tracejada = fluxo de objeto; blocos *Usuário* e *Sistema UPFinance* = raias (swimlanes).

### 2.1 Critério de agrupamento

Os dez casos de uso foram agrupados em quatro diagramas de atividades, seguindo os relacionamentos `<<include>>` e `<<extend>>` definidos na Sprint 3. Casos de uso que sempre ocorrem juntos são representados no mesmo fluxo.

| ID | Diagrama de atividades | Casos de uso | Requisitos | Regras de negócio |
|---|---|---|---|---|
| AD01 | Cadastrar e categorizar movimentação | UC01, UC02 | RF001, RF002, RF003 | RN002 |
| AD02 | Analisar situação financeira 50-30-20 | UC04, UC05, UC06 | RF005, RF006, RF007 | RN001, RN003, RN004 |
| AD03 | Enviar e interpretar fatura do cartão | UC07, UC08 | RF008, RF009 | — |
| AD04 | Identificar pagamentos recorrentes e alertar | UC09, UC10 | RF010, RF011 | — |

O UC03 (Visualizar movimentações) não recebeu diagrama próprio por ser um fluxo linear de consulta (acessar → consultar → apresentar), sem decisões relevantes além do FA01, que já está coberto pela especificação textual.

### 2.2 Elementos utilizados

| Elemento | Notação | Uso na UPFinance |
|---|---|---|
| Estado inicial / final | ● / ◉ | Início e término de cada fluxo |
| Atividade | Retângulo arredondado | Ações do usuário ou do sistema |
| Decisão / Merge | Losango | Validação de dados, limite excedido, formato da fatura |
| Condição de guarda | `[texto]` | `[valor inválido]`, `[algum pilar > limite]` |
| Fork / Join | Barra preta | Totalização paralela dos três pilares (AD02) |
| Raias (swimlanes) | Partições | **Usuário** e **Sistema UPFinance** |
| Objeto | Retângulo | `Movimentacao`, `Fatura`, `AnaliseFinanceira`, `PagamentoRecorrente` |
| Datastore | `«datastore»` | Base de movimentações |
| Concorrência dinâmica | `*` | "Identificar gastos *" e "Analisar grupo *" (repetição por item) |

---

### 2.3 AD01 — Cadastrar e categorizar movimentação

::: mermaid
graph TD;
subgraph U1 ["Usuário"];
ini((" "));
a1("Acessar opção de<br/>cadastro de movimentação");
a3("Informar descrição,<br/>valor e tipo (entrada / saída)");
a4("Selecionar categoria");
a9("Corrigir / completar os dados");
end;
subgraph S1 ["Sistema UPFinance"];
a2("Apresentar formulário<br/>e categorias disponíveis");
m1{" "};
d1{" "};
d2{" "};
msg("Informar inconsistência<br/>(FA01 / FA02)");
a5("Identificar o pilar associado<br/>à categoria (RN002)");
a6("Registrar movimentação");
o1["m : Movimentacao"];
ds["«datastore»<br/>Movimentações"];
a7("Disponibilizar movimentação<br/>para consulta");
fim((" "));
end;
ini --> a1 --> a2 --> a3 --> a4 --> m1 --> d1;
d1 -->|"[dados incompletos]"| msg;
d1 -->|"[dados completos]"| d2;
d2 -->|"[valor inválido]"| msg;
d2 -->|"[valor > 0]"| a5;
msg --> a9 --> m1;
a5 --> a6;
a6 -.-> o1 -.-> ds;
a6 --> a7 --> fim;
classDef inicio fill:#000,stroke:#000;
classDef final fill:#000,stroke:#888,stroke-width:5px;
classDef objeto fill:#fff,stroke:#333;
class ini inicio;
class fim final;
class o1,ds objeto;
:::

**Descrição do fluxo:**

1. O usuário acessa a opção de cadastro; o sistema apresenta o formulário e as categorias disponíveis.
2. O usuário informa descrição, valor e tipo (entrada/saída) e seleciona uma categoria.
3. O sistema valida os dados:
   - `[dados incompletos]` → FA01 do UC01: o sistema informa a inconsistência e o usuário corrige.
   - `[valor inválido]` → FA02 do UC01: o sistema solicita a correção do valor.
4. Com dados válidos, o sistema identifica o pilar associado à categoria (RN002), registra a movimentação (objeto `m : Movimentacao` persistido no datastore) e a disponibiliza para consulta.

O nó de merge antes da validação permite que o fluxo retorne ao ponto de verificação após a correção, formando um laço até que os dados sejam válidos. A categorização (UC02) aparece dentro do fluxo porque o UC01 a inclui (`<<include>>`).

---

### 2.4 AD02 — Analisar situação financeira 50-30-20

::: mermaid
graph TD;
subgraph U2 ["Usuário"];
ini((" "));
u1("Solicitar análise financeira");
u4("Visualizar aviso de<br/>dados insuficientes");
u3("Visualizar alerta de limite");
u2("Visualizar distribuição<br/>e interpretação");
end;
subgraph S2 ["Sistema UPFinance"];
ds["«datastore»<br/>Movimentações"];
s1("Consultar movimentações<br/>do período");
d1{" "};
s7("Informar que são necessários<br/>registros (FA01 UC04)");
s2("Calcular renda do período<br/>(soma das entradas)");
s3("Classificar saídas por pilar<br/>(categoria → pilar, RN002)");
fk["fork"];
pE("Totalizar Essencial<br/>limite = 50% da renda");
pP("Totalizar Pessoal<br/>limite = 30% da renda");
pF("Totalizar Futuro<br/>limite = 20% da renda");
jn["join"];
s4("Comparar total × limite<br/>de cada pilar (RN001, RN003)");
obj["a : AnaliseFinanceira"];
d2{" "};
s5("Gerar alerta de limite para<br/>o(s) pilar(es) excedido(s) — UC06");
m1{" "};
s6("Montar interpretação<br/>determinística");
fim((" "));
end;
ini --> u1 --> s1;
ds -.-> s1;
s1 --> d1;
d1 -->|"[sem movimentações ou renda = 0]"| s7;
s7 --> u4 --> fim;
d1 -->|"[há entradas e saídas]"| s2;
s2 --> s3 --> fk;
fk --> pE;
fk --> pP;
fk --> pF;
pE --> jn;
pP --> jn;
pF --> jn;
jn --> s4;
s4 -.-> obj;
s4 --> d2;
d2 -->|"[algum pilar > limite]"| s5;
d2 -->|"[todos dentro do limite]"| m1;
s5 --> u3 --> m1;
m1 --> s6 --> u2 --> fim;
classDef inicio fill:#000,stroke:#000;
classDef final fill:#000,stroke:#888,stroke-width:5px;
classDef barra fill:#000,stroke:#000,color:#fff;
classDef objeto fill:#fff,stroke:#333;
class ini inicio;
class fim final;
class fk,jn barra;
class obj,ds objeto;
:::

**Descrição do fluxo:**

1. O usuário solicita a análise; o sistema consulta as movimentações do período.
2. Decisão:
   - `[sem movimentações ou renda = 0]` → FA01 do UC04: o sistema informa que são necessários registros.
   - `[há entradas e saídas]` → segue a análise.
3. O sistema calcula a renda do período e classifica as saídas por pilar.
4. **Fork:** a totalização dos pilares Essencial (50%), Pessoal (30%) e Futuro (20%) ocorre de forma independente; o **join** sincroniza os três resultados antes da comparação.
5. O sistema compara total × limite de cada pilar (RN001, RN003), produzindo o objeto `a : AnaliseFinanceira`.
6. Decisão:
   - `[algum pilar > limite]` → o sistema gera o alerta de limite (UC06, comportamento condicional do `<<extend>>`) e o usuário o visualiza.
   - `[todos dentro do limite]` → nenhum alerta é emitido (FA01 do UC06).
7. Os caminhos se reúnem (merge), o sistema monta a interpretação determinística (sem LLM, conforme escopo) e o usuário visualiza a distribuição e a interpretação.

O `<<extend>>` do UC06 aparece como o ramo condicional da decisão, e o `<<include>>` do UC05 sobre o UC04 aparece como o cálculo da distribuição sendo pré-requisito da interpretação.

---

### 2.5 AD03 — Enviar e interpretar fatura do cartão

::: mermaid
graph TD;
subgraph U3 ["Usuário"];
ini((" "));
u1("Acessar opção de<br/>envio de fatura");
u2("Selecionar arquivo");
u3("Revisar gastos identificados");
u4("Ajustar categorias<br/>(se necessário)");
end;
subgraph S3 ["Sistema UPFinance"];
m0{" "};
s1("Receber e verificar arquivo");
of["f : Fatura"];
d1{" "};
sE1("Solicitar envio em PDF<br/>(FA01 UC07)");
s2("Ler conteúdo do PDF");
d2{" "};
sE2("Informar que a fatura não pôde<br/>ser interpretada (FA01 UC08)");
fim2((" "));
s3("Identificar gastos *<br/>(data, descrição, valor)");
s4("Sugerir categoria<br/>para cada gasto");
s5("Registrar gastos como<br/>movimentações de saída");
ds["«datastore»<br/>Movimentações"];
fim((" "));
end;
ini --> u1 --> m0 --> u2 --> s1 --> d1;
s1 -.-> of;
of -.-> s2;
d1 -->|"[não é PDF]"| sE1;
sE1 --> m0;
d1 -->|"[PDF válido]"| s2;
s2 --> d2;
d2 -->|"[formato não reconhecido]"| sE2;
sE2 --> fim2;
d2 -->|"[formato reconhecido]"| s3;
s3 --> s4 --> u3 --> u4 --> s5;
s5 -.-> ds;
s5 --> fim;
classDef inicio fill:#000,stroke:#000;
classDef final fill:#000,stroke:#888,stroke-width:5px;
classDef objeto fill:#fff,stroke:#333;
class ini inicio;
class fim,fim2 final;
class of,ds objeto;
:::

**Descrição do fluxo:**

1. O usuário acessa a opção de envio e seleciona o arquivo.
2. O sistema recebe e verifica o arquivo, criando o objeto `f : Fatura`:
   - `[não é PDF]` → FA01 do UC07: o sistema solicita o envio em PDF e o fluxo retorna à seleção do arquivo.
   - `[PDF válido]` → leitura do conteúdo.
3. Decisão sobre o formato:
   - `[formato não reconhecido]` → FA01 do UC08: o sistema informa que a fatura não pôde ser interpretada e o fluxo termina.
   - `[formato reconhecido]` → o sistema identifica cada gasto (concorrência dinâmica `*`) e sugere uma categoria.
4. O usuário revisa os gastos e ajusta categorias se necessário.
5. O sistema registra os gastos como movimentações de saída.

O passo de revisão pelo usuário trata o risco identificado na Sprint 2 sobre a variedade de formatos de fatura: a interpretação é automática, mas o usuário confirma o resultado antes do registro.

---

### 2.6 AD04 — Identificar pagamentos recorrentes e alertar

::: mermaid
graph TD;
subgraph S4 ["Sistema UPFinance"];
ini((" "));
ds["«datastore»<br/>Movimentações"];
s1("Consultar histórico de<br/>movimentações de saída");
s2("Agrupar saídas por<br/>descrição semelhante");
s3("Analisar grupo *<br/>(intervalo entre datas e valor)");
d1{" "};
s4("Registrar pagamento recorrente<br/>e próximo vencimento");
op["p : PagamentoRecorrente"];
s5("Gerar alerta de pagamento<br/>recorrente (UC10)");
m1{" "};
d2{" "};
fim((" "));
end;
subgraph U4 ["Usuário"];
u1("Visualizar alerta de<br/>pagamento recorrente");
end;
ini --> s1;
ds -.-> s1;
s1 --> s2 --> s3 --> d1;
d1 -->|"[≥ 2 ocorrências em intervalo regular]"| s4;
d1 -->|"[sem padrão (FA01 UC09)]"| m1;
s4 -.-> op;
s4 --> s5 --> u1 --> m1;
m1 --> d2;
d2 -->|"[há grupos a analisar]"| s3;
d2 -->|"[todos os grupos analisados]"| fim;
classDef inicio fill:#000,stroke:#000;
classDef final fill:#000,stroke:#888,stroke-width:5px;
classDef objeto fill:#fff,stroke:#333;
class ini inicio;
class fim final;
class op,ds objeto;
:::

**Descrição do fluxo:**

1. O sistema consulta o histórico de movimentações de saída e agrupa as saídas por descrição semelhante.
2. Para cada grupo (concorrência dinâmica `*`), analisa intervalo entre datas e valor:
   - `[≥ 2 ocorrências em intervalo regular]` → registra o pagamento recorrente e o próximo vencimento (objeto `p : PagamentoRecorrente`), gera o alerta (UC10) e o usuário o visualiza.
   - `[sem padrão]` → FA01 do UC09: nenhuma recorrência é registrada.
3. O laço continua enquanto `[há grupos a analisar]` e termina quando `[todos os grupos analisados]`.

Exemplos esperados de recorrência, conforme o glossário: contas de água, luz e internet.

---

## 3. Diagrama de Classes

### 3.1 Identificação das classes

As classes foram identificadas a partir dos substantivos presentes nos requisitos, nas regras de negócio e nos objetos que aparecem nos diagramas de atividades.

| Classe | Origem | Responsabilidade |
|---|---|---|
| `Usuario` | Ator principal (Sprint 3) | Possui movimentações, faturas, recorrências e recebe alertas |
| `Movimentacao` | RF001 | Entrada ou saída financeira (descrição, valor, data, tipo) |
| `Categoria` | RF002, RN002 | Classificação da movimentação, associada a um pilar |
| `Pilar` «enumeration» | RF003, RN001, RN004 | Essencial (50%), Pessoal (30%), Futuro (20%) — percentuais fixos |
| `TipoMovimentacao` «enumeration» | RF001 | ENTRADA / SAIDA |
| `Fatura` | RF008 | Arquivo PDF enviado e seu status de interpretação |
| `StatusFatura` «enumeration» | RF009 / FA01 UC08 | RECEBIDA, INTERPRETADA, NAO_INTERPRETADA |
| `InterpretadorFatura` «interface» | RF009 | Contrato para leitura de faturas |
| `InterpretadorFaturaPDF` | RF009 | Implementação para os formatos de PDF contemplados |
| `AnaliseFinanceira` | RF005, RF006 | Resultado da análise 50-30-20 de um período |
| `DistribuicaoPilar` | RF005, RN003 | Total gasto, limite e situação de um pilar |
| `Alerta` (abstrata) | RF007, RF011 | Comportamento comum dos alertas |
| `AlertaLimite` | RF007 | Alerta de pilar excedido |
| `AlertaRecorrencia` | RF011 | Alerta de pagamento recorrente |
| `PagamentoRecorrente` | RF010 | Pagamento identificado como recorrente no histórico |
| `IdentificadorRecorrencia` «service» | RF010 | Analisa o histórico e cria pagamentos recorrentes |

### 3.2 Diagrama

::: mermaid
classDiagram
class Usuario {
-Long id
-String nome
-String email
+cadastrarMovimentacao(Movimentacao m) void
+enviarFatura(Arquivo arquivo) Fatura
+solicitarAnalise(Periodo periodo) AnaliseFinanceira
+getMovimentacoes(Periodo periodo) List~Movimentacao~
}
class Movimentacao {
-Long id
-String descricao
-BigDecimal valor
-LocalDate data
-TipoMovimentacao tipo
+categorizar(Categoria c) void
+getPilar() Pilar
+isSaida() boolean
}
class Categoria {
-Long id
-String nome
-Pilar pilar
+getPilar() Pilar
}
class Pilar {
<<enumeration>>
ESSENCIAL = 0.50
PESSOAL = 0.30
FUTURO = 0.20
-BigDecimal percentual
+calcularLimite(BigDecimal renda) BigDecimal
}
class TipoMovimentacao {
<<enumeration>>
ENTRADA
SAIDA
}
class Fatura {
-Long id
-String nomeArquivo
-LocalDate dataEnvio
-StatusFatura status
+marcarInterpretada() void
+marcarFalha(String motivo) void
}
class StatusFatura {
<<enumeration>>
RECEBIDA
INTERPRETADA
NAO_INTERPRETADA
}
class InterpretadorFatura {
<<interface>>
+suporta(Fatura f) boolean
+interpretar(Fatura f) List~Movimentacao~
}
class InterpretadorFaturaPDF {
+suporta(Fatura f) boolean
+interpretar(Fatura f) List~Movimentacao~
}
class AnaliseFinanceira {
-Periodo periodo
-BigDecimal renda
-LocalDateTime dataGeracao
+calcularDistribuicao() void
+getInterpretacao() String
+getPilaresExcedidos() List~Pilar~
}
class DistribuicaoPilar {
-Pilar pilar
-BigDecimal totalGasto
-BigDecimal limite
+getPercentualUtilizado() BigDecimal
+isExcedido() boolean
}
class Alerta {
<<abstract>>
-Long id
-String mensagem
-LocalDateTime dataEmissao
-boolean lido
+marcarComoLido() void
}
class AlertaLimite {
-Pilar pilar
-BigDecimal valorExcedido
}
class AlertaRecorrencia {
-LocalDate proximoVencimento
}
class PagamentoRecorrente {
-Long id
-String descricao
-BigDecimal valorMedio
-int periodicidadeDias
-LocalDate proximoVencimento
+calcularProximoVencimento() LocalDate
}
class IdentificadorRecorrencia {
<<service>>
+identificar(List~Movimentacao~ historico) List~PagamentoRecorrente~
}
Usuario "1" *-- "0..*" Movimentacao : registra
Usuario "1" *-- "0..*" Fatura : envia
Usuario "1" *-- "0..*" PagamentoRecorrente : possui
AnaliseFinanceira "1" *-- "3" DistribuicaoPilar : contém
Usuario "1" --> "0..*" AnaliseFinanceira : solicita
Usuario "1" --> "0..*" Alerta : recebe
Movimentacao "0..*" --> "1" Categoria : classificada em
Fatura "0..1" --> "0..*" Movimentacao : origina
PagamentoRecorrente "0..1" --> "2..*" Movimentacao : baseado em
AnaliseFinanceira "0..*" --> "0..*" Movimentacao : considera
AnaliseFinanceira "1" --> "0..3" AlertaLimite : gera
PagamentoRecorrente "1" --> "0..*" AlertaRecorrencia : gera
Alerta <|-- AlertaLimite
Alerta <|-- AlertaRecorrencia
InterpretadorFatura <|.. InterpretadorFaturaPDF
Categoria ..> Pilar : use
Movimentacao ..> TipoMovimentacao : use
Fatura ..> StatusFatura : use
InterpretadorFatura ..> Fatura : parameter
IdentificadorRecorrencia ..> Movimentacao : parameter
IdentificadorRecorrencia ..> PagamentoRecorrente : create
:::

### 3.3 Relacionamentos

| Origem | Tipo | Destino | Multiplicidade | Justificativa |
|---|---|---|---|---|
| Usuario | Composição | Movimentacao | 1 — 0..* | As movimentações pertencem a um único usuário e não existem sem ele |
| Usuario | Composição | Fatura | 1 — 0..* | A fatura enviada pertence ao usuário |
| Usuario | Composição | PagamentoRecorrente | 1 — 0..* | Recorrências são derivadas do histórico de um usuário |
| AnaliseFinanceira | Composição | DistribuicaoPilar | 1 — 3 | Toda análise contém exatamente uma distribuição por pilar |
| Usuario | Associação | AnaliseFinanceira | 1 — 0..* | O usuário solicita análises por período |
| Usuario | Associação | Alerta | 1 — 0..* | O usuário recebe alertas |
| Movimentacao | Associação | Categoria | 0..* — 1 | Cada movimentação possui exatamente uma categoria (RF002) |
| Fatura | Associação | Movimentacao | 0..1 — 0..* | Uma fatura origina movimentações; uma movimentação manual não tem fatura |
| PagamentoRecorrente | Associação | Movimentacao | 0..1 — 2..* | Recorrência exige no mínimo duas ocorrências |
| AnaliseFinanceira | Associação | Movimentacao | 0..* — 0..* | A análise considera as movimentações do período |
| AnaliseFinanceira | Associação | AlertaLimite | 1 — 0..3 | No máximo um alerta por pilar excedido |
| PagamentoRecorrente | Associação | AlertaRecorrencia | 1 — 0..* | Cada alerta refere-se a uma recorrência |
| AlertaLimite, AlertaRecorrencia | Generalização | Alerta | — | Compartilham mensagem, data de emissão e status de leitura |
| InterpretadorFaturaPDF | Realização | InterpretadorFatura | — | Implementa o contrato de interpretação |
| Categoria | Dependência «use» | Pilar | — | A categoria referencia um pilar fixo (RN002) |
| IdentificadorRecorrencia | Dependência «parameter» | Movimentacao | — | Recebe o histórico como parâmetro |
| IdentificadorRecorrencia | Dependência «create» | PagamentoRecorrente | — | Cria as recorrências identificadas |
| InterpretadorFatura | Dependência «parameter» | Fatura | — | Recebe a fatura a interpretar |

### 3.4 Decisões de modelagem

- **Pilar como enumeração:** como a distribuição 50-30-20 é fixa na primeira versão (RN004), os pilares e seus percentuais são valores constantes, não registros editáveis. Se a personalização entrar no escopo futuro, `Pilar` pode se tornar uma classe.
- **Interface `InterpretadorFatura`:** a variedade de formatos de fatura é uma incerteza do projeto. A interface permite adicionar novos interpretadores (por banco ou layout) sem alterar o restante do sistema.
- **Renda como atributo derivado (`renda`):** a renda de uma análise é calculada como a soma das movimentações de ENTRADA do período, evitando duplicar a informação.
- **Composição vs. associação:** usou-se composição apenas onde o ciclo de vida da parte depende do todo. A relação Fatura → Movimentacao é associação simples, pois as movimentações continuam válidas mesmo que a fatura seja removida.
- **Escopo:** não há classes para integração bancária, pagamentos, transferências ou LLM, respeitando as restrições da primeira versão.

### 3.5 Mapeamento para código (exemplo em Java)

```java
public enum Pilar {
    ESSENCIAL(new BigDecimal("0.50")),
    PESSOAL(new BigDecimal("0.30")),
    FUTURO(new BigDecimal("0.20"));

    private final BigDecimal percentual;
    Pilar(BigDecimal percentual) { this.percentual = percentual; }

    public BigDecimal calcularLimite(BigDecimal renda) {
        return renda.multiply(percentual);           // RN003
    }
}

public class Movimentacao {
    private Long id;
    private String descricao;
    private BigDecimal valor;
    private LocalDate data;
    private TipoMovimentacao tipo;
    private Categoria categoria;                     // associação 0..* — 1

    public Pilar getPilar() { return categoria.getPilar(); }
}

public class Usuario {
    private Long id;
    private String nome;
    private String email;
    private List<Movimentacao> movimentacoes = new ArrayList<>(); // composição
}

public abstract class Alerta {                       // classe abstrata
    private String mensagem;
    private LocalDateTime dataEmissao;
    private boolean lido;
}

public class AlertaLimite extends Alerta {          // generalização
    private Pilar pilar;
    private BigDecimal valorExcedido;
}

public interface InterpretadorFatura {
    boolean suporta(Fatura f);
    List<Movimentacao> interpretar(Fatura f);
}

public class InterpretadorFaturaPDF implements InterpretadorFatura { ... } // realização
```

---

## 4. Rastreabilidade

| Requisito | Caso de uso | Diagrama de atividades | Classes envolvidas |
|---|---|---|---|
| RF001 | UC01 | AD01 | Usuario, Movimentacao, TipoMovimentacao |
| RF002 | UC02 | AD01 | Movimentacao, Categoria |
| RF003 | UC02 | AD01 | Categoria, Pilar |
| RF004 | UC03 | — (fluxo linear) | Usuario, Movimentacao |
| RF005 | UC04 | AD02 | AnaliseFinanceira, DistribuicaoPilar, Pilar |
| RF006 | UC05 | AD02 | AnaliseFinanceira |
| RF007 | UC06 | AD02 | AlertaLimite, Alerta |
| RF008 | UC07 | AD03 | Fatura, StatusFatura |
| RF009 | UC08 | AD03 | InterpretadorFatura, InterpretadorFaturaPDF, Movimentacao |
| RF010 | UC09 | AD04 | IdentificadorRecorrencia, PagamentoRecorrente |
| RF011 | UC10 | AD04 | AlertaRecorrencia, Alerta |

---

## 5. Resultado da Sprint 4

Ao final da Sprint 4, a UPFinance possui:

- quatro diagramas de atividades cobrindo os fluxos principais e alternativos dos casos de uso;
- uso de raias, decisões, condições de guarda, merge, fork/join, fluxo de objetos e datastore;
- diagrama de classes com classes, atributos, operações, enumerações, interface e classe abstrata;
- relacionamentos de associação, composição, generalização, realização e dependência, com multiplicidades;
- justificativa das decisões de modelagem;
- mapeamento de exemplo para código Java;
- matriz de rastreabilidade RF → UC → AD → Classes.

Os diagramas de atividades descrevem **como** o sistema se comporta ao executar cada caso de uso, enquanto o diagrama de classes descreve **quais** estruturas sustentam esse comportamento. Juntos, eles formam a base para o projeto detalhado e a implementação nas próximas sprints.
