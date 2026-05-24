# -*- coding: utf-8 -*-
"""Gera os dois PDFs do exame de proficiência em leitura."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# =============================================================================
# ESTILOS COMUNS
# =============================================================================

NAVY = colors.HexColor("#0d2347")
SLATE = colors.HexColor("#1e5080")
GRAY_LIGHT = colors.HexColor("#dde8f5")
GRAY_MID = colors.HexColor("#6888a8")
ACCENT = colors.HexColor("#3b82c4")

styles = getSampleStyleSheet()

def make_styles():
    s = {}
    s["cover_title"] = ParagraphStyle(
        "cover_title", fontName="Helvetica-Bold", fontSize=24, leading=30,
        textColor=NAVY, alignment=TA_LEFT, spaceAfter=6,
    )
    s["cover_subtitle"] = ParagraphStyle(
        "cover_subtitle", fontName="Helvetica", fontSize=14, leading=18,
        textColor=SLATE, alignment=TA_LEFT, spaceAfter=20,
    )
    s["volume"] = ParagraphStyle(
        "volume", fontName="Helvetica-Bold", fontSize=10, leading=12,
        textColor=ACCENT, alignment=TA_LEFT, spaceAfter=4,
    )
    s["author_label"] = ParagraphStyle(
        "author_label", fontName="Helvetica", fontSize=9, leading=11,
        textColor=GRAY_MID, alignment=TA_LEFT,
    )
    s["author_name"] = ParagraphStyle(
        "author_name", fontName="Helvetica-Bold", fontSize=11, leading=14,
        textColor=NAVY, alignment=TA_LEFT, spaceAfter=2,
    )
    s["author_role"] = ParagraphStyle(
        "author_role", fontName="Helvetica-Oblique", fontSize=10, leading=13,
        textColor=SLATE, alignment=TA_LEFT, spaceAfter=12,
    )
    s["tech_label"] = ParagraphStyle(
        "tech_label", fontName="Helvetica-Bold", fontSize=9, leading=12,
        textColor=ACCENT, alignment=TA_LEFT, spaceAfter=4,
    )
    s["tech_body"] = ParagraphStyle(
        "tech_body", fontName="Helvetica", fontSize=9.5, leading=14,
        textColor=SLATE, alignment=TA_JUSTIFY, spaceAfter=6,
    )
    s["h1"] = ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=16, leading=20,
        textColor=NAVY, alignment=TA_LEFT, spaceBefore=18, spaceAfter=10,
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=13, leading=16,
        textColor=NAVY, alignment=TA_LEFT, spaceBefore=14, spaceAfter=6,
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName="Helvetica-Bold", fontSize=11, leading=14,
        textColor=SLATE, alignment=TA_LEFT, spaceBefore=10, spaceAfter=4,
    )
    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10.5, leading=15,
        textColor=colors.black, alignment=TA_JUSTIFY, spaceAfter=6,
    )
    s["body_indent"] = ParagraphStyle(
        "body_indent", parent=s["body"], leftIndent=14,
    )
    s["text_passage"] = ParagraphStyle(
        "text_passage", fontName="Helvetica", fontSize=11, leading=17,
        textColor=colors.black, alignment=TA_JUSTIFY,
        firstLineIndent=14, spaceAfter=6,
    )
    s["question_stem"] = ParagraphStyle(
        "question_stem", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
        textColor=NAVY, alignment=TA_JUSTIFY, spaceBefore=10, spaceAfter=6,
    )
    s["alt"] = ParagraphStyle(
        "alt", fontName="Helvetica", fontSize=10.5, leading=14,
        textColor=colors.black, alignment=TA_LEFT,
        leftIndent=22, spaceAfter=3,
    )
    s["instruction"] = ParagraphStyle(
        "instruction", fontName="Helvetica-Oblique", fontSize=10, leading=13,
        textColor=SLATE, alignment=TA_LEFT, spaceAfter=6,
    )
    s["small"] = ParagraphStyle(
        "small", fontName="Helvetica", fontSize=8.5, leading=11,
        textColor=GRAY_MID, alignment=TA_LEFT,
    )
    s["small_just"] = ParagraphStyle(
        "small_just", fontName="Helvetica", fontSize=9, leading=12,
        textColor=colors.black, alignment=TA_JUSTIFY,
    )
    s["table_cell"] = ParagraphStyle(
        "table_cell", fontName="Helvetica", fontSize=9, leading=11.5,
        textColor=colors.black, alignment=TA_LEFT,
    )
    s["table_cell_bold"] = ParagraphStyle(
        "table_cell_bold", fontName="Helvetica-Bold", fontSize=9, leading=11.5,
        textColor=NAVY, alignment=TA_LEFT,
    )
    s["table_header"] = ParagraphStyle(
        "table_header", fontName="Helvetica-Bold", fontSize=9, leading=11.5,
        textColor=colors.white, alignment=TA_CENTER,
    )
    return s

S = make_styles()

# =============================================================================
# RODAPÉ E NUMERAÇÃO DE PÁGINAS
# =============================================================================

def make_page_decorator(volume_label, doc_title):
    def decorator(canv, doc):
        canv.saveState()
        canv.setFont("Helvetica", 8)
        canv.setFillColor(GRAY_MID)
        # Rodapé esquerdo
        canv.drawString(2.0 * cm, 1.2 * cm, f"{volume_label}  ·  {doc_title}")
        # Rodapé direito (número de página)
        canv.drawRightString(
            A4[0] - 2.0 * cm, 1.2 * cm, f"página {doc.page}"
        )
        # Linha de rodapé
        canv.setStrokeColor(GRAY_LIGHT)
        canv.setLineWidth(0.5)
        canv.line(2.0 * cm, 1.5 * cm, A4[0] - 2.0 * cm, 1.5 * cm)
        canv.restoreState()
    return decorator

# =============================================================================
# BLOCOS COMUNS — CABEÇALHO DO PROFESSOR E NATUREZA DO TESTE
# =============================================================================

def author_block():
    """Cartão de identificação do professor responsável."""
    data = [[
        Paragraph("PROFESSOR RESPONSÁVEL", S["author_label"]),
    ], [
        Paragraph("Rodrigo Leão", S["author_name"]),
    ], [
        Paragraph("Professor de Ensino Médio", S["author_role"]),
    ], [
        Paragraph(
            "contato.profleao@gmail.com · youtube.com/rodrigoleaobr",
            S["author_role"]
        ),
    ]]
    tbl = Table(data, colWidths=[16.5 * cm])
    tbl.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (0, 0), 10),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("LINEBEFORE", (0, 0), (0, -1), 2, ACCENT),
        ("BACKGROUND", (0, 0), (-1, -1), GRAY_LIGHT),
    ]))
    return tbl

def technical_description(audience="aluno"):
    """Descrição técnica do instrumento."""
    elems = []
    elems.append(Paragraph("NATUREZA DO INSTRUMENTO", S["tech_label"]))

    if audience == "aluno":
        body = (
            "Esta avaliação é um instrumento diagnóstico de proficiência em "
            "leitura. Ela não mede conhecimento de conteúdos curriculares nem "
            "tem caráter classificatório. Seu objetivo é identificar como "
            "você processa um texto: o que você consegue compreender com "
            "facilidade e em que ponto a leitura encontra obstáculos. "
            "Os resultados serão utilizados para planejar um programa de "
            "aperfeiçoamento da leitura adequado à sua realidade. "
            "Responda com calma e atenção — não há nota para boletim, "
            "mas há a chance de tornar a leitura uma ferramenta mais "
            "potente na sua trajetória."
        )
        elems.append(Paragraph(body, S["tech_body"]))
    else:
        body = (
            "Instrumento de avaliação diagnóstica de proficiência leitora "
            "para alunos de Ensino Médio, com aplicação coletiva e duração "
            "estimada de 50 a 70 minutos. Não constitui avaliação de "
            "conhecimento curricular nem prova classificatória — mede "
            "operações cognitivas envolvidas na compreensão textual, "
            "distribuídas em cinco níveis hierárquicos:"
        )
        elems.append(Paragraph(body, S["tech_body"]))

        levels = [
            ["P0", "Identificação elementar (pré-inferencial): tema, vocabulário em contexto, sequência."],
            ["P1", "Recuperação de informação explícita declarada textualmente."],
            ["P2", "Inferência direta por integração intraparagráfica."],
            ["P3", "Interpretação e integração global do texto: mensagem, tom, intenção."],
            ["P4", "Avaliação crítica de escolhas autorais e elementos textuais."],
        ]
        rows = []
        for code, desc in levels:
            rows.append([
                Paragraph(f"<b>{code}</b>", S["table_cell_bold"]),
                Paragraph(desc, S["table_cell"]),
            ])
        tbl = Table(rows, colWidths=[1.2 * cm, 15.3 * cm])
        tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1, 6))

        body2 = (
            "<b>Base teórica:</b> PIRLS 2021 Assessment Framework — Progress in "
            "International Reading Literacy Study, IEA / TIMSS &amp; PIRLS "
            "International Study Center, Boston College."
        )
        elems.append(Paragraph(body2, S["tech_body"]))

        body3 = (
            "<b>Calibragem:</b> textos curtos (122 e 235 palavras), vocabulário "
            "concreto, sintaxe direta, sem itens discursivos. Instrumento "
            "dimensionado para o piso da escala de proficiência, com função "
            "diagnóstica de identificar o ponto exato em que a compreensão se "
            "rompe — anterior à medição de capacidade leitora plena. "
            "Os resultados produzem perfil individual e mapa coletivo da turma, "
            "ambos destinados ao planejamento do programa de intervenção."
        )
        elems.append(Paragraph(body3, S["tech_body"]))

    return elems

# =============================================================================
# PDF 1 — EXAME DO ALUNO
# =============================================================================

def build_exame(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=2.0 * cm, rightMargin=2.0 * cm,
        topMargin=2.0 * cm, bottomMargin=2.0 * cm,
        title="LEIA! — Levantamento Integrado de Avaliação em Leitura",
        author="Rodrigo Leão",
    )
    elems = []

    # === CAPA ===
    elems.append(Paragraph("VOLUME I", S["volume"]))
    elems.append(Paragraph("LEIA! — Levantamento Integrado de Avaliação em Leitura", S["cover_title"]))
    elems.append(Paragraph(
        "Avaliação Diagnóstica — Ensino Médio",
        S["cover_subtitle"]
    ))
    elems.append(author_block())
    elems.append(Spacer(1, 18))
    elems.extend(technical_description(audience="aluno"))
    elems.append(Spacer(1, 14))

    # Bloco de identificação
    ident_data = [
        ["Escola:", "", "Data:", ""],
        ["Aluno(a):", "", "Turma:", ""],
        ["Nº:", "", "Idade:", ""],
    ]
    ident_tbl = Table(
        ident_data,
        colWidths=[2.2 * cm, 8.3 * cm, 1.5 * cm, 4.5 * cm],
        rowHeights=[0.95 * cm] * 3,
    )
    ident_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
        ("TEXTCOLOR", (0, 0), (0, -1), SLATE),
        ("TEXTCOLOR", (2, 0), (2, -1), SLATE),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 10),
        ("FONT", (2, 0), (2, -1), "Helvetica-Bold", 10),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LINEBELOW", (1, 0), (1, -1), 0.5, NAVY),
        ("LINEBELOW", (3, 0), (3, -1), 0.5, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    elems.append(ident_tbl)
    elems.append(Spacer(1, 10))

    # Instruções
    elems.append(Paragraph("INSTRUÇÕES", S["tech_label"]))
    instr_items = [
        "Leia com atenção cada texto antes de responder às questões correspondentes.",
        "Para cada questão, marque <b>apenas uma</b> alternativa.",
        "Utilize caneta azul ou preta. Não rasure.",
        "Tempo total estimado: 50 a 70 minutos. Não é permitido o uso de dicionário ou celular.",
    ]
    for it in instr_items:
        elems.append(Paragraph(f"·&nbsp;&nbsp;{it}", S["instruction"]))

    elems.append(PageBreak())

    # === TEXTO 1 ===
    elems.append(Paragraph("TEXTO 1 — A Entrevista", S["h1"]))

    t1_paragraphs = [
        ("Carla tinha 18 anos e nunca tinha trabalhado. Quando viu o cartaz "
         "colado na porta do mercado do bairro — <i>“Contratamos caixa, não é "
         "necessária experiência”</i> — entrou sem pensar duas vezes."),
        ("A gerente chamou Carla para uma sala pequena nos fundos do mercado "
         "e fez algumas perguntas simples: nome completo, onde morava, se o "
         "ensino médio estava completo ou incompleto. Carla respondeu com a "
         "voz firme, mas as mãos tremiam debaixo da mesa."),
        ("No final da conversa, a gerente disse: <i>“Você parece ser esforçada. "
         "Se ainda quiser a vaga, pode começar na segunda-feira.”</i>"),
        ("Carla saiu do mercado sem conseguir acreditar. Ligou para a mãe ainda "
         "na calçada, antes mesmo de chegar em casa. A mãe chorou. Elas "
         "precisavam muito daquele dinheiro."),
    ]
    for p in t1_paragraphs:
        elems.append(Paragraph(p, S["text_passage"]))

    elems.append(Spacer(1, 6))
    elems.append(HRFlowable(width="100%", thickness=0.5, color=GRAY_LIGHT))
    elems.append(Paragraph("Questões — Texto 1", S["h2"]))

    # Questões Texto 1
    q1 = [
        ("1.", "Qual é o assunto principal deste texto?",
         ["A) A rotina de trabalho de uma gerente de mercado.",
          "B) A primeira entrevista de emprego de uma jovem.",
          "C) As dificuldades do comércio em bairros pobres.",
          "D) A amizade entre uma filha e sua mãe."]),
        ("2.", "No texto, a gerente disse que Carla parece ser "
               "<i>“esforçada”</i>. Qual das palavras abaixo tem sentido "
               "parecido com <i>“esforçada”</i>?",
         ["A) Distraída.",
          "B) Quieta.",
          "C) Dedicada.",
          "D) Experiente."]),
        ("3.", "O que aconteceu <b>primeiro</b> na história?",
         ["A) Carla ligou para a mãe na calçada.",
          "B) A gerente disse que Carla poderia começar na segunda-feira.",
          "C) A mãe de Carla chorou ao ouvir a novidade.",
          "D) Carla viu o cartaz na porta do mercado."]),
        ("4.", "Quantos anos Carla tinha quando foi à entrevista?",
         ["A) 16 anos.",
          "B) 17 anos.",
          "C) 18 anos.",
          "D) O texto não informa a idade de Carla."]),
        ("5.", "O que estava escrito no cartaz que Carla viu na porta do "
               "mercado?",
         ["A) “Precisamos de gerente com experiência comprovada.”",
          "B) “Contratamos caixa, não é necessária experiência.”",
          "C) “Vagas abertas para caixa e estoquista.”",
          "D) “Contratamos funcionários do bairro.”"]),
        ("6.", "Onde aconteceu a conversa entre Carla e a gerente?",
         ["A) Na entrada do mercado, perto dos caixas.",
          "B) Na calçada em frente ao mercado.",
          "C) Em uma sala pequena nos fundos do mercado.",
          "D) Em um escritório fora do mercado."]),
        ("7.", "Por que as mãos de Carla tremiam debaixo da mesa durante a "
               "entrevista?",
         ["A) Ela estava com frio por causa do ar-condicionado.",
          "B) Ela estava nervosa com a situação.",
          "C) Ela estava com uma ferida na mão.",
          "D) Ela estava com sono e muito cansada."]),
        ("8.", "O texto diz que Carla <i>“entrou sem pensar duas vezes”</i> "
               "quando viu o cartaz. O que isso indica sobre ela?",
         ["A) Que ela não leu o cartaz com atenção.",
          "B) Que ela não precisava tanto do emprego.",
          "C) Que ela agiu com determinação e não deixou a oportunidade passar.",
          "D) Que ela não sabia o que era uma função de caixa."]),
        ("9.", "No final do texto, a mãe de Carla chora ao saber da notícia. "
               "Considerando tudo o que o texto mostra, qual sentimento "
               "melhor descreve o final da história?",
         ["A) Tristeza, porque o emprego de caixa é difícil e mal pago.",
          "B) Raiva, porque Carla demorou muito para conseguir um trabalho.",
          "C) Alívio e esperança, porque uma oportunidade importante chegou "
          "para uma família que precisava.",
          "D) Orgulho da gerente, que soube reconhecer uma boa funcionária."]),
        ("10.", "Qual é a mensagem principal deste texto?",
         ["A) Que jovens devem procurar emprego antes mesmo de terminar o "
          "ensino médio.",
          "B) Que os mercados de bairro são os melhores empregadores para "
          "jovens.",
          "C) Que uma simples oportunidade de trabalho pode representar uma "
          "grande mudança na vida de quem precisa.",
          "D) Que entrevistas de emprego são sempre simples e rápidas."]),
    ]
    add_questions(elems, q1)

    elems.append(PageBreak())

    # === TEXTO 2 ===
    elems.append(Paragraph("TEXTO 2 — A Armadilha das Notificações", S["h1"]))

    t2_paragraphs = [
        ("Você já percebeu que é difícil parar de olhar para o celular, mesmo "
         "quando não há nada importante para ver? Isso não acontece por acaso."),
        ("Aplicativos de redes sociais são desenvolvidos por equipes de "
         "especialistas com um objetivo claro: manter o usuário conectado pelo "
         "maior tempo possível. Para isso, utilizam um mecanismo que explora o "
         "funcionamento do cérebro humano. Cada curtida, comentário ou "
         "notificação provoca a liberação de pequenas doses de dopamina, uma "
         "substância responsável pela sensação de prazer e recompensa. O "
         "resultado se parece com qualquer tipo de vício: o cérebro aprende a "
         "buscar aquele estímulo repetidamente, mesmo quando não há nenhuma "
         "mensagem nova para ler."),
        ("Pesquisas realizadas em universidades dos Estados Unidos e da Europa "
         "mostram que jovens entre 13 e 25 anos verificam o celular, em média, "
         "96 vezes por dia — o equivalente a uma vez a cada dez minutos "
         "enquanto estão acordados. Boa parte dessas verificações acontece sem "
         "nenhuma notificação: o próprio hábito vira automático."),
        ("O problema não está no celular em si, mas no uso sem consciência. "
         "Especialistas recomendam períodos do dia sem acesso ao celular, "
         "especialmente durante as refeições e antes de dormir. Pequenas "
         "pausas digitais ajudam o cérebro a recuperar a capacidade de "
         "concentração e reduzem a ansiedade causada pela sensação de estar "
         "sempre disponível."),
    ]
    for p in t2_paragraphs:
        elems.append(Paragraph(p, S["text_passage"]))

    elems.append(Spacer(1, 6))
    elems.append(HRFlowable(width="100%", thickness=0.5, color=GRAY_LIGHT))
    elems.append(Paragraph("Questões — Texto 2", S["h2"]))

    q2 = [
        ("11.", "Segundo o texto, quantas vezes por dia jovens entre 13 e 25 "
                "anos verificam o celular, em média?",
         ["A) 69 vezes.",
          "B) 96 vezes.",
          "C) 100 vezes.",
          "D) O texto não menciona esse número."]),
        ("12.", "De acordo com o texto, o que provoca a liberação de dopamina "
                "no cérebro?",
         ["A) Assistir vídeos longos nas redes sociais.",
          "B) Usar o celular por mais de uma hora seguida.",
          "C) Curtidas, comentários e notificações.",
          "D) Baixar novos aplicativos no celular."]),
        ("13.", "O texto compara o uso excessivo de celular a um vício. O "
                "que, dentro do texto, justifica essa comparação?",
         ["A) O celular é caro e as pessoas ficam com medo de perdê-lo.",
          "B) O cérebro aprende a buscar repetidamente o estímulo da "
          "dopamina, mesmo sem novidades.",
          "C) As redes sociais obrigam o usuário a acessar o aplicativo "
          "todos os dias.",
          "D) Os jovens passam a dormir menos por causa do celular."]),
        ("14.", "O texto afirma que <i>“o próprio hábito vira automático”</i>. "
                "O que essa expressão significa no contexto?",
         ["A) O celular começa a funcionar de forma independente do usuário.",
          "B) O aplicativo passa a enviar notificações com ainda mais "
          "frequência.",
          "C) A pessoa verifica o celular por impulso, mesmo sem ter "
          "recebido nenhum aviso.",
          "D) O cérebro para de processar informações novas com o tempo."]),
        ("15.", "O texto diz que <i>“pausas digitais reduzem a ansiedade "
                "causada pela sensação de estar sempre disponível”</i>. O que "
                "provoca essa ansiedade, segundo o texto?",
         ["A) Receber muitas notificações ao mesmo tempo.",
          "B) Usar um celular com pouca memória.",
          "C) A pressão de estar constantemente acessível e conectado.",
          "D) A falta de sinal de internet em alguns momentos."]),
        ("16.", "Boa parte das verificações do celular acontece <i>“sem "
                "nenhuma notificação”</i>. O que isso indica sobre o "
                "comportamento do usuário?",
         ["A) Que as notificações do celular costumam funcionar mal.",
          "B) Que os usuários geralmente desativam as notificações dos "
          "aplicativos.",
          "C) Que verificar o celular virou um reflexo, independente de "
          "qualquer estímulo externo.",
          "D) Que o celular perde sinal com frequência no dia a dia."]),
        ("17.", "Por que o texto menciona pesquisas realizadas em "
                "universidades dos Estados Unidos e da Europa?",
         ["A) Para mostrar que o problema existe apenas em países ricos.",
          "B) Para comparar o comportamento de jovens brasileiros com o de "
          "jovens estrangeiros.",
          "C) Para dar credibilidade ao dado sobre a frequência com que "
          "jovens verificam o celular.",
          "D) Para sugerir que o Brasil não realiza pesquisas sobre esse "
          "tema."]),
        ("18.", "Qual é a ideia central deste texto?",
         ["A) Jovens usam o celular de forma irresponsável e precisam ser "
          "proibidos de acessar redes sociais.",
          "B) O uso excessivo do celular resulta de um design intencional "
          "que explora mecanismos cerebrais, mas pode ser controlado com "
          "hábitos conscientes.",
          "C) A dopamina é uma substância perigosa que deveria ser "
          "eliminada do organismo.",
          "D) As redes sociais foram criadas com o objetivo de prejudicar a "
          "saúde dos jovens."]),
        ("19.", "O tom predominante do texto é:",
         ["A) Alarmista, com o objetivo de assustar o leitor sobre os "
          "perigos do celular.",
          "B) Humorístico, tratando o tema com leveza e ironia.",
          "C) Informativo e analítico, explicando o fenômeno e apontando "
          "formas de lidar com ele.",
          "D) Nostálgico, lembrando como era a vida antes dos celulares."]),
        ("20.", "No segundo parágrafo, o texto diz que os aplicativos "
                "<i>“exploram o funcionamento do cérebro humano”</i>. A "
                "escolha do verbo <i>“explorar”</i> nesse contexto sugere que:",
         ["A) Os desenvolvedores estudam o cérebro para melhorar a "
          "experiência do usuário.",
          "B) Os usuários descobrem novas capacidades do próprio cérebro ao "
          "usar os aplicativos.",
          "C) Os aplicativos se aproveitam de características do cérebro "
          "humano para prender a atenção.",
          "D) O funcionamento do cérebro humano ainda é desconhecido para a "
          "ciência."]),
    ]
    add_questions(elems, q2)

    # Folha de respostas OMR inserida via mesclagem (ver __main__)

    decorator = make_page_decorator(
        "LEIA!", "Levantamento Integrado de Avaliação em Leitura"
    )
    doc.build(elems, onFirstPage=decorator, onLaterPages=decorator)


def fiducial_marker(size=0.5 * cm):
    """Marca de referência (quadrado preto) para alinhamento na leitura automatizada."""
    t = Table([[""]], colWidths=[size], rowHeights=[size])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.black),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def answer_sheet_OLD_REMOVED():
    """Folha de respostas compacta, otimizada para leitura por OCR / visão computacional.

    Convenções:
      - Cabeçalho fixo com identificador do template ("PIRLS-EM v1").
      - Marcas fiduciais (quadrados pretos) nos quatro cantos da grade de marcação.
      - Células de marcação com bordas pretas espessas e dimensões padronizadas.
      - Aluno marca um X dentro da célula correspondente à alternativa.
      - Bloco do professor abaixo, para correção manual e cálculo de subtotais.
    """
    elems = []

    # === CABEÇALHO COMPACTO ===
    title_data = [[
        Paragraph(
            "<b>FOLHA DE RESPOSTAS</b>",
            ParagraphStyle("fs_title", fontName="Helvetica-Bold",
                           fontSize=13, leading=15, textColor=NAVY,
                           alignment=TA_LEFT)
        ),
        Paragraph(
            "<font color='#6b3410'><b>PIRLS-EM v1</b></font>",
            ParagraphStyle("fs_code", fontName="Helvetica-Bold",
                           fontSize=10, leading=12, alignment=TA_LEFT)
        ),
    ]]
    title_tbl = Table(title_data, colWidths=[10.0 * cm, 6.5 * cm])
    title_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(title_tbl)
    elems.append(Spacer(1, 2))
    elems.append(Paragraph(
        "Marque um <b>X</b> dentro do quadrado da alternativa escolhida. "
        "Use uma só marca por questão.",
        ParagraphStyle("fs_inst", fontName="Helvetica-Oblique",
                       fontSize=8.5, leading=10, textColor=SLATE)
    ))
    elems.append(Spacer(1, 6))

    # === BLOCO DE IDENTIFICAÇÃO COMPACTO ===
    ident_data = [
        ["Aluno(a):", "", "Turma:", "", "Nº:", ""],
        ["Escola:", "", "Data:", "", "Idade:", ""],
    ]
    ident_tbl = Table(
        ident_data,
        colWidths=[1.7 * cm, 5.8 * cm, 1.3 * cm, 3.0 * cm, 1.2 * cm, 3.5 * cm],
        rowHeights=[0.65 * cm] * 2,
    )
    ident_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.5),
        ("FONT", (2, 0), (2, -1), "Helvetica-Bold", 8.5),
        ("FONT", (4, 0), (4, -1), "Helvetica-Bold", 8.5),
        ("TEXTCOLOR", (0, 0), (0, -1), SLATE),
        ("TEXTCOLOR", (2, 0), (2, -1), SLATE),
        ("TEXTCOLOR", (4, 0), (4, -1), SLATE),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LINEBELOW", (1, 0), (1, -1), 0.6, colors.black),
        ("LINEBELOW", (3, 0), (3, -1), 0.6, colors.black),
        ("LINEBELOW", (5, 0), (5, -1), 0.6, colors.black),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    elems.append(ident_tbl)
    elems.append(Spacer(1, 10))

    # === GRADE DE MARCAÇÃO DO ALUNO ===
    # Construída com 4 fiduciais nos cantos para alinhamento de imagem
    def build_marking_block(start, end):
        rows = [[
            Paragraph("<b>Nº</b>",
                      ParagraphStyle("h", fontName="Helvetica-Bold",
                                     fontSize=8.5, alignment=TA_CENTER,
                                     textColor=colors.white)),
            Paragraph("<b>A</b>",
                      ParagraphStyle("h", fontName="Helvetica-Bold",
                                     fontSize=8.5, alignment=TA_CENTER,
                                     textColor=colors.white)),
            Paragraph("<b>B</b>",
                      ParagraphStyle("h", fontName="Helvetica-Bold",
                                     fontSize=8.5, alignment=TA_CENTER,
                                     textColor=colors.white)),
            Paragraph("<b>C</b>",
                      ParagraphStyle("h", fontName="Helvetica-Bold",
                                     fontSize=8.5, alignment=TA_CENTER,
                                     textColor=colors.white)),
            Paragraph("<b>D</b>",
                      ParagraphStyle("h", fontName="Helvetica-Bold",
                                     fontSize=8.5, alignment=TA_CENTER,
                                     textColor=colors.white)),
        ]]
        for i in range(start, end + 1):
            rows.append([
                Paragraph(
                    f"<b>{i:02d}</b>",
                    ParagraphStyle("n", fontName="Helvetica-Bold",
                                   fontSize=9, alignment=TA_CENTER)
                ),
                "", "", "", "",
            ])
        tbl = Table(
            rows,
            colWidths=[0.9 * cm, 1.0 * cm, 1.0 * cm, 1.0 * cm, 1.0 * cm],
            rowHeights=[0.55 * cm] + [0.62 * cm] * (end - start + 1),
        )
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.black),
            ("BACKGROUND", (0, 1), (0, -1), GRAY_LIGHT),
            ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
            ("LINEBEFORE", (1, 1), (-1, -1), 1.0, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]))
        return tbl

    block1 = build_marking_block(1, 10)
    block2 = build_marking_block(11, 20)

    # Disposição: [fiducial] [block1] [gap] [block2] [fiducial]
    # Usa subtabela para juntar os fiduciais aos blocos
    grid_row = [
        fiducial_marker(),
        block1,
        "",
        block2,
        fiducial_marker(),
    ]
    grid_tbl = Table(
        [grid_row],
        colWidths=[0.45 * cm, 4.9 * cm, 1.0 * cm, 4.9 * cm, 0.45 * cm],
    )
    grid_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    # Linha inferior de fiduciais (mesmo padrão)
    bottom_fid_row = Table(
        [[fiducial_marker(), "", fiducial_marker()]],
        colWidths=[0.45 * cm, 10.8 * cm, 0.45 * cm],
    )
    bottom_fid_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))

    # Centralizar grid_tbl na página
    centered = Table([[grid_tbl]], colWidths=[16.5 * cm])
    centered.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(centered)

    # Fiduciais inferiores alinhados
    elems.append(Spacer(1, 2))
    bot_centered = Table([[bottom_fid_row]], colWidths=[16.5 * cm])
    bot_centered.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(bot_centered)

    elems.append(Spacer(1, 6))

    # Assinatura compacta
    sig_data = [["Assinatura do aluno:",
                 "____________________________________________"]]
    sig_tbl = Table(sig_data, colWidths=[3.7 * cm, 12.8 * cm])
    sig_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.5),
        ("TEXTCOLOR", (0, 0), (0, -1), SLATE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(sig_tbl)

    elems.append(Spacer(1, 8))
    elems.append(HRFlowable(width="100%", thickness=0.4, color=GRAY_LIGHT,
                            dash=(2, 2)))
    elems.append(Spacer(1, 4))

    # === ÁREA DO PROFESSOR ===
    elems.append(Paragraph(
        "<b>USO DO PROFESSOR</b> &nbsp;·&nbsp; correção e diagnóstico",
        ParagraphStyle("prof_label", fontName="Helvetica-Bold",
                       fontSize=8.5, leading=10, textColor=ACCENT)
    ))
    elems.append(Spacer(1, 4))

    def build_teacher_block(start, end):
        gabarito = ["B", "C", "D", "C", "B", "C", "B", "C", "C", "C",
                    "B", "C", "B", "C", "C", "C", "C", "B", "C", "C"]
        processos = ["P0", "P0", "P0", "P0", "P1", "P1", "P2", "P2", "P3", "P3",
                     "P1", "P1", "P2", "P2", "P2", "P2", "P2", "P3", "P3", "P4"]
        h_style = ParagraphStyle("th", fontName="Helvetica-Bold",
                                  fontSize=7.5, alignment=TA_CENTER,
                                  textColor=colors.white)
        c_style = ParagraphStyle("tc", fontName="Helvetica",
                                  fontSize=8, alignment=TA_CENTER)
        cb_style = ParagraphStyle("tcb", fontName="Helvetica-Bold",
                                   fontSize=8, alignment=TA_CENTER)
        rows = [[
            Paragraph("<b>Nº</b>", h_style),
            Paragraph("<b>Resp</b>", h_style),
            Paragraph("<b>Gab</b>", h_style),
            Paragraph("<b>✓/✗</b>", h_style),
            Paragraph("<b>P</b>", h_style),
        ]]
        for i in range(start, end + 1):
            rows.append([
                Paragraph(f"<b>{i:02d}</b>", cb_style),
                "",
                Paragraph(f"<b>{gabarito[i-1]}</b>", c_style),
                "",
                Paragraph(processos[i-1], c_style),
            ])
        tbl = Table(
            rows,
            colWidths=[0.75 * cm, 1.0 * cm, 0.85 * cm, 1.0 * cm, 0.85 * cm],
            rowHeights=[0.45 * cm] + [0.42 * cm] * (end - start + 1),
        )
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), SLATE),
            ("GRID", (0, 0), (-1, -1), 0.4, GRAY_MID),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BACKGROUND", (2, 1), (2, -1), GRAY_LIGHT),
            ("BACKGROUND", (4, 1), (4, -1), GRAY_LIGHT),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]))
        return tbl

    tblock1 = build_teacher_block(1, 10)
    tblock2 = build_teacher_block(11, 20)
    side = Table(
        [[tblock1, "", tblock2]],
        colWidths=[4.45 * cm, 1.0 * cm, 4.45 * cm],
    )
    side.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    centered_t = Table([[side]], colWidths=[16.5 * cm])
    centered_t.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(centered_t)

    elems.append(Spacer(1, 8))

    # Linha de subtotais por processo
    h_style = ParagraphStyle("sh", fontName="Helvetica-Bold",
                              fontSize=8.5, alignment=TA_CENTER,
                              textColor=colors.white)
    subtot_rows = [[
        Paragraph("<b>Subtotais por processo</b>",
                  ParagraphStyle("st", fontName="Helvetica-Bold",
                                 fontSize=8.5, textColor=SLATE,
                                 alignment=TA_LEFT)),
        Paragraph("<b>P0</b> /4", h_style),
        Paragraph("<b>P1</b> /4", h_style),
        Paragraph("<b>P2</b> /7", h_style),
        Paragraph("<b>P3</b> /4", h_style),
        Paragraph("<b>P4</b> /1", h_style),
        Paragraph("<b>TOTAL</b> /20", h_style),
        Paragraph("<b>Perfil</b>", h_style),
    ], ["", "", "", "", "", "", "", ""]]
    tbl = Table(
        subtot_rows,
        colWidths=[3.8 * cm, 1.4 * cm, 1.4 * cm, 1.4 * cm, 1.4 * cm,
                   1.4 * cm, 2.0 * cm, 2.2 * cm],
        rowHeights=[0.55 * cm, 0.75 * cm],
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (1, 0), (-1, 0), SLATE),
        ("BACKGROUND", (0, 0), (0, 0), GRAY_LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.4, GRAY_MID),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    elems.append(tbl)

    return elems


def answer_sheet():
    """Folha de respostas em página única, com diagramação robusta e legível.

    Estratégia para evitar clipping:
      - Conteúdo em narrow cells usa STRINGS planas + TableStyle FONT,
        NÃO Paragraph (Paragraph em cell pequena clipa por leading).
      - Alturas de linha generosas (≥0.7 cm) para acomodar 9–11 pt.
      - Bordas pretas espessas para visibilidade na digitalização.

    Recursos para OCR / visão computacional:
      - Identificador de template "PIRLS-EM v1" no topo.
      - Quatro marcas fiduciais (quadrados pretos) ao redor da grade de marcação.
      - Cabeçalho da grade em preto sólido (linha-âncora).
      - Numeração em dois dígitos (01–20).
    """
    elems = []

    # ---------- CABEÇALHO ----------
    title_data = [["FOLHA DE RESPOSTAS", "LEIA!-EM valpha"]]
    title_tbl = Table(title_data, colWidths=[12.0 * cm, 4.5 * cm],
                      rowHeights=[0.7 * cm])
    title_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (0, 0), "Helvetica-Bold", 13),
        ("TEXTCOLOR", (0, 0), (0, 0), NAVY),
        ("FONT", (1, 0), (1, 0), "Helvetica-Bold", 10),
        ("TEXTCOLOR", (1, 0), (1, 0), ACCENT),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(title_tbl)

    instr_style = ParagraphStyle(
        "as_inst", fontName="Helvetica-Oblique", fontSize=9, leading=11,
        textColor=SLATE, alignment=TA_LEFT,
    )
    elems.append(Paragraph(
        "Marque um <b>X</b> dentro do quadrado da alternativa escolhida — "
        "uma só marca por questão.", instr_style
    ))
    elems.append(Spacer(1, 6))

    # ---------- IDENTIFICAÇÃO ----------
    ident_data = [
        ["Aluno(a):", "", "Turma:", "", "Nº:", ""],
        ["Escola:",   "", "Data:",  "", "Idade:", ""],
    ]
    ident_tbl = Table(
        ident_data,
        colWidths=[1.8 * cm, 5.7 * cm, 1.3 * cm, 3.0 * cm, 1.2 * cm, 3.5 * cm],
        rowHeights=[0.75 * cm, 0.75 * cm],
    )
    ident_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 9.5),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9.5),
        ("FONT", (2, 0), (2, -1), "Helvetica-Bold", 9.5),
        ("FONT", (4, 0), (4, -1), "Helvetica-Bold", 9.5),
        ("TEXTCOLOR", (0, 0), (0, -1), SLATE),
        ("TEXTCOLOR", (2, 0), (2, -1), SLATE),
        ("TEXTCOLOR", (4, 0), (4, -1), SLATE),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LINEBELOW", (1, 0), (1, -1), 0.6, colors.black),
        ("LINEBELOW", (3, 0), (3, -1), 0.6, colors.black),
        ("LINEBELOW", (5, 0), (5, -1), 0.6, colors.black),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))
    elems.append(ident_tbl)
    elems.append(Spacer(1, 8))

    # ---------- GRADE DO ALUNO ----------
    def build_marking_block(start, end):
        rows = [["Nº", "A", "B", "C", "D"]]
        for i in range(start, end + 1):
            rows.append([f"{i:02d}", "", "", "", ""])
        tbl = Table(
            rows,
            colWidths=[1.0 * cm, 1.1 * cm, 1.1 * cm, 1.1 * cm, 1.1 * cm],
            rowHeights=[0.65 * cm] + [0.7 * cm] * (end - start + 1),
        )
        tbl.setStyle(TableStyle([
            # Cabeçalho preto
            ("BACKGROUND", (0, 0), (-1, 0), colors.black),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 11),
            # Coluna de números
            ("BACKGROUND", (0, 1), (0, -1), GRAY_LIGHT),
            ("FONT", (0, 1), (0, -1), "Helvetica-Bold", 11),
            # Bordas
            ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
            ("LINEBEFORE", (1, 1), (1, -1), 1.2, colors.black),
            # Alinhamento
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        return tbl

    block1 = build_marking_block(1, 10)
    block2 = build_marking_block(11, 20)
    fid = lambda: fiducial_marker(0.5 * cm)

    # Composição: fiduciais nos cantos da grade
    # Estrutura: 3 linhas
    #   linha 1: [fid] [vazio] [fid]
    #   linha 2: [block1] [gap] [block2]  (com fiduciais na margem externa)
    #   linha 3: [fid] [vazio] [fid]
    # Para isso, montamos 5 colunas: [fid_col][block1][gap][block2][fid_col]
    # e usamos linhas de fiduciais antes e depois.

    inner_width_block = 5.4 * cm  # 1.0 + 1.1*4
    gap = 1.0 * cm
    fid_col = 0.55 * cm  # leve folga ao redor do fiducial 0.5cm

    top_fid_row = [fid(), "", "", "", fid()]
    middle_row = ["", block1, "", block2, ""]
    bot_fid_row = [fid(), "", "", "", fid()]

    grid_assembly = Table(
        [top_fid_row, middle_row, bot_fid_row],
        colWidths=[fid_col, inner_width_block, gap, inner_width_block, fid_col],
        rowHeights=[0.55 * cm, None, 0.55 * cm],
    )
    grid_assembly.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    # Centraliza horizontalmente
    centered = Table([[grid_assembly]], colWidths=[16.5 * cm])
    centered.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(centered)
    elems.append(Spacer(1, 8))

    # ---------- ASSINATURA ----------
    sig_data = [["Assinatura do aluno:",
                 "____________________________________________"]]
    sig_tbl = Table(sig_data, colWidths=[3.8 * cm, 12.7 * cm],
                    rowHeights=[0.6 * cm])
    sig_tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 9.5),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9.5),
        ("TEXTCOLOR", (0, 0), (0, -1), SLATE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(sig_tbl)

    elems.append(Spacer(1, 6))
    elems.append(HRFlowable(width="100%", thickness=0.5, color=GRAY_MID,
                            dash=(2, 2)))
    elems.append(Spacer(1, 6))

    # ---------- ÁREA DO PROFESSOR ----------
    prof_label_style = ParagraphStyle(
        "prof", fontName="Helvetica-Bold", fontSize=9.5, leading=12,
        textColor=ACCENT,
    )
    elems.append(Paragraph(
        "USO DO PROFESSOR &nbsp;·&nbsp; correção e diagnóstico",
        prof_label_style
    ))
    elems.append(Spacer(1, 6))

    gabarito = ["B", "C", "D", "C", "B", "C", "B", "C", "C", "C",
                "B", "C", "B", "C", "C", "C", "C", "B", "C", "C"]
    processos = ["P0", "P0", "P0", "P0", "P1", "P1", "P2", "P2", "P3", "P3",
                 "P1", "P1", "P2", "P2", "P2", "P2", "P2", "P3", "P3", "P4"]

    def build_teacher_block(start, end):
        rows = [["Nº", "Resp", "Gab", "OK", "Proc"]]
        for i in range(start, end + 1):
            rows.append([
                f"{i:02d}", "", gabarito[i - 1], "", processos[i - 1],
            ])
        tbl = Table(
            rows,
            colWidths=[0.95 * cm, 1.15 * cm, 0.95 * cm, 0.95 * cm, 1.15 * cm],
            rowHeights=[0.55 * cm] + [0.5 * cm] * (end - start + 1),
        )
        tbl.setStyle(TableStyle([
            # Cabeçalho
            ("BACKGROUND", (0, 0), (-1, 0), SLATE),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
            # Corpo
            ("FONT", (0, 1), (-1, -1), "Helvetica", 9.5),
            ("FONT", (0, 1), (0, -1), "Helvetica-Bold", 9.5),
            ("FONT", (2, 1), (2, -1), "Helvetica-Bold", 9.5),
            # Realces
            ("BACKGROUND", (2, 1), (2, -1), GRAY_LIGHT),
            ("BACKGROUND", (4, 1), (4, -1), GRAY_LIGHT),
            # Bordas
            ("GRID", (0, 0), (-1, -1), 0.5, GRAY_MID),
            # Alinhamento
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]))
        return tbl

    tblock1 = build_teacher_block(1, 10)
    tblock2 = build_teacher_block(11, 20)
    teacher_width = 5.15 * cm
    side = Table(
        [[tblock1, "", tblock2]],
        colWidths=[teacher_width, 1.0 * cm, teacher_width],
    )
    side.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    centered_t = Table([[side]], colWidths=[16.5 * cm])
    centered_t.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(centered_t)
    elems.append(Spacer(1, 8))

    # ---------- SUBTOTAIS ----------
    subtot_header = [
        "Subtotais por processo",
        "P0 /4", "P1 /4", "P2 /7", "P3 /4", "P4 /1",
        "TOTAL /20", "Perfil",
    ]
    subtot_body = ["", "", "", "", "", "", "", ""]
    tbl = Table(
        [subtot_header, subtot_body],
        colWidths=[3.8 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm,
                   1.5 * cm, 2.1 * cm, 2.1 * cm],
        rowHeights=[0.6 * cm, 0.85 * cm],
    )
    tbl.setStyle(TableStyle([
        # Cabeçalho
        ("BACKGROUND", (1, 0), (-1, 0), SLATE),
        ("TEXTCOLOR", (1, 0), (-1, 0), colors.white),
        ("FONT", (1, 0), (-1, 0), "Helvetica-Bold", 9),
        ("FONT", (0, 0), (0, 0), "Helvetica-Bold", 9.5),
        ("TEXTCOLOR", (0, 0), (0, 0), SLATE),
        ("BACKGROUND", (0, 0), (0, 0), GRAY_LIGHT),
        # Bordas
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY_MID),
        # Alinhamento
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elems.append(tbl)

    return elems


def add_questions(elems, questions):
    for num, stem, alts in questions:
        block = [Paragraph(f"<b>{num}</b>&nbsp;&nbsp;{stem}", S["question_stem"])]
        for a in alts:
            block.append(Paragraph(a, S["alt"]))
        elems.append(KeepTogether(block))


# =============================================================================
# PDF 2 — GUIA DO PROFESSOR
# =============================================================================

def build_guia(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=2.0 * cm, rightMargin=2.0 * cm,
        topMargin=2.0 * cm, bottomMargin=2.0 * cm,
        title="LEIA! — Levantamento Integrado de Avaliação em Leitura",
        author="Rodrigo Leão",
    )
    elems = []

    # === CAPA ===
    elems.append(Paragraph("VOLUME II", S["volume"]))
    elems.append(Paragraph("LEIA! — Levantamento Integrado de Avaliação em Leitura", S["cover_title"]))
    elems.append(Paragraph(
        "Manual técnico do professor — correção, classificação e análise",
        S["cover_subtitle"]
    ))
    elems.append(author_block())
    elems.append(Spacer(1, 18))
    elems.extend(technical_description(audience="professor"))
    elems.append(Spacer(1, 10))

    # Aviso de uso
    aviso = (
        "<b>Documento confidencial.</b> Este volume contém gabarito, análise "
        "de distratores e instrumentos de classificação. Não deve circular "
        "entre os alunos antes da aplicação. Acompanha o Volume I (Exame) e "
        "deve ser utilizado em conjunto com ele — todas as numerações de "
        "questões referem-se diretamente ao Volume I."
    )
    elems.append(Paragraph(aviso, S["tech_body"]))

    elems.append(PageBreak())

    # ===================== GUIA DE USO =====================
    elems.append(Paragraph("Guia de Uso", S["h1"]))

    elems.append(Paragraph("O que este documento contém", S["h3"]))
    elems.append(Paragraph(
        "Este guia acompanha o exame (Volume I) e contém tudo que o "
        "professor precisa para corrigir, classificar e interpretar os "
        "resultados — individual e coletivamente. Não é um gabarito comum: "
        "cada questão errada indica <i>o que</i> o aluno não consegue fazer "
        "com o texto, não apenas <i>que</i> ele errou.", S["body"]
    ))

    elems.append(Paragraph("O que este exame mede", S["h3"]))
    elems.append(Paragraph(
        "O exame avalia cinco níveis de operação leitora, do mais elementar "
        "ao mais complexo:", S["body"]
    ))
    levels_table = [
        [Paragraph("<b>Código</b>", S["table_header"]),
         Paragraph("<b>O que o aluno precisa fazer</b>", S["table_header"]),
         Paragraph("<b>Questões</b>", S["table_header"])],
        [Paragraph("<b>P0</b>", S["table_cell_bold"]),
         Paragraph("Identificar tema, reconhecer palavra no contexto, ordenar sequência.", S["table_cell"]),
         Paragraph("Q1–Q4", S["table_cell"])],
        [Paragraph("<b>P1</b>", S["table_cell_bold"]),
         Paragraph("Localizar informação escrita textualmente.", S["table_cell"]),
         Paragraph("Q5, Q6, Q11, Q12", S["table_cell"])],
        [Paragraph("<b>P2</b>", S["table_cell_bold"]),
         Paragraph("Ligar duas informações para chegar a conclusão não declarada.", S["table_cell"]),
         Paragraph("Q7, Q8, Q13–Q17", S["table_cell"])],
        [Paragraph("<b>P3</b>", S["table_cell_bold"]),
         Paragraph("Integrar o texto inteiro: mensagem, tom, sentimento global.", S["table_cell"]),
         Paragraph("Q9, Q10, Q18, Q19", S["table_cell"])],
        [Paragraph("<b>P4</b>", S["table_cell_bold"]),
         Paragraph("Avaliar escolha autoral e julgar sua intenção.", S["table_cell"]),
         Paragraph("Q20", S["table_cell"])],
    ]
    tbl = Table(levels_table, colWidths=[1.7 * cm, 11.0 * cm, 3.8 * cm])
    tbl.setStyle(default_table_style(header_bg=NAVY))
    elems.append(tbl)

    elems.append(Paragraph("Passo a passo de uso", S["h3"]))
    steps = [
        ("Correção.",
         "Use o Gabarito Rápido (Parte 1). Marque acerto (1) ou erro (0) na "
         "folha do aluno ou diretamente na Ficha de Registro (Parte 3)."),
        ("Pontuação por processo.",
         "Some separadamente os acertos de P0, P1, P2, P3 e P4 — não apenas "
         "o total. O total isolado não informa onde intervir; os subscores, "
         "sim."),
        ("Identificação do perfil.",
         "Com os subscores em mãos, aplique os critérios da Parte 4 para "
         "classificar cada aluno em um dos quatro perfis (A, B, C ou D). "
         "Anote o perfil na última coluna da Ficha de Registro."),
        ("Análise de turma.",
         "Calcule o percentual de acerto por processo usando as fórmulas da "
         "Parte 5. O processo com menor percentual é o ponto de partida "
         "coletivo do programa de intervenção."),
        ("Diagnóstico de erros recorrentes.",
         "Identifique as questões com maior índice de erro e consulte a "
         "Grade Diagnóstica (Parte 2) para saber qual tipo de erro domina — "
         "isso orienta a estratégia de ensino, não apenas o conteúdo."),
        ("Planejamento do segundo ciclo.",
         "Após a intervenção, use a tabela da Parte 6 para calibrar o "
         "próximo exame conforme o perfil majoritário da turma."),
    ]
    for i, (title, body) in enumerate(steps, start=1):
        elems.append(Paragraph(
            f"<b>{i}. {title}</b> {body}", S["body"]
        ))

    elems.append(Paragraph("O que este exame não faz", S["h3"]))
    elems.append(Paragraph(
        "Não produz nota para boletim. Não compara a turma com escolas ou "
        "médias externas — não há escala nacional calibrada para este "
        "nível. Produz exclusivamente um mapa de onde cada aluno está e o "
        "que o programa precisa atacar primeiro.", S["body"]
    ))

    elems.append(PageBreak())

    # ===================== PARTE 1 — GABARITO =====================
    elems.append(Paragraph("Parte 1 — Gabarito Rápido", S["h1"]))

    answers = ["B", "C", "D", "C", "B", "C", "B", "C", "C", "C",
               "B", "C", "B", "C", "C", "C", "C", "B", "C", "C"]

    # Tabela 1 — Q1 a Q10
    row_q = [Paragraph("<b>Q</b>", S["table_header"])]
    row_r = [Paragraph("<b>R</b>", S["table_header"])]
    for i in range(1, 11):
        row_q.append(Paragraph(f"<b>{i}</b>", S["table_header"]))
        row_r.append(Paragraph(
            f"<b>{answers[i-1]}</b>", S["table_cell_bold"]
        ))
    tbl = Table(
        [row_q, row_r],
        colWidths=[1.4 * cm] + [1.5 * cm] * 10,
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY_MID),
        ("BACKGROUND", (0, 1), (0, 1), GRAY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(tbl)
    elems.append(Spacer(1, 8))

    # Tabela 2 — Q11 a Q20
    row_q = [Paragraph("<b>Q</b>", S["table_header"])]
    row_r = [Paragraph("<b>R</b>", S["table_header"])]
    for i in range(11, 21):
        row_q.append(Paragraph(f"<b>{i}</b>", S["table_header"]))
        row_r.append(Paragraph(
            f"<b>{answers[i-1]}</b>", S["table_cell_bold"]
        ))
    tbl = Table(
        [row_q, row_r],
        colWidths=[1.4 * cm] + [1.5 * cm] * 10,
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY_MID),
        ("BACKGROUND", (0, 1), (0, 1), GRAY_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(tbl)

    elems.append(Spacer(1, 14))

    # Estrutura por processo
    elems.append(Paragraph("Estrutura por processo cognitivo", S["h3"]))
    proc_table = [
        [Paragraph("<b>Processo</b>", S["table_header"]),
         Paragraph("<b>Questões</b>", S["table_header"]),
         Paragraph("<b>Pontos</b>", S["table_header"])],
        [Paragraph("<b>P0</b> — Pré-benchmark", S["table_cell_bold"]),
         Paragraph("Q1, Q2, Q3, Q4", S["table_cell"]),
         Paragraph("4 pts", S["table_cell"])],
        [Paragraph("<b>P1</b> — Recuperação explícita", S["table_cell_bold"]),
         Paragraph("Q5, Q6, Q11, Q12", S["table_cell"]),
         Paragraph("4 pts", S["table_cell"])],
        [Paragraph("<b>P2</b> — Inferência direta", S["table_cell_bold"]),
         Paragraph("Q7, Q8, Q13, Q14, Q15, Q16, Q17", S["table_cell"]),
         Paragraph("7 pts", S["table_cell"])],
        [Paragraph("<b>P3</b> — Interpretar e integrar", S["table_cell_bold"]),
         Paragraph("Q9, Q10, Q18, Q19", S["table_cell"]),
         Paragraph("4 pts", S["table_cell"])],
        [Paragraph("<b>P4</b> — Avaliar e criticar", S["table_cell_bold"]),
         Paragraph("Q20", S["table_cell"]),
         Paragraph("1 pt", S["table_cell"])],
        [Paragraph("<b>TOTAL</b>", S["table_cell_bold"]),
         Paragraph("20 questões", S["table_cell"]),
         Paragraph("<b>20 pts</b>", S["table_cell_bold"])],
    ]
    tbl = Table(proc_table, colWidths=[6.0 * cm, 7.5 * cm, 3.0 * cm])
    tbl.setStyle(default_table_style(header_bg=NAVY, last_row_highlight=True))
    elems.append(tbl)

    elems.append(PageBreak())

    # ===================== PARTE 2 — GRADE DIAGNÓSTICA =====================
    elems.append(Paragraph("Parte 2 — Grade Diagnóstica Completa", S["h1"]))
    elems.append(Paragraph(
        "Para cada questão: nível, gabarito e análise dos três distratores "
        "com o erro de leitura que leva o aluno a cada alternativa incorreta.",
        S["body"]
    ))

    diagnostic_data = [
        # (Q, processo, gabarito, [(alt, erro), ...], descrição da questão, nota opcional)
        (1, "P0", "B", "Tema principal",
         [("A", "Confusão de elemento — toma personagem secundária (a gerente) como assunto central; não distingue figura principal de coadjuvante."),
          ("C", "Extrapolação — projeta sobre o texto um contexto externo (dificuldades do comércio) que ele não tematiza."),
          ("D", "Leitura parcial — prende-se ao detalhe do final (ligação para a mãe) e não identifica o evento central.")], None),
        (2, "P0", "C", "Vocabulário em contexto",
         [("A", "Inversão semântica — “distraída” é antônimo; o aluno não reconhece o campo semântico."),
          ("B", "Senso comum — “quieta” remete a comportamento esperado em entrevista, sem relação com o sentido da palavra."),
          ("D", "Palavra isolada — “experiente” aparece no cartaz (sendo negada) e é associada a “esforçada” por proximidade textual.")], None),
        (3, "P0", "D", "Sequência temporal",
         [("A", "Inversão — ocorreu por último na narrativa."),
          ("B", "Inversão — ocorreu no penúltimo momento."),
          ("C", "Inversão — encerra a narrativa.")], None),
        (4, "P0", "C", "Fato elementar (idade)",
         [("A", "Número inventado — sem base no texto."),
          ("B", "Número inventado — sem base no texto."),
          ("D", "Ignora informação explícita — “18 anos” está no primeiro período do texto.")],
         "Aluno que erra Q4 (informação na primeira linha) precisa de intervenção imediata em fluência de leitura."),
        (5, "P1", "B", "Texto do cartaz",
         [("A", "Paráfrase enganosa — inverte o sentido; o cartaz diz exatamente o contrário."),
          ("C", "Extrapolação — acrescenta cargo (estoquista) não presente no texto."),
          ("D", "Paráfrase enganosa — usa palavras do contexto (“bairro”) mas deforma o enunciado.")], None),
        (6, "P1", "C", "Local da entrevista",
         [("A", "Leitura parcial — identifica “mercado” mas não localiza o detalhe “sala nos fundos”."),
          ("B", "Confusão de cena — a calçada é onde Carla faz a ligação após a entrevista."),
          ("D", "Extrapolação — escritório externo não é mencionado.")], None),
        (7, "P2", "B", "Mãos tremendo (nervosismo)",
         [("A", "Extrapolação por senso comum — ar-condicionado associado a tremor por experiência cotidiana, sem base no texto."),
          ("C", "Extrapolação — ferida não é mencionada."),
          ("D", "Extrapolação por estereótipo — cansaço associado a sintoma físico genérico.")], None),
        (8, "P2", "C", "“Entrou sem pensar duas vezes”",
         [("A", "Leitura literal — interpreta a expressão como falta de atenção, não como expressão idiomática de prontidão."),
          ("B", "Inversão — o texto mostra o contrário; a família precisava do dinheiro."),
          ("D", "Extrapolação — não há questionamento no texto sobre o conhecimento da função.")], None),
        (9, "P3", "C", "Sentimento predominante no final",
         [("A", "Extrapolação — o texto não avalia o nível ou salário do emprego."),
          ("B", "Extrapolação — não há indicação de raiva nem de demora."),
          ("D", "Confusão de sujeito — quem se emociona é a mãe de Carla; o aluno perde a referência pronominal.")], None),
        (10, "P3", "C", "Mensagem principal",
         [("A", "Extrapolação moralizante — o texto não contém essa recomendação."),
          ("B", "Extrapolação — o texto não compara empregadores."),
          ("D", "Inversão — o texto mostra que a entrevista gerou nervosismo; o aluno contradiz o texto.")], None),
        (11, "P1", "B", "Número de verificações diárias",
         [("A", "Confusão numérica — número não presente no texto; provável leitura rápida."),
          ("C", "Arredondamento indevido — aproxima 96 para 100, revelando leitura imprecisa."),
          ("D", "Ignora informação explícita — o dado está claramente no texto.")], None),
        (12, "P1", "C", "O que provoca dopamina",
         [("A", "Senso comum — vídeos associados a celular por experiência cotidiana, não pelo texto."),
          ("B", "Leitura parcial — tempo de uso é dado do texto, mas não distingue correlação de causalidade."),
          ("D", "Extrapolação — baixar aplicativos não é mencionado como gatilho.")], None),
        (13, "P2", "B", "Justificativa da comparação com vício",
         [("A", "Extrapolação — preço do celular não é mencionado; uso de conhecimento externo."),
          ("C", "Extrapolação — o texto não diz que as redes sociais impõem acesso diário obrigatório."),
          ("D", "Leitura parcial — dormir menos é efeito possível, mas não é a justificativa usada no texto.")], None),
        (14, "P2", "C", "“Hábito vira automático”",
         [("A", "Palavra isolada — “automático” lido como atributo técnico do aparelho."),
          ("B", "Palavra isolada — “automático” associado a notificações, confundindo causa e consequência."),
          ("D", "Extrapolação — o texto não afirma que o cérebro para de funcionar.")], None),
        (15, "P2", "C", "Causa da ansiedade",
         [("A", "Leitura parcial — notificações são mencionadas, mas não são a causa da ansiedade neste trecho."),
          ("B", "Extrapolação — qualidade do aparelho não é mencionada."),
          ("D", "Extrapolação — falta de sinal não aparece no texto.")], None),
        (16, "P2", "C", "Verificações sem notificação",
         [("A", "Extrapolação técnica — falha nas notificações não é mencionada; busca explicação técnica para fenômeno psicológico."),
          ("B", "Inversão — desativar notificações é o contrário da situação descrita."),
          ("D", "Extrapolação — problema de sinal não tem relação com o trecho.")], None),
        (17, "P2", "C", "Função das pesquisas no texto",
         [("A", "Extrapolação — o texto não restringe o problema a países ricos."),
          ("B", "Extrapolação — o texto não compara jovens de diferentes nacionalidades."),
          ("D", "Extrapolação — ausência de pesquisas brasileiras não é mencionada.")], None),
        (18, "P3", "B", "Ideia central do texto",
         [("A", "Extrapolação radicalizante — o texto não propõe proibição; o aluno amplifica."),
          ("C", "Leitura parcial — dopamina é mencionada, mas o aluno distorce sua função argumentativa."),
          ("D", "Extrapolação de intenção — o texto não atribui intenção maliciosa de forma absoluta.")], None),
        (19, "P3", "C", "Tom do texto",
         [("A", "Extrapolação avaliativa — confunde apresentação de dados preocupantes com alarmismo."),
          ("B", "Extrapolação — não há registro humorístico no texto."),
          ("D", "Extrapolação — o texto não menciona o passado pré-celular.")], None),
        (20, "P4", "C", "Análise do verbo “explorar”",
         [("A", "Inversão de perspectiva — atribui intenção benevolente; não percebe carga negativa do verbo no contexto."),
          ("B", "Troca de sujeito — desloca o agente da ação (aplicativos) para o usuário, perdendo o ponto de vista crítico."),
          ("D", "Palavra isolada descontextualizada — associa “explorar” à ideia de território desconhecido, ignorando o contexto argumentativo.")],
         "Q20 é o único item P4. Aluno que acerta Q20 errando P3 merece atenção especial — pode ter intuição crítica sem estrutura de integração."),
    ]

    for q_num, proc, gab, desc, distratores, nota in diagnostic_data:
        # Cabeçalho da questão
        header = Paragraph(
            f"<b>Q{q_num}</b>  ·  {desc}  ·  <font color='#6b3410'>"
            f"<b>{proc}</b></font>  ·  Gabarito: <b>{gab}</b>",
            S["h3"]
        )
        # Tabela com os 3 distratores
        rows = [[
            Paragraph("<b>Alt.</b>", S["table_header"]),
            Paragraph("<b>Erro diagnóstico</b>", S["table_header"]),
        ]]
        for alt, err in distratores:
            rows.append([
                Paragraph(f"<b>{alt}</b>", S["table_cell_bold"]),
                Paragraph(err, S["table_cell"]),
            ])
        tbl = Table(rows, colWidths=[1.3 * cm, 15.2 * cm])
        tbl.setStyle(default_table_style(header_bg=SLATE))

        block = [header, tbl]
        if nota:
            block.append(Spacer(1, 4))
            block.append(Paragraph(
                f"<i>Observação:</i> {nota}", S["small_just"]
            ))
        block.append(Spacer(1, 8))
        elems.append(KeepTogether(block))

    elems.append(PageBreak())

    # ===================== PARTE 3 — FICHA DE REGISTRO =====================
    elems.append(Paragraph("Parte 3 — Ficha de Registro por Aluno", S["h1"]))
    elems.append(Paragraph(
        "Registre o número de acertos de cada aluno em cada bloco de "
        "processo. Some a linha para obter o total. Compare os totais das "
        "colunas para identificar onde a turma mais erra. Esta ficha foi "
        "dimensionada para até 35 alunos — se a turma for maior, anexe "
        "página adicional.", S["body"]
    ))

    # Cabeçalho da ficha
    elems.append(Spacer(1, 6))
    ficha_top = [
        ["Turma:", "_______________________", "Data:", "______ / ______ / __________"],
        ["Professor(a):", "Rodrigo Leão", "Aplicação:", "_____________________________"],
    ]
    tbl = Table(ficha_top, colWidths=[2.5 * cm, 6.5 * cm, 2.5 * cm, 5.0 * cm])
    tbl.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 9),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9),
        ("FONT", (2, 0), (2, -1), "Helvetica-Bold", 9),
        ("TEXTCOLOR", (0, 0), (0, -1), SLATE),
        ("TEXTCOLOR", (2, 0), (2, -1), SLATE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    elems.append(tbl)
    elems.append(Spacer(1, 8))

    # Tabela da ficha
    header = [
        Paragraph("<b>Nº</b>", S["table_header"]),
        Paragraph("<b>Nome do aluno</b>", S["table_header"]),
        Paragraph("<b>P0</b><br/>/4", S["table_header"]),
        Paragraph("<b>P1</b><br/>/4", S["table_header"]),
        Paragraph("<b>P2</b><br/>/7", S["table_header"]),
        Paragraph("<b>P3</b><br/>/4", S["table_header"]),
        Paragraph("<b>P4</b><br/>/1", S["table_header"]),
        Paragraph("<b>Total</b><br/>/20", S["table_header"]),
        Paragraph("<b>Perfil</b>", S["table_header"]),
    ]
    ficha = [header]
    for i in range(1, 36):
        ficha.append([
            Paragraph(str(i), S["table_cell"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
        ])
    # Linhas de soma
    ficha.append([
        Paragraph("", S["table_cell"]),
        Paragraph("<b>SOMA DA TURMA</b>", S["table_cell_bold"]),
    ] + [Paragraph("", S["table_cell"]) for _ in range(7)])
    ficha.append([
        Paragraph("", S["table_cell"]),
        Paragraph("<b>MÉDIA DA TURMA</b>", S["table_cell_bold"]),
    ] + [Paragraph("", S["table_cell"]) for _ in range(7)])
    ficha.append([
        Paragraph("", S["table_cell"]),
        Paragraph("<b>% DE ACERTO</b>", S["table_cell_bold"]),
    ] + [Paragraph("", S["table_cell"]) for _ in range(7)])

    col_widths = [
        0.9 * cm,  # nº
        5.5 * cm,  # nome
        1.1 * cm,  # P0
        1.1 * cm,  # P1
        1.1 * cm,  # P2
        1.1 * cm,  # P3
        1.1 * cm,  # P4
        1.4 * cm,  # total
        1.7 * cm,  # perfil
    ]
    tbl = Table(ficha, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, GRAY_MID),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, -3), (-1, -1), GRAY_LIGHT),
    ]))
    elems.append(tbl)

    elems.append(PageBreak())

    # ===================== PARTE 4 — PERFIS =====================
    elems.append(Paragraph("Parte 4 — Classificação de Perfis", S["h1"]))
    elems.append(Paragraph(
        "Aplique os critérios abaixo para preencher a coluna PERFIL na "
        "Ficha de Registro.", S["body"]
    ))

    perfis = [
        ("Perfil A", "Falha em identificação elementar",
         "P0 ≤ 2 pontos (erra 2 ou mais dos 4 itens básicos)",
         "O aluno não consegue identificar o tema do texto, não reconhece "
         "palavras no contexto ou não organiza a sequência de eventos. A "
         "dificuldade está no nível da frase ou do período — anterior à "
         "compreensão de parágrafo.",
         "Prioridade máxima. Intervenção em vocabulário funcional, fluência "
         "oral e leitura em voz alta de textos curtos."),
        ("Perfil B", "Lê frases, não integra o parágrafo",
         "P0 ≥ 3  E  P1 ≤ 2 pontos",
         "O aluno localiza elementos básicos do texto mas não recupera "
         "informações explícitas com precisão. Lê segmentos isolados; perde "
         "detalhes ao percorrer o texto inteiro.",
         "Prioridade alta. Exercícios de localização de informação, "
         "sublinhado guiado, leitura com perguntas de ancoragem (“Onde está "
         "escrito isso?”)."),
        ("Perfil C", "Compreende dados, não constrói sentido global",
         "P0 ≥ 3  E  P1 ≥ 3  E  P2 ≤ 4 pontos",
         "O aluno recupera informações explícitas, mas não conecta duas "
         "informações para fazer uma inferência simples. Lê o texto como "
         "lista de fatos, sem relações de causa, consequência ou intenção.",
         "Prioridade média-alta. Exercícios de inferência com pares de frases, "
         "identificação de causa e efeito, perguntas “Por quê?” com resposta "
         "ancorável no texto."),
        ("Perfil D", "Compreensão funcional em desenvolvimento",
         "P0 ≥ 3  E  P1 ≥ 3  E  P2 ≥ 5",
         "O aluno localiza informações explícitas e faz inferências diretas "
         "com consistência — Benchmark Intermediário PIRLS (475). "
         "P3 ≥ 2: integração global emergindo, aproximando-se do Benchmark "
         "Alto (550). P3 ≤ 1: consolidado no Intermediário, ainda sem síntese "
         "do texto como unidade — requer intervenção antes de avançar para P4.",
         "Diferenciada conforme P3. "
         "P3 ≥ 2: textos mais longos, exercícios de síntese, identificação "
         "de ponto de vista e intenção do autor. "
         "P3 ≤ 1: sumarização, ideia principal, perguntas de sentido global — "
         "antes de avançar para leitura crítica."),
    ]

    for label, subtitle, criterio, indica, prioridade in perfis:
        rows = [[
            Paragraph(f"<b>{label}</b><br/><font size='9'>{subtitle}</font>",
                      S["table_cell_bold"]),
            Paragraph(f"<b>Critério:</b> {criterio}", S["table_cell"]),
        ], [
            Paragraph("", S["table_cell"]),
            Paragraph(f"<b>O que indica:</b> {indica}", S["table_cell"]),
        ], [
            Paragraph("", S["table_cell"]),
            Paragraph(f"<b>No programa:</b> {prioridade}", S["table_cell"]),
        ]]
        tbl = Table(rows, colWidths=[4.5 * cm, 12.0 * cm])
        tbl.setStyle(TableStyle([
            ("SPAN", (0, 0), (0, 2)),
            ("BACKGROUND", (0, 0), (0, 2), GRAY_LIGHT),
            ("LINEBEFORE", (0, 0), (0, 2), 2.5, ACCENT),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("BOX", (0, 0), (-1, -1), 0.4, GRAY_MID),
            ("INNERGRID", (1, 0), (-1, -1), 0.3, GRAY_LIGHT),
        ]))
        elems.append(KeepTogether([tbl, Spacer(1, 8)]))

    elems.append(Paragraph("Padrões atípicos dentro dos perfis", S["h3"]))
    elems.append(Paragraph(
        "Alguns alunos apresentam subscores que destoam do padrão esperado "
        "para o perfil classificado. Os casos abaixo têm implicação "
        "pedagógica real.", S["body"]
    ))

    mistos_header = [
        Paragraph("<b>Perfil</b>", S["table_header"]),
        Paragraph("<b>Padrão atípico</b>", S["table_header"]),
        Paragraph("<b>Sinal diagnóstico</b>", S["table_header"]),
        Paragraph("<b>Observação para o programa</b>", S["table_header"]),
    ]
    mistos_rows = [
        [Paragraph("<b>A</b>", S["table_cell_bold"]),
         Paragraph("P0 baixo + acerto isolado em P2 ou P3", S["table_cell"]),
         Paragraph("Lampejo interpretativo encoberto por falha de fluência", S["table_cell"]),
         Paragraph("Testar compreensão oral antes de assumir déficit cognitivo; intervenção primária é fluência.", S["table_cell"])],
        [Paragraph("<b>B</b>", S["table_cell_bold"]),
         Paragraph("P1 baixo + P2 relativamente alto", S["table_cell"]),
         Paragraph("Lê por contexto e antecipação, não por localização precisa", S["table_cell"]),
         Paragraph("Exercícios de rastreamento (“Onde está escrito isso?”); problema de precisão, não de compreensão geral.", S["table_cell"])],
        [Paragraph("<b>C</b>", S["table_cell_bold"]),
         Paragraph("P2 parcial + P3 alto", S["table_cell"]),
         Paragraph("Leitor holístico: integra globalmente sem rastrear inferências diretas", S["table_cell"]),
         Paragraph("Reforçar P2 com relações causa-efeito antes de avançar; não tratar como déficit grave.", S["table_cell"])],
        [Paragraph("<b>D</b>", S["table_cell_bold"]),
         Paragraph("P2 alto + P3 = 0", S["table_cell"]),
         Paragraph("Benchmark Intermediário consolidado sem integração global", S["table_cell"]),
         Paragraph("Ver subdivisão interna do Perfil D acima.", S["table_cell"])],
    ]
    tbl_mistos = Table(
        [mistos_header] + mistos_rows,
        colWidths=[1.5 * cm, 3.8 * cm, 4.8 * cm, 6.4 * cm],
    )
    tbl_mistos.setStyle(default_table_style(header_bg=SLATE))
    elems.append(tbl_mistos)

    elems.append(PageBreak())

    # ===================== PARTE 5 — ANÁLISE DE TURMA =====================
    elems.append(Paragraph("Parte 5 — Análise de Turma", S["h1"]))
    elems.append(Paragraph(
        "Após preencher a Ficha de Registro, calcule o percentual de acerto "
        "por processo.", S["body"]
    ))

    formulas = [
        "% acerto P0  =  (Soma P0 da turma)  ÷  (nº de alunos × 4)  × 100",
        "% acerto P1  =  (Soma P1 da turma)  ÷  (nº de alunos × 4)  × 100",
        "% acerto P2  =  (Soma P2 da turma)  ÷  (nº de alunos × 7)  × 100",
        "% acerto P3  =  (Soma P3 da turma)  ÷  (nº de alunos × 4)  × 100",
        "% acerto P4  =  (Soma P4 da turma)  ÷  (nº de alunos × 1)  × 100",
    ]
    formula_rows = [[Paragraph(
        f"<font face='Courier'>{f}</font>", S["table_cell"]
    )] for f in formulas]
    tbl = Table(formula_rows, colWidths=[16.5 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRAY_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.4, GRAY_MID),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(tbl)

    elems.append(Paragraph("Leitura dos resultados da turma", S["h3"]))
    rows = [
        [Paragraph("<b>% de acerto</b>", S["table_header"]),
         Paragraph("<b>Interpretação</b>", S["table_header"]),
         Paragraph("<b>Ação no programa</b>", S["table_header"])],
        [Paragraph("Abaixo de 50%", S["table_cell_bold"]),
         Paragraph("Fragilidade coletiva neste processo.", S["table_cell"]),
         Paragraph("Intervenção coletiva obrigatória.", S["table_cell"])],
        [Paragraph("Entre 50% e 75%", S["table_cell_bold"]),
         Paragraph("Desenvolvimento parcial.", S["table_cell"]),
         Paragraph("Reforço em grupos menores.", S["table_cell"])],
        [Paragraph("Acima de 75%", S["table_cell_bold"]),
         Paragraph("Processo consolidado na turma.", S["table_cell"]),
         Paragraph("Avançar para o próximo nível.", S["table_cell"])],
    ]
    tbl = Table(rows, colWidths=[3.5 * cm, 6.0 * cm, 7.0 * cm])
    tbl.setStyle(default_table_style(header_bg=NAVY))
    elems.append(tbl)

    elems.append(Paragraph("Questões com maior índice de erro", S["h3"]))
    elems.append(Paragraph(
        "Identifique as 3 questões com menor % de acerto na turma. Elas "
        "revelam:", S["body"]
    ))
    bullets = [
        "O ponto exato de ruptura de compreensão mais frequente.",
        "O tipo de erro predominante — consulte a Parte 2 para o diagnóstico de cada distrator.",
        "O foco prioritário das primeiras aulas do programa.",
    ]
    for b in bullets:
        elems.append(Paragraph(f"·&nbsp;&nbsp;{b}", S["body_indent"]))

    # Quadro para anotar
    elems.append(Spacer(1, 8))
    elems.append(Paragraph("Registro das 3 questões críticas", S["h3"]))
    rows = [
        [Paragraph("<b>Posição</b>", S["table_header"]),
         Paragraph("<b>Nº da questão</b>", S["table_header"]),
         Paragraph("<b>% de acerto</b>", S["table_header"]),
         Paragraph("<b>Processo</b>", S["table_header"]),
         Paragraph("<b>Erro predominante observado</b>", S["table_header"])],
    ]
    for pos in ["1ª", "2ª", "3ª"]:
        rows.append([
            Paragraph(f"<b>{pos}</b>", S["table_cell_bold"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
            Paragraph("", S["table_cell"]),
        ])
    tbl = Table(rows, colWidths=[1.5 * cm, 2.2 * cm, 2.2 * cm, 2.0 * cm, 8.6 * cm])
    tbl.setStyle(default_table_style(header_bg=NAVY))
    elems.append(tbl)

    elems.append(PageBreak())

    # ===================== PARTE 6 — SEGUNDO CICLO =====================
    elems.append(Paragraph("Parte 6 — Calibração do Segundo Ciclo", S["h1"]))
    elems.append(Paragraph(
        "Após a aplicação do programa de intervenção, o segundo exame deve "
        "ser ajustado conforme o perfil majoritário observado nesta "
        "aplicação.", S["body"]
    ))
    rows = [
        [Paragraph("<b>Condição observada no 1º exame</b>", S["table_header"]),
         Paragraph("<b>Ajuste no 2º exame</b>", S["table_header"])],
        [Paragraph("Maioria no Perfil A", S["table_cell_bold"]),
         Paragraph("Manter textos curtos; aumentar P0 e P1; introduzir 2 "
                   "questões P2.", S["table_cell"])],
        [Paragraph("Maioria no Perfil B / C", S["table_cell_bold"]),
         Paragraph("Aumentar textos para 300–400 palavras; ampliar P2 e P3; "
                   "reduzir P0.", S["table_cell"])],
        [Paragraph("Maioria no Perfil D", S["table_cell_bold"]),
         Paragraph("Textos de 400–600 palavras; inserir texto argumentativo; "
                   "aumentar P3 e P4.", S["table_cell"])],
        [Paragraph("Distribuição mista A + D", S["table_cell_bold"]),
         Paragraph("Dois cadernos de prova com dificuldades distintas — "
                   "grupo de reforço e grupo avançado.", S["table_cell"])],
    ]
    tbl = Table(rows, colWidths=[5.0 * cm, 11.5 * cm])
    tbl.setStyle(default_table_style(header_bg=NAVY))
    elems.append(tbl)

    elems.append(Spacer(1, 18))
    elems.append(HRFlowable(width="100%", thickness=0.4, color=GRAY_LIGHT))
    elems.append(Paragraph(
        "<i>Exame elaborado com base no PIRLS 2021 Assessment Framework "
        "(IEA / Boston College), adaptado para populações com defasagem "
        "severa no Ensino Médio.</i>", S["small"]
    ))

    decorator = make_page_decorator("LEIA!", "Levantamento Integrado de Avaliação em Leitura")
    doc.build(elems, onFirstPage=decorator, onLaterPages=decorator)


def default_table_style(header_bg=NAVY, last_row_highlight=False):
    s = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("GRID", (0, 0), (-1, -1), 0.4, GRAY_MID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if last_row_highlight:
        s.append(("BACKGROUND", (0, -1), (-1, -1), GRAY_LIGHT))
    return TableStyle(s)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import os
    import tempfile
    from pypdf import PdfWriter, PdfReader

    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(base, "..", "exame", "pdfs")
    os.makedirs(out, exist_ok=True)

    p1 = os.path.join(out, "01-exame-proficiencia-leitura.pdf")
    p2 = os.path.join(out, "02-guia-diagnostico-professor.pdf")
    scan_sheet = os.path.join(out, "04-folha-respostas-scan.pdf")

    # Exame: gera sem folha de respostas, depois mescla com a folha OMR
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name
    build_exame(tmp_path)

    writer = PdfWriter()
    for page in PdfReader(tmp_path).pages:
        writer.add_page(page)
    for page in PdfReader(scan_sheet).pages:
        writer.add_page(page)
    with open(p1, "wb") as f:
        writer.write(f)
    os.unlink(tmp_path)

    build_guia(p2)
    print("OK:", p1)
    print("OK:", p2)
