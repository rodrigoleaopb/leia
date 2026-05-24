# LEIA! — Levantamento Integrado de Avaliação em Leitura
### Ensino Médio — Populações com Defasagem Severa · `v1-alpha`

Instrumento diagnóstico de leitura para alunos do ensino médio com déficit severo de compreensão. Baseado na matriz de processos cognitivos do PIRLS 2021 (IEA / Boston College), adaptado para populações que operam abaixo do Benchmark Baixo internacional (400 pontos).

---
### PRIMEIRA VERSÃO (v1-alpha) DISPONÍVEL:
https://github.com/rodrigoleaopb/leia/releases/tag/v1-alpha
---

## O que é o LEIA!

Um levantamento de ponto zero: não mede onde o aluno deveria estar pelo critério curricular, mas onde ele efetivamente está. O LEIA! produz um perfil diagnóstico por aluno — identificando em qual processo cognitivo ocorre a ruptura de compreensão — e orienta diretamente a intervenção.

---

## Estrutura do repositório

```
├── nota-tecnica.md                    — fundamentação, decisões de design, limitações
├── ROADMAP.md                         — próximos passos do projeto
├── exame/
│   ├── exame-proficiencia.md          — prova do aluno (20 questões, 2 textos)
│   ├── guia-do-professor.md           — gabarito diagnóstico, perfis, ficha de registro
│   ├── lista-de-presenca.md           — lista de presença para aplicação
│   ├── gerar-lista-presenca.py        — gera pdfs/03-lista-de-presenca.pdf
│   ├── gerar-folha-scan.py            — gera pdfs/04-folha-respostas-scan.pdf
│   └── pdfs/
│       ├── 01-exame-proficiencia-leitura.pdf
│       ├── 02-guia-diagnostico-professor.pdf
│       ├── 03-lista-de-presenca.pdf   — lista de presença com assinatura
│       └── 04-folha-respostas-scan.pdf — folha OMR para leitura por câmera
├── fundamentacao/
│   ├── base-conceitual.md             — síntese teórica e prompts de referência
│   ├── viabilidade.md                 — análise do design e adaptações ao contexto
│   └── pirls-referencial-exame.md     — matriz PIRLS adaptada para elaboração
└── recursos/
    ├── comando-geracao.md             — prompt utilizado para geração do material
    ├── gerar_pdfs.py                  — script de geração dos PDFs
    └── webapp/                        — aplicativo web de correção (repositório próprio)
        ├── index.html                 — correção manual + ficha diagnóstica + PDF
        └── scan.html                  — leitura por câmera (OMR) + ficha + PDF
```

---

## Como usar

### Aplicação presencial

1. **Imprimir** — `pdfs/03-lista-de-presenca.pdf` e `pdfs/04-folha-respostas-scan.pdf` para cada aluno
2. **Aplicar o exame** — `pdfs/01-exame-proficiencia-leitura.pdf`
3. **Corrigir** — via webapp (ver abaixo) ou manualmente com `pdfs/02-guia-diagnostico-professor.pdf`

### Correção via webapp

Acesse **https://rodrigoleaopb.github.io/leia-app/** no celular ou computador.

| Arquivo | Quando usar |
|---|---|
| `index.html` | Digitar as respostas manualmente durante ou após a aplicação |
| `scan.html` | Fotografar a folha de respostas preenchida para leitura automática |

**Fluxo do `scan.html`:**
1. Fotografe a folha de respostas (`04-folha-respostas-scan.pdf`) sobre superfície plana
2. O app detecta os 4 marcadores de canto, corrige a perspectiva e lê as 20 bolhas automaticamente
3. Confirme ou corrija as respostas na grade (questões não detectadas ficam destacadas em laranja)
4. Informe o nome do aluno e gere a ficha diagnóstica em PDF

**Ambos os modos produzem:** perfil de leitura (A–D), subscores por processo (P0–P4) e diagnóstico por distrator de cada erro.

O exame tem 20 questões de múltipla escolha distribuídas em 5 processos cognitivos (P0 a P4). A correção produz subscores por processo, não apenas um total — o subscore é o dado diagnóstico relevante.

---

## Referências

- Mullis, I.V.S. & Martin, M.O. (Eds.). *PIRLS 2021 Assessment Frameworks*. IEA / Boston College, 2019.
- OECD. *PISA 2022 Assessment and Analytical Framework*. OECD Publishing, 2023.

---

## Licença

Os materiais deste repositório são publicados como **Recurso Educacional Aberto (REA)**, nos termos da UNESCO.

| Componente | Licença |
|---|---|
| Textos, exame, guia do professor, nota técnica, fundamentação | [Creative Commons CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt) |
| Scripts e código de apoio (`recursos/gerar_pdfs.py`) | [MIT License](https://opensource.org/licenses/MIT) |

**CC BY 4.0** — Uso, adaptação e redistribuição são permitidos para qualquer finalidade, inclusive comercial, desde que a autoria seja atribuída. Adaptações não precisam ser licenciadas sob os mesmos termos.

Consulte [`LICENSE.md`](LICENSE.md) para os termos completos.

---

## Autor

**Rodrigo Leão**
[contato.profleao@gmail.com](mailto:contato.profleao@gmail.com)

| Canal | Link |
|---|---|
| YouTube | [youtube.com/rodrigoleaobr](https://youtube.com/rodrigoleaobr) |
| Instagram | [instagram.com/rodrigoleaobr](https://instagram.com/rodrigoleaobr) |
| X / Twitter | [x.com/rodrigoleao](https://x.com/rodrigoleao) |
| GitHub | [github.com/rodrigoleaopb](https://github.com/rodrigoleaopb) |

