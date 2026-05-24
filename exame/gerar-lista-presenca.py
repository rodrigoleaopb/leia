"""Gera lista-de-presenca.pdf no padrão visual LEIA! (reportlab)"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registra Segoe UI Symbol para renderizar ☐ corretamente no Windows
_SYM_FONT = "Helvetica"
_SYM_PATH = r"C:\Windows\Fonts\seguisym.ttf"
if os.path.exists(_SYM_PATH):
    pdfmetrics.registerFont(TTFont("SegoeSymbol", _SYM_PATH))
    _SYM_FONT = "SegoeSymbol"

# ── Paleta ───────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1e3a6e")
BLUE   = colors.HexColor("#2563a8")
LBLUE  = colors.HexColor("#c8d8ee")
FBLUE  = colors.HexColor("#f0f5fb")
TWHITE = colors.white
GRAY   = colors.HexColor("#555555")
LGRAY  = colors.HexColor("#f5f8fc")

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "pdfs", "03-lista-de-presenca.pdf")

PAGE_W, PAGE_H = A4
MARGIN_L = 18 * mm
MARGIN_R = 18 * mm
MARGIN_T = 18 * mm
MARGIN_B = 22 * mm
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

# ── Estilos ───────────────────────────────────────────────────────────────────
def st(name, **kw):
    return ParagraphStyle(name, **kw)

S_VOLUME = st("volume", fontName="Helvetica-Bold", fontSize=8,
              textColor=BLUE, leading=10, spaceAfter=2)
S_TITLE  = st("title",  fontName="Helvetica-Bold", fontSize=20,
              textColor=NAVY, leading=24, spaceAfter=3)
S_SUB    = st("sub",    fontName="Helvetica", fontSize=12,
              textColor=BLUE, leading=15, spaceAfter=0)
S_BODY   = st("body",   fontName="Helvetica", fontSize=9.5,
              textColor=colors.black, leading=12)
S_SMALL  = st("small",  fontName="Helvetica-Oblique", fontSize=8.5,
              textColor=colors.black, leading=11)
S_LABEL  = st("lbl",    fontName="Helvetica-Bold", fontSize=7,
              textColor=BLUE, leading=9)
S_TH     = st("th",     fontName="Helvetica-Bold", fontSize=9,
              textColor=TWHITE, alignment=TA_CENTER, leading=11)
S_THLEFT = st("thl",    fontName="Helvetica-Bold", fontSize=9,
              textColor=TWHITE, alignment=TA_LEFT, leading=11)
S_TLBL   = st("tlbl",   fontName="Helvetica-Bold", fontSize=9.5,
              textColor=NAVY, leading=12)
S_OBS    = st("obs",    fontName="Helvetica-Bold", fontSize=9.5,
              textColor=NAVY, leading=12, spaceAfter=3)
S_NROW   = st("nrow",   fontName="Helvetica-Bold", fontSize=8.5,
              textColor=BLUE, alignment=TA_CENTER, leading=10)

# ── Rodapé de página ─────────────────────────────────────────────────────────
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.setStrokeColor(colors.HexColor("#cccccc"))
    canvas.setLineWidth(0.5)
    y_line = MARGIN_B - 6 * mm
    canvas.line(MARGIN_L, y_line, PAGE_W - MARGIN_R, y_line)
    canvas.drawString(MARGIN_L, y_line - 4 * mm,
                      "LEIA! · Levantamento Integrado de Avaliação em Leitura")
    canvas.drawRightString(PAGE_W - MARGIN_R, y_line - 4 * mm,
                           f"página {doc.page}")
    canvas.restoreState()

# ── Helper: campo com linha sublinhada ───────────────────────────────────────
def campo_linha(label, w_label, w_line):
    inner = Table([[Paragraph(label, S_TLBL), ""]],
                  colWidths=[w_label, w_line])
    inner.setStyle(TableStyle([
        ("LINEBELOW",     (1, 0), (1, 0), 0.75, NAVY),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("VALIGN",        (0, 0), (-1, -1), "BOTTOM"),
        ("RIGHTPADDING",  (0, 0), (0, 0),   4),
    ]))
    return inner

# ── Story ────────────────────────────────────────────────────────────────────
story = []

# Cabeçalho
story.append(Paragraph("LISTA DE PRESENÇA", S_VOLUME))
story.append(Paragraph(
    "LEIA! — Levantamento Integrado de Avaliação em Leitura", S_TITLE))
story.append(Paragraph("Avaliação Diagnóstica — Ensino Médio", S_SUB))
story.append(Spacer(1, 6))

# Caixa do professor (compacta)
prof_data = [
    [Paragraph("PROFESSOR RESPONSÁVEL", S_LABEL)],
    [Paragraph("<b>Rodrigo Leão</b>  <i>· Professor de Ensino Médio · "
               "contato.profleao@gmail.com · youtube.com/rodrigoleaobr</i>",
               S_BODY)],
]
prof_table = Table(prof_data, colWidths=[CONTENT_W])
prof_table.setStyle(TableStyle([
    ("BOX",           (0, 0), (-1, -1), 0.75, LBLUE),
    ("BACKGROUND",    (0, 0), (-1, -1), FBLUE),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 9),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 9),
]))
story.append(prof_table)
story.append(Spacer(1, 7))

# Campos — linha 1: Data | Turma | Série
W3 = CONTENT_W / 3
campos_l1 = Table([[
    campo_linha("Data:",  18*mm, W3 - 22*mm),
    campo_linha("Turma:", 20*mm, W3 - 24*mm),
    campo_linha("Série:", 18*mm, W3 - 22*mm),
]], colWidths=[W3, W3, W3])
campos_l1.setStyle(TableStyle([
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
]))
story.append(campos_l1)
story.append(Spacer(1, 6))

# Campos — linha 2: Professor | Sala
W_PROF = CONTENT_W * 0.72
W_SALA = CONTENT_W * 0.28
campos_l2 = Table([[
    campo_linha("Professor(a):", 30*mm, W_PROF - 34*mm),
    campo_linha("Sala:",         14*mm, W_SALA - 18*mm),
]], colWidths=[W_PROF, W_SALA])
campos_l2.setStyle(TableStyle([
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
]))
story.append(campos_l2)
story.append(Spacer(1, 6))

# Turno — usa SegoeSymbol para renderizar ☐ vazio
def turno_opt(label):
    cb = f'<font name="{_SYM_FONT}">☐</font>'
    return Paragraph(f"{cb}  {label}", S_BODY)

turno_t = Table([[
    Paragraph("<b>Turno:</b>", S_TLBL),
    turno_opt("Matutino"),
    turno_opt("Vespertino"),
    turno_opt("Noturno"),
]], colWidths=[20*mm, 38*mm, 42*mm, 38*mm])
turno_t.setStyle(TableStyle([
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
]))
story.append(turno_t)
story.append(Spacer(1, 8))

# ── Tabela: Nº | Nome completo | Assinatura ──────────────────────────────────
COL_NUM  = 13 * mm
COL_ASS  = 62 * mm
COL_NOME = CONTENT_W - COL_NUM - COL_ASS

header = [
    Paragraph("Nº",            S_TH),
    Paragraph("Nome completo", S_THLEFT),
    Paragraph("Assinatura",    S_TH),
]
col_widths = [COL_NUM, COL_NOME, COL_ASS]

table_data = [header]
for i in range(1, 41):
    table_data.append([Paragraph(f"{i:02d}", S_NROW), "", ""])

ROW_H = 7.5 * mm
pres_table = Table(table_data, colWidths=col_widths,
                   rowHeights=[None] + [ROW_H] * 40,
                   repeatRows=1)

ts = TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), NAVY),
    ("TOPPADDING",    (0, 0), (-1, 0), 5),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
    ("ALIGN",         (0, 0), (-1, 0), "CENTER"),
    ("ALIGN",         (1, 0), (1, 0),  "LEFT"),
    ("LEFTPADDING",   (1, 0), (1, 0),  6),
    ("LINEBELOW",     (0, 0), (-1, 0), 0.5, NAVY),
    ("GRID",          (0, 1), (-1, -1), 0.5, LBLUE),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN",         (0, 1), (0, -1), "CENTER"),
    ("TOPPADDING",    (0, 1), (-1, -1), 1),
    ("BOTTOMPADDING", (0, 1), (-1, -1), 1),
    ("LEFTPADDING",   (1, 1), (1, -1), 6),
])
for i in range(2, 41, 2):
    ts.add("BACKGROUND", (0, i), (-1, i), LGRAY)

pres_table.setStyle(ts)
story.append(pres_table)
story.append(Spacer(1, 5))

# ── Totalizadores ─────────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=0.75, color=LBLUE, spaceAfter=6))

W_TOT = CONTENT_W / 3
totais_t = Table([[
    campo_linha("Total matriculados:", 36*mm, W_TOT - 42*mm),
    campo_linha("Presentes:",          22*mm, W_TOT - 28*mm),
    campo_linha("Ausentes:",           22*mm, W_TOT - 28*mm),
]], colWidths=[W_TOT, W_TOT, W_TOT])
totais_t.setStyle(TableStyle([
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
]))
story.append(totais_t)
story.append(Spacer(1, 8))

# ── Observações ───────────────────────────────────────────────────────────────
story.append(Paragraph("Observações:", S_OBS))
for _ in range(2):
    story.append(HRFlowable(width="100%", thickness=0.75, color=GRAY,
                             spaceAfter=9))
story.append(Spacer(1, 5))

# ── Rodapé do formulário (2 linhas: assinatura / horários) ───────────────────
W_HOR = 38 * mm

rodape_ass = Table([[
    campo_linha("Assinatura do(a) professor(a):", 62*mm, CONTENT_W - 66*mm),
]], colWidths=[CONTENT_W])
rodape_ass.setStyle(TableStyle([
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
]))
story.append(rodape_ass)
story.append(Spacer(1, 6))

W_HALF = CONTENT_W / 2
rodape_hor = Table([[
    campo_linha("Horário de início:",  40*mm, W_HALF - 44*mm),
    campo_linha("Horário de término:", 42*mm, W_HALF - 46*mm),
]], colWidths=[W_HALF, W_HALF])
rodape_hor.setStyle(TableStyle([
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING",    (0, 0), (-1, -1), 0),
    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
]))
story.append(rodape_hor)

# ── Geração ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    leftMargin=MARGIN_L,
    rightMargin=MARGIN_R,
    topMargin=MARGIN_T,
    bottomMargin=MARGIN_B,
    title="LEIA! — Lista de Presença",
    author="Rodrigo Leão",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"OK · {OUTPUT_PATH}")
