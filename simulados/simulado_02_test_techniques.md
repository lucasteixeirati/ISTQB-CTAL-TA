# ISTQB CTAL-TA - Simulado 02: Test Techniques

**Capítulo:** 2 - Test Techniques  
**Questões:** 20  
**Tempo sugerido:** 60 minutos  
**Aprovação:** 14/20 (70%)

---

## Questão 1 (K3) - Equivalence Partitioning
Campo "Idade" aceita valores de 18 a 65 anos. Aplicando EP, quantas partições você identificaria?

A) 2 partições (válida e inválida)  
B) 3 partições (1 válida e 2 inválidas)  
C) 4 partições (2 válidas e 2 inválidas)  
D) 5 partições (1 válida e 4 inválidas)

**Resposta:** B  
**Justificativa:** 
- 1 partição válida: [18-65]
- 2 partições inválidas: [<18] e [>65]

---

## Questão 2 (K4) - Boundary Value Analysis
Sistema aceita valores de 1 a 100. Usando BVA 3-value, quais valores você testaria?

A) 0, 1, 100, 101  
B) 1, 50, 100  
C) 0, 1, 2, 99, 100, 101  
D) 1, 2, 99, 100

**Resposta:** C  
**Justificativa:** BVA 3-value testa 3 valores por fronteira:
- Fronteira inferior: 0 (fora), 1 (limite), 2 (dentro)
- Fronteira superior: 99 (dentro), 100 (limite), 101 (fora)

---

## Questão 3 (K3) - Decision Table
Sistema de desconto: Cliente VIP (Sim/Não) e Compra > R$100 (Sim/Não). Quantas regras uma decision table completa teria?

A) 2 regras  
B) 3 regras  
C) 4 regras  
D) 8 regras

**Resposta:** C  
**Justificativa:** 2^n onde n=2 condições → 2^2 = 4 regras (VV, VF, FV, FF)

---

## Questão 4 (K4) - Decision Table Collapsed
Duas regras: R1(Sim, Sim → Desconto 20%) e R2(Sim, Não → Desconto 20%). Podem ser collapsed?

A) Não, são regras diferentes  
B) Sim, resultam em (Sim, - → Desconto 20%)  
C) Sim, resultam em (-, Sim → Desconto 20%)  
D) Apenas se houver terceira condição

**Resposta:** B  
**Justificativa:** Ambas têm mesma ação quando condição 1 = Sim, independente da condição 2. Usa-se "-" (don't care) na condição 2.

---

## Questão 5 (K3) - State Transition
Sistema de login tem 3 estados: Deslogado, Logado, Bloqueado. Para cobertura 1-switch (all transitions), quantos casos de teste mínimos?

A) 3 casos (um por estado)  
B) 4 casos (número de transições válidas)  
C) 6 casos (todas as combinações)  
D) 9 casos (todas as possibilidades)

**Resposta:** B  
**Justificativa:** 1-switch cobre todas as transições válidas. Exemplo:
- Deslogado → Logado
- Logado → Deslogado
- Deslogado → Bloqueado
- Bloqueado → Deslogado
= 4 transições

---

## Questão 6 (K4) - State Transition Coverage
Qual a diferença entre 0-switch e 1-switch coverage?

A) 0-switch testa estados, 1-switch testa transições  
B) 0-switch é mais rigoroso que 1-switch  
C) Não há diferença prática  
D) 0-switch testa transições inválidas

**Resposta:** A  
**Justificativa:** 
- 0-switch (All States): Visita cada estado pelo menos 1x
- 1-switch (All Transitions): Executa cada transição pelo menos 1x (mais rigoroso)

---

## Questão 7 (K3) - Use Case Testing
Use Case "Comprar Produto" tem: 1 main flow, 2 alternative flows, 3 exception flows. Quantos casos de teste mínimos para cobertura completa?

A) 3 casos  
B) 4 casos  
C) 6 casos  
D) 12 casos

**Resposta:** C  
**Justificativa:** 1 (main) + 2 (alternative) + 3 (exception) = 6 casos mínimos

---

## Questão 8 (K4) - Use Case vs User Story
Qual afirmação está CORRETA sobre Use Case vs User Story?

A) Use Case é mais adequado para metodologias ágeis  
B) User Story é mais detalhada que Use Case  
C) Use Case inclui fluxos alternativos e de exceção  
D) User Story substitui completamente Use Case

**Resposta:** C  
**Justificativa:** Use Case é mais detalhado e formal, incluindo main/alternative/exception flows. User Story é concisa e focada em valor.

---

## Questão 9 (K3) - Classification Tree
Busca de produtos: Tipo (3 opções), Ordenação (2 opções), Filtro (2 opções). Quantas combinações possíveis?

A) 7 combinações  
B) 12 combinações  
C) 18 combinações  
D) 24 combinações

**Resposta:** B  
**Justificativa:** 3 × 2 × 2 = 12 combinações possíveis

---

## Questão 10 (K4) - Classification Tree Strategy
Qual estratégia de seleção de combinações em Classification Tree oferece melhor custo-benefício?

A) All combinations (exaustivo)  
B) Each choice (mínimo)  
C) Pairwise (balanceado)  
D) Random selection

**Resposta:** C  
**Justificativa:** Pairwise testa cada par de valores pelo menos 1x, oferecendo boa cobertura com número reduzido de casos (balanceado).

---

## Questão 11 (K2) - White-Box Testing
O que mede Statement Coverage?

A) Percentual de decisões testadas  
B) Percentual de linhas de código executadas  
C) Percentual de branches testadas  
D) Percentual de caminhos testados

**Resposta:** B  
**Justificativa:** Statement Coverage mede % de linhas/statements executadas pelos testes.

---

## Questão 12 (K3) - Branch Coverage
Código tem 5 IFs (10 branches). Testes cobrem 8 branches. Qual a Branch Coverage?

A) 50%  
B) 60%  
C) 80%  
D) 100%

**Resposta:** C  
**Justificativa:** 8/10 × 100 = 80%

---

## Questão 13 (K4) - Statement vs Branch
É possível ter 100% Statement Coverage mas menos de 100% Branch Coverage?

A) Não, são equivalentes  
B) Sim, Statement é mais fraco que Branch  
C) Não, Branch é mais fraco que Statement  
D) Apenas em linguagens específicas

**Resposta:** B  
**Justificativa:** Exemplo:
```
if (x > 0) { print("OK"); }
```
Testando apenas x=5: Statement=100% (linha executada) mas Branch=50% (só TRUE testado).

---

## Questão 14 (K2) - Error Guessing
O que é Error Guessing?

A) Técnica formal baseada em especificações  
B) Técnica que usa experiência para antecipar erros prováveis  
C) Ferramenta automatizada de detecção de bugs  
D) Método de análise estática de código

**Resposta:** B  
**Justificativa:** Error Guessing é técnica experience-based onde testador antecipa erros baseado em experiência e intuição.

---

## Questão 15 (K3) - Exploratory Testing
Qual característica NÃO é típica de Exploratory Testing?

A) Design e execução simultâneos  
B) Scripts detalhados pré-definidos  
C) Aprendizado contínuo durante teste  
D) Adaptação baseada em resultados

**Resposta:** B  
**Justificativa:** Exploratory Testing NÃO usa scripts pré-definidos. Design acontece durante a execução.

---

## Questão 16 (K3) - Session-Based Testing
O que é um Charter em Session-Based Exploratory Testing?

A) Relatório final da sessão  
B) Objetivo/missão da sessão exploratória  
C) Ferramenta de automação  
D) Métrica de cobertura

**Resposta:** B  
**Justificativa:** Charter define o objetivo/foco da sessão exploratória. Ex: "Explorar upload de arquivos focando em tipos e tamanhos".

---

## Questão 17 (K4) - Checklist-Based Testing
Qual a principal LIMITAÇÃO de Checklist-Based Testing?

A) É muito caro de implementar  
B) Requer ferramentas especializadas  
C) Pode ficar desatualizado e criar "checkbox mentality"  
D) Não pode ser usado em projetos ágeis

**Resposta:** C  
**Justificativa:** Checklists podem ficar desatualizados e criar mentalidade de apenas "marcar itens" sem análise crítica.

---

## Questão 18 (K4) - Combinação de Técnicas
Qual a melhor estratégia para combinar técnicas de teste?

A) Usar apenas técnicas formais (EP, BVA)  
B) Usar apenas técnicas experience-based  
C) Aplicar técnicas formais primeiro, depois experience-based para gaps  
D) Escolher apenas uma técnica por projeto

**Resposta:** C  
**Justificativa:** Melhor abordagem: técnicas formais para cobertura sistemática + experience-based para casos não cobertos e exploração.

---

## Questão 19 (K3) - Seleção de Técnica
Sistema bancário com cálculos complexos de juros. Qual técnica é MAIS apropriada?

A) Exploratory Testing  
B) Decision Tables  
C) State Transition  
D) Error Guessing

**Resposta:** B  
**Justificativa:** Decision Tables são ideais para lógica complexa com múltiplas condições e regras de negócio (como cálculos de juros).

---

## Questão 20 (K4) - Técnicas por Nível
Qual técnica é MAIS apropriada para testes de INTEGRAÇÃO?

A) Statement Coverage  
B) Branch Coverage  
C) State Transition Testing  
D) Exploratory Testing

**Resposta:** C  
**Justificativa:** State Transition é ideal para integração, testando interações e mudanças de estado entre componentes. White-box (A, B) é para unitário.

---

## Gabarito Rápido
1-B | 2-C | 3-C | 4-B | 5-B | 6-A | 7-C | 8-C | 9-B | 10-C  
11-B | 12-C | 13-B | 14-B | 15-B | 16-B | 17-C | 18-C | 19-B | 20-C

---

## Análise de Desempenho

**Sua pontuação:** ___/20

- **18-20 acertos (90-100%):** Excelente! Domínio completo de técnicas
- **14-17 acertos (70-85%):** Bom! Revisar questões erradas
- **10-13 acertos (50-65%):** Regular. Estudar Cap 2 novamente
- **0-9 acertos (<50%):** Insuficiente. Leitura completa + flashcards

---

## Análise por Técnica

**Black-Box Básico (Q1-4):** ___/4
- EP e BVA: Questões 1-2
- Decision Tables: Questões 3-4

**Black-Box Avançado (Q5-10):** ___/6
- State Transition: Questões 5-6
- Use Case: Questões 7-8
- Classification Trees: Questões 9-10

**White-Box (Q11-13):** ___/3
- Statement/Branch Coverage

**Experience-Based (Q14-17):** ___/4
- Error Guessing, Exploratory, Checklist

**Aplicação (Q18-20):** ___/3
- Combinação e seleção de técnicas

---

## Próximos Passos

**Se acertou 70%+:**
- [ ] Revisar questões erradas
- [ ] Revisar flashcards das técnicas que errou
- [ ] Avançar para Simulado 03 (Quality Characteristics)

**Se acertou <70%:**
- [ ] Revisar todo o Cap 2 do syllabus
- [ ] Estudar todos os flashcards do Cap 2 (104 cards)
- [ ] Refazer este simulado em 3 dias
- [ ] Criar exemplos práticos de cada técnica

---

**Dica:** Cap 2 é 50% do exame! Domine estas técnicas antes de avançar.
