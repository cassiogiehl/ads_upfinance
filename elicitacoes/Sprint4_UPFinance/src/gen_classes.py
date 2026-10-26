import html
def cls(name, attrs, ops, stereo=None, abstract=False):
    e=html.escape
    t = (f'<FONT POINT-SIZE="9">«{e(stereo)}»</FONT><BR/>' if stereo else '')
    n = f'<I>{e(name)}</I>' if abstract else e(name)
    a = '<BR ALIGN="LEFT"/>'.join(e(x) for x in attrs) + ('<BR ALIGN="LEFT"/>' if attrs else ' ')
    o = '<BR ALIGN="LEFT"/>'.join(e(x) for x in ops) + ('<BR ALIGN="LEFT"/>' if ops else ' ')
    return (f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
            f'<TR><TD BGCOLOR="#FFF8DC">{t}<B>{n}</B></TD></TR>'
            f'<TR><TD ALIGN="LEFT">{a}</TD></TR><TR><TD ALIGN="LEFT">{o}</TD></TR></TABLE>>')

C = {
 'Usuario': (['- id : Long','- nome : String','- email : String'],
             ['+ cadastrarMovimentacao(m : Movimentacao)','+ enviarFatura(arquivo : Arquivo) : Fatura','+ solicitarAnalise(periodo : Periodo) : AnaliseFinanceira','+ getMovimentacoes(periodo : Periodo) : List<Movimentacao>'],None,False),
 'Movimentacao': (['- id : Long','- descricao : String','- valor : BigDecimal','- data : LocalDate','- tipo : TipoMovimentacao'],
             ['+ categorizar(c : Categoria)','+ getPilar() : Pilar','+ isSaida() : boolean'],None,False),
 'Categoria': (['- id : Long','- nome : String','- pilar : Pilar'],['+ getPilar() : Pilar'],None,False),
 'Pilar': (['ESSENCIAL (0.50)','PESSOAL (0.30)','FUTURO (0.20)','- percentual : BigDecimal'],['+ calcularLimite(renda : BigDecimal) : BigDecimal'],'enumeration',False),
 'TipoMovimentacao': (['ENTRADA','SAIDA'],[],'enumeration',False),
 'Fatura': (['- id : Long','- nomeArquivo : String','- dataEnvio : LocalDate','- status : StatusFatura'],['+ marcarInterpretada()','+ marcarFalha(motivo : String)'],None,False),
 'StatusFatura': (['RECEBIDA','INTERPRETADA','NAO_INTERPRETADA'],[],'enumeration',False),
 'InterpretadorFatura': ([],['+ suporta(f : Fatura) : boolean','+ interpretar(f : Fatura) : List<Movimentacao>'],'interface',False),
 'InterpretadorFaturaPDF': ([],['+ suporta(f : Fatura) : boolean','+ interpretar(f : Fatura) : List<Movimentacao>'],None,False),
 'AnaliseFinanceira': (['- periodo : Periodo','- /renda : BigDecimal','- dataGeracao : LocalDateTime'],['+ calcularDistribuicao()','+ getInterpretacao() : String','+ getPilaresExcedidos() : List<Pilar>'],None,False),
 'DistribuicaoPilar': (['- pilar : Pilar','- totalGasto : BigDecimal','- limite : BigDecimal'],['+ getPercentualUtilizado() : BigDecimal','+ isExcedido() : boolean'],None,False),
 'Alerta': (['- id : Long','- mensagem : String','- dataEmissao : LocalDateTime','- lido : boolean'],['+ marcarComoLido()'],None,True),
 'AlertaLimite': (['- pilar : Pilar','- valorExcedido : BigDecimal'],[],None,False),
 'AlertaRecorrencia': (['- proximoVencimento : LocalDate'],[],None,False),
 'PagamentoRecorrente': (['- id : Long','- descricao : String','- valorMedio : BigDecimal','- periodicidadeDias : int','- proximoVencimento : LocalDate'],['+ calcularProximoVencimento() : LocalDate'],None,False),
 'IdentificadorRecorrencia': ([],['+ identificar(historico : List<Movimentacao>) : List<PagamentoRecorrente>'],'service',False),
}
out = ['digraph Classes {',
 'graph [fontname="DejaVu Sans", fontsize=14, label="Diagrama de Classes — UPFinance (Sprint 4)", labelloc=t, rankdir=TB, nodesep=0.6, ranksep=0.9, splines=true];',
 'node [shape=plaintext, fontname="DejaVu Sans", fontsize=10];',
 'edge [fontname="DejaVu Sans", fontsize=9, arrowsize=0.8];']
for k,(a,o,s,ab) in C.items(): out.append(f'{k} [label={cls(k,a,o,s,ab)}];')
R = '''
# composição (losango cheio na ponta do todo)
Usuario -> Movimentacao [dir=both, arrowtail=diamond, arrowhead=none, taillabel="1", headlabel="0..*", label="registra"];
Usuario -> Fatura [dir=both, arrowtail=diamond, arrowhead=none, taillabel="1", headlabel="0..*", label="envia"];
Usuario -> PagamentoRecorrente [dir=both, arrowtail=diamond, arrowhead=none, taillabel="1", headlabel="0..*", label="possui"];
AnaliseFinanceira -> DistribuicaoPilar [dir=both, arrowtail=diamond, arrowhead=none, taillabel="1", headlabel="3", label="contém"];
# associações navegáveis
Usuario -> AnaliseFinanceira [arrowhead=vee, taillabel="1", headlabel="0..*", label="solicita"];
Usuario -> Alerta [arrowhead=vee, taillabel="1", headlabel="0..*", label="recebe"];
Movimentacao -> Categoria [arrowhead=vee, taillabel="0..*", headlabel="1", label="classificada em"];
Fatura -> Movimentacao [arrowhead=vee, taillabel="0..1", headlabel="0..*", label="origina"];
PagamentoRecorrente -> Movimentacao [arrowhead=vee, taillabel="0..1", headlabel="2..*", label="baseado em"];
AnaliseFinanceira -> Movimentacao [arrowhead=vee, taillabel="0..*", headlabel="0..*", label="considera"];
AnaliseFinanceira -> AlertaLimite [dir=back, arrowtail=vee, arrowhead=none, taillabel="1", headlabel="0..3", label="gera"];
PagamentoRecorrente -> AlertaRecorrencia [dir=back, arrowtail=vee, arrowhead=none, taillabel="1", headlabel="0..*", label="gera"];
# generalização
Alerta -> AlertaLimite [dir=back, arrowtail=empty, arrowhead=none];
Alerta -> AlertaRecorrencia [dir=back, arrowtail=empty, arrowhead=none];
# realização
InterpretadorFatura -> InterpretadorFaturaPDF [dir=back, arrowtail=empty, arrowhead=none, style=dashed];
# dependências
Categoria -> Pilar [arrowhead=vee, style=dashed, label="«use»"];
Movimentacao -> TipoMovimentacao [arrowhead=vee, style=dashed, label="«use»"];
Fatura -> StatusFatura [arrowhead=vee, style=dashed, label="«use»"];
InterpretadorFatura -> Fatura [arrowhead=vee, style=dashed, label="«parameter»"];
IdentificadorRecorrencia -> PagamentoRecorrente [arrowhead=vee, style=dashed, label="«create»"];
IdentificadorRecorrencia -> Movimentacao [arrowhead=vee, style=dashed, label="«parameter»"];
'''
out.append(R); out.append('}')
open('/home/claude/sprint4/src/classes.dot','w').write('\n'.join(out))
