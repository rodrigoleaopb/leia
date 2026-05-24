# LEIA! — Roadmap

---

## v1-alpha → v0-beta: Campo antes de código

A prioridade imediata não é o app — é a aplicação de campo. O instrumento foi calibrado por critério lógico, sem piloto. Os dados reais de turma vão revelar o que nenhuma análise teórica prevê: efeito chão (maioria zerando P0), distribuição atípica de erros, itens com redação ambígua, tempo real de aplicação.

**Objetivo desta fase:** acumular dados suficientes para calibrar o instrumento antes de construir a automação sobre ele.

### O que fazer nesta fase

* Aplicar em pelo menos 3 turmas com perfis distintos (defasagem severa, intermediária, mista).
* Registrar: tempo de aplicação, dúvidas recorrentes dos alunos, itens com índice de acerto acima de 90% ou abaixo de 20% (candidatos a revisão).
* Corrigir manualmente com o guia do professor e preencher a ficha de registro — esse processo revela o que a automação precisará reproduzir.
* Documentar em `CAMPO.md` (por turma): perfil majoritário, distribuição dos perfis A/B/C/D, padrões atípicos observados.

### Saída esperada

Versão revisada do instrumento (`v0-beta`) com eventuais ajustes de redação nos itens e redistribuição de P0 se o efeito chão for confirmado. Somente após esse ajuste o instrumento está estável o suficiente para ser a base do app.

---

## v1.0: App de Correção Automatizada

### Premissa técnica

A folha de respostas já foi construída com **marcas fiduciais** (quadrados pretos nos quatro cantos — `gerar_pdfs.py`, linhas 533–543). O fluxo de correção automatizada usa essas marcas para alinhar e recortar a imagem antes da leitura das marcações.

### Fluxo do app

```
Foto da folha (celular do professor)
    → Detecção das marcas fiduciais (OpenCV)
    → Correção perspectiva e recorte
    → Leitura das marcações Q1–Q20
    → Comparação com gabarito
    → Geração da ficha diagnóstica
```

### Ficha do Aluno

Para cada aluno, o app gera:

| Campo | Dado |
|---|---|
| Subscores | P0 /4 · P1 /4 · P2 /7 · P3 /4 · P4 /1 |
| Total | /20 |
| Perfil | A / B / C / D (com subdivisão de D) |
| Padrão atípico | Detectado automaticamente se houver |
| Indicação de intervenção | Texto curto vinculado ao perfil |

### Ficha de Turma

Agrega as fichas individuais e produz:

* Distribuição dos perfis (quantos A, B, C, D).
* Percentual de acerto por processo (P0 a P4) — identifica o gargalo coletivo.
* Mapa de calor por questão: quais itens concentram mais erros.
* Padrões atípicos: frequência por turma.
* Ponto de partida recomendado para o programa de intervenção.

### Stack

| Componente | Opção |
|---|---|
| Visão computacional | Python + OpenCV |
| Interface | Streamlit (web simples, sem instalação para o professor) |
| Armazenamento | SQLite local ou exportação CSV/JSON |
| Geração de relatórios | ReportLab (já em uso no projeto) |

O professor acessa pelo navegador, faz upload da foto da folha e recebe as fichas geradas — sem instalação, sem dependência de sistema operacional.

---

## v2.0+: Ciclos e Longitudinalidade

Após o app de correção estar estável:

* **Segundo exame calibrado** — instrumento para reavaliação após intervenção, com textos de 300–500 palavras e maior proporção de P3/P4.
* **Rastreamento longitudinal** — comparação do perfil do aluno entre aplicações (ponto zero → pós-intervenção).
* **Exportação para secretarias** — relatório agregado por escola ou rede, para uso em planejamento de política educacional.

---

## O que não está no roadmap (por ora)

* Questões discursivas — entram somente após o estabelecimento do perfil de base, conforme descrito na nota técnica.
* Comparação com escala PIRLS internacional — os textos são mais curtos e a distribuição de itens é distinta; a comparação seria metodologicamente indefensável nesta versão.
