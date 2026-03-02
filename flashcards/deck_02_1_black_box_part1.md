# ISTQB CTAL-TA - Flashcards: Black-Box Techniques (Parte 1)

**Capítulo:** 2 - Test Techniques  
**Conteúdo:** Equivalence Partitioning, Boundary Value Analysis, Decision Tables  
**Total:** 36 flashcards  
**Revisão:** Dia 1, 3, 7, 14, 30

---

## 🎯 EQUIVALENCE PARTITIONING (EP)

### Card 1 - Conceito Básico (K2)
**Q:** O que é Equivalence Partitioning (EP)?
**A:** Técnica black-box que divide entradas em partições/classes onde todos os valores devem ter comportamento similar, reduzindo o número de casos de teste.

---

### Card 2 - Objetivo (K2)
**Q:** Qual o principal objetivo do EP?
**A:** Reduzir o número de casos de teste mantendo cobertura adequada, testando 1 valor representativo de cada partição.

---

### Card 3 - Tipos de Partições (K2)
**Q:** Quais os tipos de partições no EP?
**A:** 
- **Partições válidas:** Valores aceitos pelo sistema
- **Partições inválidas:** Valores rejeitados pelo sistema

---

### Card 4 - Exemplo Prático (K3)
**Q:** Sistema aceita idade 18-65. Identifique as partições.
**A:** 
- **Válida:** [18-65]
- **Inválida 1:** [< 18]
- **Inválida 2:** [> 65]
**Total:** 3 partições

---

### Card 5 - Seleção de Valores (K3)
**Q:** Como selecionar valores de teste em cada partição?
**A:** Escolher 1 valor representativo do meio da partição (não nas bordas). Ex: partição [18-65] → testar com 40.

---

### Card 6 - EP com Múltiplas Variáveis (K3)
**Q:** Sistema tem 2 campos: Idade [18-65] e Salário [1000-10000]. Quantos casos de teste mínimos?
**A:** 
- Idade: 3 partições (1 válida + 2 inválidas)
- Salário: 3 partições (1 válida + 2 inválidas)
**Mínimo:** 4 casos (1 válido + 3 inválidos combinando as inválidas)

---

### Card 7 - EP Forte vs Fraco (K4)
**Q:** Diferença entre EP Forte e EP Fraco?
**A:** 
- **Fraco:** Combina valores válidos juntos e inválidos separados
- **Forte:** Testa todas as combinações de partições (válidas e inválidas)

---

### Card 8 - Quando Usar EP (K3)
**Q:** Quando EP é mais eficaz?
**A:** 
- Entradas com ranges numéricos
- Listas de valores discretos
- Campos com regras de validação claras
- Quando há muitos valores possíveis

---

### Card 9 - Limitações do EP (K4)
**Q:** Quais as limitações do EP?
**A:** 
- Não testa valores de fronteira (use BVA)
- Assume comportamento uniforme na partição
- Pode perder defeitos em valores específicos

---

### Card 10 - EP com Strings (K3)
**Q:** Campo "Nome" aceita 2-50 caracteres. Identifique partições.
**A:** 
- **Válida:** [2-50 caracteres]
- **Inválida 1:** [0-1 caracteres]
- **Inválida 2:** [> 50 caracteres]
- **Inválida 3:** [caracteres especiais inválidos]

---

### Card 11 - EP em Listas (K3)
**Q:** Campo "Estado Civil" aceita: Solteiro, Casado, Divorciado, Viúvo. Quantas partições?
**A:** 
- **4 válidas:** Uma para cada opção
- **1 inválida:** Valores não listados (ex: "Outro")
**Total:** 5 partições

---

### Card 12 - Análise de EP (K4)
**Q:** Como documentar partições de EP?
**A:** Criar tabela com:
- ID da partição
- Descrição
- Tipo (válida/inválida)
- Valores de exemplo
- Caso de teste associado

---

## 🎯 BOUNDARY VALUE ANALYSIS (BVA)

### Card 13 - Conceito Básico (K2)
**Q:** O que é Boundary Value Analysis (BVA)?
**A:** Técnica que testa valores nas fronteiras (limites) das partições, onde defeitos são mais prováveis.

---

### Card 14 - Princípio do BVA (K2)
**Q:** Por que testar valores de fronteira?
**A:** Defeitos ocorrem frequentemente em limites devido a erros de implementação (<=, <, >=, >).

---

### Card 15 - Valores de Fronteira (K3)
**Q:** Para range [18-65], quais valores testar no BVA?
**A:** 
- **Fronteira inferior:** 17, 18, 19
- **Fronteira superior:** 64, 65, 66
**Total:** 6 valores

---

### Card 16 - BVA 2-Value (K3)
**Q:** O que é BVA 2-value?
**A:** Testa apenas 2 valores por fronteira: o limite e o valor imediatamente fora. Ex: [18-65] → testar 17, 18, 65, 66.

---

### Card 17 - BVA 3-Value (K3)
**Q:** O que é BVA 3-value?
**A:** Testa 3 valores por fronteira: limite, valor antes e valor depois. Ex: [18-65] → testar 17, 18, 19, 64, 65, 66.

---

### Card 18 - BVA com EP (K4)
**Q:** Como combinar EP e BVA?
**A:** 
1. Identificar partições (EP)
2. Testar fronteiras de cada partição (BVA)
3. Adicionar 1 valor do meio da partição válida (EP)

---

### Card 19 - BVA em Strings (K3)
**Q:** Campo aceita 2-50 caracteres. Quais valores testar?
**A:** 
- **Fronteira inferior:** 1, 2, 3 caracteres
- **Fronteira superior:** 49, 50, 51 caracteres
- **Especial:** 0 caracteres (vazio)

---

### Card 20 - BVA em Listas Ordenadas (K3)
**Q:** Dropdown com 10 itens. Quais posições testar?
**A:** 
- Primeiro item (posição 1)
- Segundo item (posição 2)
- Penúltimo item (posição 9)
- Último item (posição 10)

---

### Card 21 - BVA Interno (K4)
**Q:** O que é BVA interno?
**A:** Testar fronteiras internas quando há múltiplas partições válidas. Ex: Desconto 5% [0-100], 10% [101-500], 15% [501+] → testar 100, 101, 500, 501.

---

### Card 22 - Quando Usar BVA (K3)
**Q:** Quando BVA é mais eficaz?
**A:** 
- Ranges numéricos
- Limites de tamanho (strings, arrays)
- Datas e horários
- Valores ordenados

---

### Card 23 - BVA Robustez (K4)
**Q:** O que é BVA de robustez?
**A:** Extensão do BVA que testa valores extremos além das fronteiras normais (ex: valores negativos, muito grandes, null).

---

### Card 24 - Limitações do BVA (K4)
**Q:** Quais as limitações do BVA?
**A:** 
- Não testa valores no meio das partições
- Pode gerar muitos casos de teste
- Assume que fronteiras são críticas (nem sempre verdade)

---

## 🎯 DECISION TABLES

### Card 25 - Conceito Básico (K2)
**Q:** O que é Decision Table?
**A:** Técnica que representa combinações de condições (inputs) e suas ações resultantes (outputs) em formato tabular.

---

### Card 26 - Estrutura (K2)
**Q:** Quais os componentes de uma Decision Table?
**A:** 
- **Conditions (Condições):** Inputs/variáveis
- **Actions (Ações):** Outputs/resultados
- **Rules (Regras):** Colunas com combinações
- **Entries (Entradas):** Valores (T/F, Y/N)

---

### Card 27 - Exemplo Básico (K3)
**Q:** Sistema de desconto: Cliente VIP? Compra > R$100? Crie a tabela.
**A:** 
```
Condições       | R1 | R2 | R3 | R4 |
VIP?            | Y  | Y  | N  | N  |
Compra > 100?   | Y  | N  | Y  | N  |
----------------|----|----|----|----|
Desconto 20%    | X  |    |    |    |
Desconto 10%    |    | X  | X  |    |
Sem desconto    |    |    |    | X  |
```

---

### Card 28 - Número de Regras (K3)
**Q:** Como calcular o número de regras em uma Decision Table?
**A:** **2^n** onde n = número de condições. Ex: 3 condições → 2³ = 8 regras.

---

### Card 29 - Tabela Completa vs Limitada (K3)
**Q:** Diferença entre Decision Table completa e limitada?
**A:** 
- **Completa:** Todas as 2^n combinações
- **Limitada:** Apenas combinações relevantes (remove impossíveis/redundantes)

---

### Card 30 - Collapsed Table (K4)
**Q:** O que é uma Collapsed Decision Table?
**A:** Tabela otimizada que combina regras com mesmas ações usando "-" (don't care). Reduz número de colunas.

---

### Card 31 - Exemplo Collapsed (K4)
**Q:** Regras R1(Y,Y→A) e R2(Y,N→A) podem ser collapsed?
**A:** Sim! Ambas têm mesma ação quando condição 1 = Y.
```
Resultado: (Y, - → A)
```

---

### Card 32 - Quando Usar Decision Tables (K3)
**Q:** Quando Decision Tables são mais eficazes?
**A:** 
- Múltiplas condições combinadas
- Regras de negócio complexas
- Lógica booleana
- Sistemas com muitos IFs

---

### Card 33 - Cobertura (K4)
**Q:** Como medir cobertura em Decision Tables?
**A:** 
- **Cobertura de regras:** % de regras testadas
- **Cobertura de condições:** % de T/F testados por condição
- **Cobertura de ações:** % de ações executadas

---

### Card 34 - Decision Tables vs Decision Trees (K4)
**Q:** Diferença entre Decision Table e Decision Tree?
**A:** 
- **Table:** Formato tabular, melhor para múltiplas condições paralelas
- **Tree:** Formato hierárquico, melhor para decisões sequenciais

---

### Card 35 - Validação de Tabelas (K4)
**Q:** Como validar uma Decision Table?
**A:** 
- Verificar completude (todas as combinações)
- Verificar consistência (sem contradições)
- Verificar redundância (regras duplicadas)
- Validar com stakeholders

---

### Card 36 - Limitações (K4)
**Q:** Quais as limitações de Decision Tables?
**A:** 
- Explosão combinatória (muitas condições)
- Difícil manutenção em sistemas grandes
- Não representa fluxo temporal
- Pode ser complexa para não-técnicos

---

## 📊 Resumo do Deck 2.1

**Técnicas Cobertas:**
- ✅ Equivalence Partitioning (12 cards)
- ✅ Boundary Value Analysis (12 cards)
- ✅ Decision Tables (12 cards)

**Distribuição por K-Level:**
- K2 (Conhecimento): 9 cards
- K3 (Aplicação): 18 cards
- K4 (Análise): 9 cards

**Próximo Deck:** 2.2 - State Transition, Use Case, Classification Trees

---

**Revisão Sugerida (Spaced Repetition):**
- Dia 1: Todos os 36 cards
- Dia 3: Cards marcados como "difícil"
- Dia 7: Todos os cards novamente
- Dia 14: Cards "difícil" + revisão geral
- Dia 30: Revisão final antes do exame
