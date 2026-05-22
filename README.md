# LEIA! — Levantamento Integrado de Avaliação em Leitura
### Ensino Médio — Populações com Defasagem Severa · `v0-alpha`

Instrumento diagnóstico de leitura para alunos do ensino médio com déficit severo de compreensão. Baseado na matriz de processos cognitivos do PIRLS 2021 (IEA / Boston College), adaptado para populações que operam abaixo do Benchmark Baixo internacional (400 pontos).

---

## O que é o LEIA!

Um levantamento de ponto zero: não mede onde o aluno deveria estar pelo critério curricular, mas onde ele efetivamente está. O LEIA! produz um perfil diagnóstico por aluno — identificando em qual processo cognitivo ocorre a ruptura de compreensão — e orienta diretamente a intervenção.

---

## Estrutura do repositório

```
├── nota-tecnica.md              — fundamentação, decisões de design, limitações
├── exame/
│   ├── exame-proficiencia.md    — prova do aluno (20 questões, 2 textos)
│   ├── guia-do-professor.md     — gabarito diagnóstico, perfis, ficha de registro
│   └── pdfs/                   — versões prontas para impressão
├── fundamentacao/
│   ├── base-conceitual.md       — síntese teórica e prompts de referência
│   ├── viabilidade.md           — análise do design e adaptações ao contexto
│   └── pirls-referencial-exame.md — matriz PIRLS adaptada para elaboração
└── recursos/
    ├── comando-geracao.md       — prompt utilizado para geração do material
    └── gerar_pdfs.py            — script de geração dos PDFs
```

---

## Como usar

1. **Aplicar o exame** — `exame/pdfs/01-exame-proficiencia-leitura.pdf`
2. **Corrigir e classificar** — `exame/pdfs/02-guia-diagnostico-professor.pdf`
3. **Entender o design** — `nota-tecnica.md`

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

