# Resumo expandido — GCV 2026

## Build

```bash
cd manuscript/gcv2026
latexmk -pdf resumo-expandido.tex
```

## Regras (extraídas de `docs/gcv2026-regras-submissao.docx`)

- **Formato**: PDF
- **Páginas**: máx. 5
- **Página**: A4
- **Margens**: superior 3cm, inferior 2cm, lateral esquerda 3cm, lateral direita 2cm
- **Fonte do corpo**: Times New Roman 12pt
- **Alinhamento**: justificado
- **Espaçamento**: simples (1,0)
- **Numeração**: a partir da primeira página, abaixo e à direita
- **Estrutura sugerida**: Introdução, Metodologia, Resultados, Conclusões
- **Legendas figuras/tabelas**: Times 12, centralizadas, acima do elemento; fonte Times 10, centralizada, abaixo
- **Numeração de seções**: progressiva (1, 1.1, 1.1.1, ...)
- **Citações no texto**: minúsculas no fluxo, MAIÚSCULAS entre parênteses no fim do parágrafo
- **Citações longas (>4 linhas)**: destacadas, recuo 4 cm, fonte 10, justificado
- **Referências**: ordem alfabética no final, alinhadas à esquerda, NBR-6023 ABNT
- **ANONIMIZAR**: remover identificação de autoria do documento E das propriedades do arquivo Word/PDF

## Checklist pré-submissão

- [ ] Conteúdo: 4 seções (Intro, Metodologia, Resultados, Conclusões)
- [ ] Máximo 5 páginas
- [ ] Anonimizado (sem autores, sem agradecimentos, sem instituições)
- [ ] Propriedades do PDF limpas (`exiftool -all= resumo-expandido.pdf`)
- [ ] Referências em ABNT (NBR-6023)
- [ ] Tabelas e figuras com legenda acima + fonte abaixo
- [ ] Citações verificadas (zero alucinação)
