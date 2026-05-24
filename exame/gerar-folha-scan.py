"""Gera folha de respostas com bolhas para escaneamento — LEIA! v0-alpha"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas as pdfcanvas

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "pdfs", "04-folha-respostas-scan.pdf")

PW, PH = A4   # pontos: 595.28 × 841.89

# ── Paleta ────────────────────────────────────────────────────────────────────
NAVY  = colors.HexColor("#1e3a6e")
BLUE  = colors.HexColor("#2563a8")
LBLUE = colors.HexColor("#c8d8ee")
FBLUE = colors.HexColor("#f0f5fb")
GRAY  = colors.HexColor("#555555")
BLACK = colors.black
WHITE = colors.white

# ── Bolha ─────────────────────────────────────────────────────────────────────
BR   = 4.6 * mm   # raio
BGAP = 12.4 * mm  # espaçamento centro a centro

# ── Marcadores de canto (quadrados sólidos) ───────────────────────────────────
RM   = 8.0 * mm   # tamanho do marcador
RO   = 9.5 * mm   # recuo da borda da página

# ── Processo por questão ──────────────────────────────────────────────────────
PROC = [None,
    'P0','P0','P0','P0',
    'P1','P1',
    'P2','P2',
    'P3','P3',
    'P1','P1',
    'P2','P2','P2','P2','P2',
    'P3','P3',
    'P4'
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def set_fill(c, col):
    c.setFillColor(col)

def set_stroke(c, col):
    c.setStrokeColor(col)

def bolha(c, cx, cy):
    """
    Círculo branco com contorno navy.
    A letra é desenhada centralmente dentro do círculo.
    Parâmetros: cx, cy em pontos (centro da bolha).
    Retorna função para desenhar a letra — chamada separada para
    garantir que o texto fique por cima do círculo.
    """
    set_fill(c, WHITE)
    set_stroke(c, NAVY)
    c.setLineWidth(0.85)
    c.circle(cx, cy, BR, fill=1, stroke=1)

def letra_bolha(c, cx, cy, letter):
    """Letra centrada dentro da bolha já desenhada."""
    c.setFont("Helvetica-Bold", 8.5)
    set_fill(c, NAVY)
    # Ajuste: -1.1mm centraliza visualmente a cap-height do caractere
    c.drawCentredString(cx, cy - 1.1 * mm, letter)

def campo_id(c, label, x, y, line_end):
    """Label negrito + linha de preenchimento."""
    c.setFont("Helvetica-Bold", 8)
    set_fill(c, NAVY)
    c.drawString(x, y, label)
    lx = x + c.stringWidth(label, "Helvetica-Bold", 8) + 1.5 * mm
    set_stroke(c, NAVY)
    c.setLineWidth(0.65)
    c.line(lx, y - 0.8 * mm, line_end, y - 0.8 * mm)

def reg_marks(c):
    """4 quadrados sólidos nos cantos — referência de perspectiva para o scanner.
    Cada marcador tem fundo branco garantindo contraste máximo sobre qualquer cor."""
    PAD = 1.5 * mm   # margem branca ao redor do quadrado negro
    corners = [
        (RO,           PH - RO - RM),   # ↖
        (PW - RO - RM, PH - RO - RM),   # ↗
        (RO,           RO),              # ↙
        (PW - RO - RM, RO),              # ↘
    ]
    for (x, y) in corners:
        # Fundo branco (garante contraste mesmo sobre o header navy)
        set_fill(c, WHITE)
        c.rect(x - PAD, y - PAD, RM + 2*PAD, RM + 2*PAD, fill=1, stroke=0)
        # Quadrado negro
        set_fill(c, BLACK)
        c.rect(x, y, RM, RM, fill=1, stroke=0)
        # Cruz branca de centro (auxilia detecção sub-pixel)
        set_stroke(c, WHITE)
        c.setLineWidth(0.45)
        cx, cy = x + RM / 2, y + RM / 2
        c.line(cx - 2*mm, cy, cx + 2*mm, cy)
        c.line(cx, cy - 2*mm, cx, cy + 2*mm)

# ═══════════════════════════════════════════════════════════════════════════════
# GERAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

def gerar():
    c = pdfcanvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle("LEIA! — Folha de Respostas · Escaneamento")
    c.setAuthor("Rodrigo Leão")

    # ── Marcadores de canto
    reg_marks(c)

    # ── Cabeçalho navy ────────────────────────────────────────────────────────
    HEADER_H = 22 * mm
    set_fill(c, NAVY)
    c.rect(0, PH - HEADER_H, PW, HEADER_H, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 13.5)
    set_fill(c, WHITE)
    c.drawString(15 * mm, PH - 11 * mm, "LEIA! — Folha de Respostas")
    c.setFont("Helvetica", 8)
    set_fill(c, LBLUE)
    c.drawString(15 * mm, PH - 18 * mm,
        "Levantamento Integrado de Avaliação em Leitura · v0-alpha · Escaneamento")

    # ── Caixa de identificação ────────────────────────────────────────────────
    ID_TOP  = PH - HEADER_H - 2 * mm
    ID_H    = 26 * mm
    set_fill(c, FBLUE)
    set_stroke(c, LBLUE)
    c.setLineWidth(0.5)
    c.roundRect(14 * mm, ID_TOP - ID_H, PW - 28 * mm, ID_H, 2 * mm, fill=1, stroke=1)

    y1 = ID_TOP - 9 * mm
    campo_id(c, "Aluno(a):", 18*mm, y1, 115*mm)
    campo_id(c, "Turma:",    122*mm, y1, 152*mm)
    campo_id(c, "Nº:",       158*mm, y1, 178*mm)

    y2 = ID_TOP - 20 * mm
    campo_id(c, "Escola:",   18*mm,  y2, 108*mm)
    campo_id(c, "Data:",     115*mm, y2, 150*mm)
    campo_id(c, "Idade:",    157*mm, y2, 178*mm)

    # ── Instrução ─────────────────────────────────────────────────────────────
    y_inst = ID_TOP - ID_H - 5 * mm
    c.setFont("Helvetica-Bold", 7)
    set_fill(c, NAVY)
    c.drawString(15 * mm, y_inst, "INSTRUÇÃO:")
    c.setFont("Helvetica", 7)
    set_fill(c, GRAY)
    c.drawString(15 * mm, y_inst - 4 * mm,
        "Preencha completamente a bolha da alternativa escolhida com caneta azul ou preta. "
        "Não rasure. Uma única bolha por questão.")

    # ── Grade de questões — 2 colunas de 10 ──────────────────────────────────
    Q_TOP   = y_inst - 10 * mm    # topo da área de questões
    ROW_H   = 10.4 * mm           # altura de cada linha
    QL_W    = 15 * mm             # largura do label "Q01"
    PROC_W  =  8 * mm             # largura do badge de processo
    COL_PAD =  3 * mm             # espaço entre label+proc e primeira bolha

    # Início das bolhas (da borda esquerda da coluna)
    BUBBLES_X0 = QL_W + PROC_W + COL_PAD + BR  # centro da 1ª bolha

    # Largura total de uma coluna (label + proc + gap + 4 bolhas)
    COL_W = QL_W + PROC_W + COL_PAD + 4 * BGAP + BR

    COL1_X = 15 * mm
    COL2_X = PW / 2 + 5 * mm

    # Cabeçalho de coluna
    for col in range(2):
        xc = COL1_X if col == 0 else COL2_X
        y_head = Q_TOP - 2 * mm

        # Fundo azul no cabeçalho
        set_fill(c, NAVY)
        c.rect(xc - 1*mm, y_head - 5*mm, COL_W + 2*mm, 7*mm, fill=1, stroke=0)

        c.setFont("Helvetica-Bold", 7.5)
        set_fill(c, WHITE)
        c.drawString(xc + 1*mm, y_head - 1.5*mm, "Questão")

        for i, lt in enumerate("ABCD"):
            bx = xc + BUBBLES_X0 + i * BGAP
            c.drawCentredString(bx, y_head - 1.5*mm, lt)

    # Linhas de questões
    for col in range(2):
        xc   = COL1_X if col == 0 else COL2_X
        qbase = col * 10 + 1

        for i in range(10):
            q   = qbase + i
            y_r = Q_TOP - 9 * mm - i * ROW_H   # topo da linha
            cy  = y_r - ROW_H / 2 + 1 * mm     # centro vertical

            # Fundo alternado
            if i % 2 == 1:
                set_fill(c, FBLUE)
                c.rect(xc - 1*mm, y_r - ROW_H, COL_W + 2*mm, ROW_H, fill=1, stroke=0)

            # Borda inferior da linha
            set_stroke(c, LBLUE)
            c.setLineWidth(0.3)
            c.line(xc - 1*mm, y_r - ROW_H, xc + COL_W + 1*mm, y_r - ROW_H)

            # Label Q01..Q20
            c.setFont("Helvetica-Bold", 9)
            set_fill(c, NAVY)
            c.drawString(xc, cy + 1.2*mm, f"Q{q:02d}")

            # Badge de processo (P0, P1…)
            px = xc + QL_W
            set_fill(c, LBLUE)
            c.roundRect(px, cy - 1.5*mm, PROC_W - 1*mm, 5.5*mm, 1*mm, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 6.5)
            set_fill(c, BLUE)
            c.drawCentredString(px + (PROC_W - 1*mm) / 2, cy - 0.2*mm, PROC[q])

            # 4 bolhas — primeiro desenha todos os círculos, depois as letras
            # (garante que letras ficam por cima de qualquer sobreposição)
            bxs = [xc + BUBBLES_X0 + j * BGAP for j in range(4)]
            for bx in bxs:
                bolha(c, bx, cy)
            for j, lt in enumerate("ABCD"):
                letra_bolha(c, bxs[j], cy, lt)

    # Divisória vertical entre colunas
    set_stroke(c, LBLUE)
    c.setLineWidth(0.6)
    mid_x = PW / 2
    q_bottom = Q_TOP - 9*mm - 10 * ROW_H
    c.line(mid_x, Q_TOP, mid_x, q_bottom)

    # ── Área de observações ───────────────────────────────────────────────────
    y_obs = q_bottom - 8 * mm
    set_stroke(c, LBLUE)
    c.setLineWidth(0.5)
    c.line(14*mm, y_obs, PW - 14*mm, y_obs)

    c.setFont("Helvetica-Bold", 7.5)
    set_fill(c, NAVY)
    c.drawString(15*mm, y_obs - 5*mm, "Observações:")
    set_stroke(c, GRAY)
    c.setLineWidth(0.4)
    for k in range(3):
        c.line(15*mm, y_obs - 12*mm - k * 8*mm,
               PW - 15*mm, y_obs - 12*mm - k * 8*mm)

    # ── Assinatura ────────────────────────────────────────────────────────────
    y_ass = y_obs - 40 * mm
    campo_id(c, "Assinatura do(a) aluno(a):", 15*mm, y_ass, 120*mm)

    # Nota para escaneamento
    c.setFont("Helvetica-Oblique", 6.5)
    set_fill(c, GRAY)
    c.drawCentredString(PW / 2, y_ass - 7*mm,
        "Mantenha a folha plana, sem dobras ou rasuras, para garantir a leitura correta pelo aplicativo.")

    # ── Rodapé de página ──────────────────────────────────────────────────────
    set_stroke(c, colors.HexColor("#cccccc"))
    c.setLineWidth(0.35)
    c.line(14*mm, 11*mm, PW - 14*mm, 11*mm)
    c.setFont("Helvetica", 7.5)
    set_fill(c, GRAY)
    c.drawString(14*mm, 7*mm, "LEIA! · Levantamento Integrado de Avaliação em Leitura")
    c.drawRightString(PW - 14*mm, 7*mm, "Folha de Respostas · Escaneamento · v0-alpha")

    c.save()
    print(f"OK · {OUTPUT}")

gerar()
