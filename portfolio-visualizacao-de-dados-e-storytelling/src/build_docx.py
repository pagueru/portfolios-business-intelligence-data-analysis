"""Gera o .docx final da atividade textual."""
from __future__ import annotations

import os
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).parent.parent
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

DOCX_OUT = OUTPUTS / "Visualizacao_de_Dados_e_storytelling_Raphael_Henrique_Vieira_Coelho.docx"
LIMITE_BYTES = 2 * 1024 * 1024

TITULO = "Visualização de Tendências de Consumo Energético no Palácio do Jaburu"
ALUNO = "Raphael Henrique Vieira Coelho"
CURSO = "Superior de Tecnologia em Inteligência de Mercado e Análise de Dados"
INSTITUICAO = "Anhanguera"
CIDADE_UF = "Presidente Prudente – São Paulo"
ANO = "2026"
DISCIPLINA = "Visualização de Dados e Storytelling"


# ── Estilos base ──────────────────────────────────────────────────────────────

def _configurar_estilos(doc):
    """Define Arial 12 como fonte padrão do documento."""
    estilo = doc.styles["Normal"]
    estilo.font.name = "Arial"
    estilo.font.size = Pt(12)
    # herdar para todos os estilos de parágrafo
    for st in doc.styles:
        try:
            if st.font:
                st.font.name = "Arial"
        except Exception:
            pass


# ── Utilitários de parágrafo ──────────────────────────────────────────────────

def _espaco(par, antes=0, depois=6, linha=18):
    pf = par.paragraph_format
    pf.space_before = Pt(antes)
    pf.space_after = Pt(depois)
    if linha > 0:
        pf.line_spacing = Pt(linha)


def _run(par, texto, negrito=False, tam=12, italico=False):
    r = par.add_run(texto)
    r.bold = negrito
    r.italic = italico
    r.font.name = "Arial"
    r.font.size = Pt(tam)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return r


def _par_centralizado(doc, texto, negrito=False, tam=12, antes=0, depois=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    _espaco(p, antes, depois, linha=18)
    _run(p, texto, negrito=negrito, tam=tam)
    return p


def _par_texto(doc, texto, antes=0, depois=6):
    """Parágrafo de texto corrido: Arial 12, 1,5, recuo de 1ª linha 1,25 cm."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25)
    _espaco(p, antes, depois, linha=18)
    _run(p, texto)
    return p


def _titulo_secao(doc, texto, nivel=1):
    """Título de seção: ABNT nível 1 = maiúsculas + negrito; nível 2 = negrito."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.first_line_indent = Cm(0)
    _espaco(p, antes=12, depois=6, linha=18)
    _run(p, texto, negrito=True)
    return p


def _legenda_figura(doc, texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    _espaco(p, antes=2, depois=8, linha=14)
    r = _run(p, texto, tam=10, italico=True)
    return p


def _par_ref(doc, texto):
    """Referência ABNT: sem recuo, espaçamento simples, 6 pt entre itens."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.left_indent = Cm(0)
    _espaco(p, antes=0, depois=6, linha=12)
    _run(p, texto)
    return p


def _par_codigo(doc, codigo: str):
    for linha in codigo.splitlines():
        p = doc.add_paragraph()
        _espaco(p, antes=0, depois=0, linha=10)
        r = p.add_run(linha if linha else " ")
        r.font.name = "Consolas"
        r.font.size = Pt(8)


def _adicionar_imagem(doc, caminho: Path, largura_cm=15):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    _espaco(p, antes=4, depois=4, linha=0)
    p.add_run().add_picture(str(caminho), width=Cm(largura_cm))
    return p


def _quebra_pagina(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    import docx.enum.text as det
    p.add_run().add_break(det.WD_BREAK.PAGE)


def _adicionar_numeracao(doc):
    """Adiciona número de página no cabeçalho superior direito (ABNT)."""
    for section in doc.sections:
        section.different_first_page_header_footer = True  # capa sem número
        header = section.header
        # limpa parágrafos existentes
        for p in header.paragraphs:
            p.clear()
        if not header.paragraphs:
            header.add_paragraph()
        par = header.paragraphs[0]
        par.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        par.paragraph_format.space_before = Pt(0)
        par.paragraph_format.space_after = Pt(0)
        run = par.add_run()
        run.font.name = "Arial"
        run.font.size = Pt(10)
        # campo PAGE
        for tipo in ("begin", "end"):
            fldChar = OxmlElement("w:fldChar")
            fldChar.set(qn("w:fldCharType"), tipo)
            if tipo == "begin":
                instrText = OxmlElement("w:instrText")
                instrText.text = " PAGE "
                run._r.append(fldChar)
                run._r.append(instrText)
            else:
                run._r.append(fldChar)


def _ler_codigo(nome: str) -> str:
    return (ROOT / "src" / nome).read_text(encoding="utf-8")


def _dec_br(val: float, decimais: int = 3) -> str:
    """Formata número com vírgula como separador decimal (padrão PT-BR)."""
    return f"{val:.{decimais}f}".replace(".", ",")


# ── Textos humanizados ────────────────────────────────────────────────────────

INTRO_P1 = (
    "Visualizações de dados bem construídas comunicam resultados com mais clareza "
    "do que tabelas brutas. Essa prática, chamada de data storytelling, tem sido "
    "adotada em organizações públicas e privadas para apoiar decisões a partir de "
    "evidências concretas, reduzindo a dependência de relatórios extensos que poucas "
    "pessoas leem até o fim."
)

INTRO_P2 = (
    "Este trabalho analisa o consumo de energia elétrica no Palácio do Jaburu, "
    "residência oficial do Vice-Presidente da República, entre junho de 2017 e "
    "setembro de 2024. O conjunto de dados contém 88 registros mensais com o consumo "
    "em quilowatt-hora (kWh) e o valor bruto das faturas correspondentes, "
    "disponibilizados publicamente em repositório no GitHub pelo professor Anderson Salata."
)

INTRO_P3 = (
    "A seção de Desenvolvimento responde às quatro questões do roteiro da disciplina: "
    "quais anos tiveram as maiores reduções no consumo, se existe sazonalidade no "
    "padrão de consumo, qual a relação entre consumo e valor da fatura, e de que "
    "forma gráficos interativos contribuem para a análise. A Conclusão reúne os "
    "principais achados e aponta estratégias de eficiência. O Apêndice A traz o "
    "código-fonte Python utilizado."
)

DESC_FIG1 = (
    "A Figura 1 apresenta, em barras azuis, o consumo total anual em megawatt-hora "
    "e, em linha vermelha com marcadores, o valor médio mensal da fatura em reais. "
    "Os dois eixos verticais permitem comparar a evolução das duas séries no mesmo período."
)

DESC_FIG2 = (
    "A Figura 2 mostra o consumo médio por mês, calculado sobre todos os anos "
    "disponíveis. As barras em vermelho marcam os três meses com consumo "
    "sistematicamente acima da média anual."
)

DESC_FIG3 = (
    "O diagrama de dispersão (Figura 3) relaciona o consumo mensal em MWh com o "
    "valor da fatura correspondente. Cada ponto representa um mês de referência, "
    "colorido pelo ano, o que permite identificar deslocamentos ao longo do tempo."
)

DESC_FIG4 = (
    "A Figura 4 é uma captura estática do gráfico interativo gerado com Plotly. "
    "O arquivo HTML interativo acompanha esta entrega como anexo e pode ser "
    "aberto diretamente no navegador."
)

TEXTO_INTERATIVO = (
    "No gráfico Plotly, passar o cursor sobre qualquer ponto exibe o mês de "
    "referência, o consumo em MWh e o valor da fatura, sem precisar de uma tabela "
    "separada. Clicar em um ano na legenda oculta ou exibe aquela série, o que "
    "facilita comparar dois ou três anos lado a lado. A função de zoom permite "
    "isolar uma janela temporal, como os anos da pandemia, sem gerar uma nova imagem. "
    "Quando a pergunta muda no meio da análise, o analista ajusta a visualização "
    "no lugar em vez de exportar um novo gráfico para cada recorte."
)

CONCLUSAO_P1 = (
    "A análise do consumo de energia elétrica do Palácio do Jaburu entre 2017 e "
    "setembro de 2024 mostrou que gráficos bem escolhidos comunicam tendências "
    "com mais clareza do que tabelas de dados mensais. Cada visualização produzida "
    "respondeu a uma questão específica do roteiro, cobrindo as quatro perguntas "
    "propostas na atividade."
)

CONCLUSAO_P2 = (
    "O consumo caiu de forma mais expressiva nos anos associados à pandemia de "
    "COVID-19 e apresenta sazonalidade bem definida no segundo semestre, com pico "
    "entre setembro e novembro. O valor das faturas, por sua vez, cresceu mesmo em "
    "anos de queda no consumo, o que indica que os reajustes tarifários têm peso "
    "independente do volume consumido. A correlação de Pearson calculada (r = 0,624) "
    "confirma a relação positiva entre as duas variáveis, mas também mostra que o "
    "valor não é determinado apenas pelo consumo."
)

CONCLUSAO_P3 = (
    "O gráfico interativo produzido com Plotly reduziu o número de imagens "
    "necessárias para explorar o conjunto de dados. Para o Palácio do Jaburu "
    "especificamente, monitorar o consumo mensal em relação ao histórico sazonal "
    "seria uma forma prática de identificar desvios fora do padrão esperado. Os "
    "picos de setembro a novembro são previsíveis o suficiente para justificar "
    "ações de eficiência nesse período, seja em climatização, iluminação ou outros "
    "equipamentos de alta demanda."
)


# ── Geração do documento ──────────────────────────────────────────────────────

def gerar(df, pearson_r: float):
    doc = Document()
    _configurar_estilos(doc)

    # margens ABNT: sup 3, inf 2, esq 3, dir 2
    for section in doc.sections:
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2)

    # ── CAPA ─────────────────────────────────────────────────────────────────
    _par_centralizado(doc, INSTITUICAO, negrito=True, tam=14, antes=72, depois=8)
    _par_centralizado(doc, CURSO, depois=8)
    _par_centralizado(doc, ALUNO, depois=60)
    _par_centralizado(doc, TITULO, negrito=True, tam=14, depois=60)
    _par_centralizado(doc, DISCIPLINA, depois=60)
    _par_centralizado(doc, CIDADE_UF, depois=4)
    _par_centralizado(doc, ANO, depois=0)
    _quebra_pagina(doc)

    # ── SUMÁRIO ───────────────────────────────────────────────────────────────
    _titulo_secao(doc, "SUMÁRIO")
    sumario = [
        ("1",   "INTRODUÇÃO", "3"),
        ("2",   "DESENVOLVIMENTO", "4"),
        ("2.1", "Anos com Maiores Reduções no Consumo Energético", "4"),
        ("2.2", "Padrão Sazonal no Consumo de Energia", "5"),
        ("2.3", "Relação entre Consumo e Valor da Fatura", "6"),
        ("2.4", "Como Elementos Interativos Contribuem para a Análise", "7"),
        ("3",   "CONCLUSÃO", "8"),
        ("",    "REFERÊNCIAS", "9"),
        ("",    "APÊNDICE A – CÓDIGO-FONTE", "10"),
    ]
    for num, titulo, pg in sumario:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Cm(0)
        _espaco(p, antes=0, depois=4, linha=18)
        prefixo = f"{num}  " if num else ""
        _run(p, f"{prefixo}{titulo}")
    _quebra_pagina(doc)

    # ── 1 INTRODUÇÃO ──────────────────────────────────────────────────────────
    _titulo_secao(doc, "1 INTRODUÇÃO")
    _par_texto(doc, INTRO_P1)
    _par_texto(doc, INTRO_P2)
    _par_texto(doc, INTRO_P3)
    _quebra_pagina(doc)

    # ── 2 DESENVOLVIMENTO ────────────────────────────────────────────────────
    _titulo_secao(doc, "2 DESENVOLVIMENTO")

    # 2.1
    _titulo_secao(doc, "2.1 Anos com Maiores Reduções no Consumo Energético", nivel=2)
    _par_texto(doc, DESC_FIG1)
    _adicionar_imagem(doc, OUTPUTS / "fig_linha_anual.png")
    _legenda_figura(doc, "Figura 1 – Consumo total anual e valor médio da fatura por ano (2017–2024)")

    anual = df.groupby("ano")["consumo_kwh"].sum()
    anos_queda = []
    for i in range(1, len(anual)):
        a_ant, a_at = anual.index[i - 1], anual.index[i]
        var = (anual[a_at] - anual[a_ant]) / anual[a_ant] * 100
        if var < -3:
            anos_queda.append((a_at, var))
    queda_str = "; ".join(
        f"{a} ({_dec_br(v, 1)}%)" for a, v in sorted(anos_queda, key=lambda x: x[1])
    ) or "nenhum ano apresentou queda acima de 3%"

    _par_texto(doc, (
        f"Os anos com quedas mais expressivas foram: {queda_str}. "
        f"Parte dessa redução coincide com o período de pandemia de COVID-19 "
        f"(2020–2021), quando a movimentação na residência diminuiu. "
        f"Mudanças na ocupação do imóvel entre governos diferentes também influenciam "
        f"o perfil de consumo. Em contrapartida, o valor médio da fatura cresceu mesmo "
        f"nos anos em que o consumo caiu, o que indica que os reajustes tarifários "
        f"têm peso independente do volume consumido."
    ))

    # 2.2
    _titulo_secao(doc, "2.2 Padrão Sazonal no Consumo de Energia", nivel=2)
    _par_texto(doc, DESC_FIG2)
    _adicionar_imagem(doc, OUTPUTS / "fig_barras_mensal.png")
    _legenda_figura(doc, "Figura 2 – Consumo médio mensal (2017–2024); barras em vermelho indicam pico sazonal")

    mensal = df.groupby("mes_num")["consumo_kwh"].mean()
    mes_pico = mensal.idxmax()
    MESES_PT = {
        1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
        5: "maio", 6: "junho", 7: "julho", 8: "agosto",
        9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
    }
    _par_texto(doc, (
        f"Setembro, outubro e novembro concentram os maiores consumos médios do "
        f"período, com pico em {MESES_PT[mes_pico]} "
        f"({_dec_br(mensal[mes_pico] / 1000, 1)} MWh em média). "
        f"Na região de Brasília, a primavera coincide com o início das altas "
        f"temperaturas, quando o uso de ar-condicionado e climatização aumenta. "
        f"O padrão se repete com regularidade suficiente para justificar "
        f"intervenções de eficiência antes do período de pico no segundo semestre."
    ))

    # 2.3
    _titulo_secao(doc, "2.3 Relação entre Consumo e Valor da Fatura", nivel=2)
    _par_texto(doc, DESC_FIG3)
    _adicionar_imagem(doc, OUTPUTS / "fig_correlacao.png")
    _legenda_figura(doc, (
        f"Figura 3 – Correlação entre consumo (MWh) e valor da fatura (R$) | "
        f"r de Pearson = {_dec_br(pearson_r, 3)}"
    ))
    _par_texto(doc, (
        f"O coeficiente de Pearson obtido foi r = {_dec_br(pearson_r, 3)}, o que indica "
        f"{'correlação positiva forte' if pearson_r >= 0.7 else 'correlação positiva moderada'} "
        f"entre consumo e valor da fatura. Meses de maior consumo tendem, em geral, "
        f"a gerar faturas mais altas. Contudo, a dispersão crescente ao longo dos "
        f"anos mostra que o valor da fatura aumenta em ritmo maior do que o consumo. "
        f"Os reajustes tarifários no período explicam essa diferença: o custo do kWh "
        f"subiu de 2017 a 2024, portanto dois meses com o mesmo consumo podem gerar "
        f"faturas bastante diferentes dependendo do ano. Isso também explica por que "
        f"r é significativo, mas não se aproxima de 1,0."
    ))

    # 2.4
    _titulo_secao(doc, "2.4 Como Elementos Interativos Contribuem para a Análise", nivel=2)
    _par_texto(doc, DESC_FIG4)
    _adicionar_imagem(doc, OUTPUTS / "fig_interativo_preview.png")
    _legenda_figura(doc, (
        "Figura 4 – Captura do gráfico interativo (Plotly): consumo mensal por ano, "
        "com hover, zoom e controle de séries pela legenda"
    ))
    _par_texto(doc, TEXTO_INTERATIVO)
    _quebra_pagina(doc)

    # ── 3 CONCLUSÃO ──────────────────────────────────────────────────────────
    _titulo_secao(doc, "3 CONCLUSÃO")
    _par_texto(doc, CONCLUSAO_P1)
    _par_texto(doc, CONCLUSAO_P2.replace("r = 0,624", f"r = {_dec_br(pearson_r, 3)}"))
    _par_texto(doc, CONCLUSAO_P3)
    _quebra_pagina(doc)

    # ── REFERÊNCIAS ──────────────────────────────────────────────────────────
    # título ABNT: maiúsculas, negrito, centralizado (NBR 14724)
    p_ref_titulo = doc.add_paragraph()
    p_ref_titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref_titulo.paragraph_format.first_line_indent = Cm(0)
    _espaco(p_ref_titulo, antes=0, depois=12, linha=18)
    _run(p_ref_titulo, "REFERÊNCIAS", negrito=True)

    refs = [
        (
            "COORDENAÇÃO DE APERFEIÇOAMENTO DE PESSOAL DE NÍVEL SUPERIOR (CAPES). "
            "Orientação Capes: Combate ao plágio. Brasília, 2011. Disponível em: "
            "https://www.capes.gov.br/images/stories/download/diversos/"
            "OrientacoesCapes_CombateAoPlagio.pdf. Acesso em: 23 maio 2026."
        ),
        (
            "MATPLOTLIB DEVELOPMENT TEAM. Matplotlib: Visualization with Python. "
            "[S.l.], 2024. Disponível em: https://matplotlib.org. "
            "Acesso em: 23 maio 2026."
        ),
        (
            "MCKINNEY, W. Python for Data Analysis: Data Wrangling with Pandas, "
            "NumPy and IPython. 3. ed. Sebastopol: O'Reilly Media, 2022."
        ),
        (
            "PLOTLY TECHNOLOGIES INC. Plotly Python Graphing Library. [S.l.], 2024. "
            "Disponível em: https://plotly.com/python/. Acesso em: 23 maio 2026."
        ),
        (
            "SALATA, A. Consumo de energia elétrica no Palácio do Jaburu 2017-2024. "
            "[S.l.], 2024. Disponível em: "
            "https://github.com/AndersonSalata/Materiais_Alunos_EAD. "
            "Acesso em: 23 maio 2026."
        ),
    ]
    for ref in refs:
        _par_ref(doc, ref)
    _quebra_pagina(doc)

    # ── APÊNDICE A ───────────────────────────────────────────────────────────
    _titulo_secao(doc, "APÊNDICE A – CÓDIGO-FONTE")
    _par_texto(doc, (
        "Módulos Python utilizados para ingestão dos dados, limpeza e geração "
        "das visualizações desta atividade."
    ))

    p_tl = doc.add_paragraph()
    p_tl.paragraph_format.first_line_indent = Cm(0)
    _espaco(p_tl, antes=8, depois=2, linha=14)
    _run(p_tl, "src/load_data.py", negrito=True, tam=10)
    _par_codigo(doc, _ler_codigo("load_data.py"))

    p_tp = doc.add_paragraph()
    p_tp.paragraph_format.first_line_indent = Cm(0)
    _espaco(p_tp, antes=12, depois=2, linha=14)
    _run(p_tp, "src/plots.py", negrito=True, tam=10)
    _par_codigo(doc, _ler_codigo("plots.py"))

    # numeração de páginas (ABNT: superior direito)
    _adicionar_numeracao(doc)

    doc.save(str(DOCX_OUT))
    tamanho = os.path.getsize(DOCX_OUT)
    print(f"Documento salvo: {DOCX_OUT}")
    print(f"Tamanho: {tamanho / 1024:.1f} KB / {tamanho / 1024**2:.2f} MB")
    if tamanho > LIMITE_BYTES:
        print("AVISO: arquivo excede 2 MB.")
    else:
        print("OK: dentro do limite de 2 MB.")
    return DOCX_OUT


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from load_data import carregar
    from plots import barras_mensal, correlacao, interativo_plotly, linha_anual
    from scipy import stats

    print("Carregando dados...")
    df = carregar()
    print(f"  {len(df)} registros, {df['ano'].min()}–{df['ano'].max()}")

    print("Gerando gráficos...")
    linha_anual(df)
    barras_mensal(df)
    correlacao(df)
    interativo_plotly(df)

    _, _, r, *_ = stats.linregress(df["consumo_kwh"], df["valor_fatura"])
    print(f"  Pearson r = {r:.3f}")

    print("Gerando documento...")
    gerar(df, pearson_r=r)
