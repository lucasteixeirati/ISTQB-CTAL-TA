# ISTQB CTAL-TA - Flashcards: Black-Box Techniques (Parte 2)

**Capítulo:** 2 - Test Techniques  
**Conteúdo:** State Transition Testing, Use Case Testing, Classification Trees  
**Total:** 36 flashcards  
**Revisão:** Dia 1, 3, 7, 14, 30

---

## 🎯 STATE TRANSITION TESTING

### Card 1 - Conceito Básico (K2)
**Q:** O que é State Transition Testing?
**A:** Técnica que testa sistemas onde o comportamento depende do estado atual e de eventos/transições entre estados.

---

### Card 2 - Componentes (K2)
**Q:** Quais os componentes de um State Transition Diagram?
**A:** 
- **States (Estados):** Condições do sistema
- **Transitions (Transições):** Mudanças entre estados
- **Events (Eventos):** Gatilhos que causam transições
- **Actions (Ações):** Resultados das transições

---

### Card 3 - Exemplo Básico (K3)
**Q:** Sistema de login tem estados: Deslogado, Logado, Bloqueado. Desenhe transições básicas.
**A:** 
```
Deslogado --[login correto]--> Logado
Deslogado --[3 tentativas erradas]--> Bloqueado
Logado --[logout]--> Deslogado
Bloqueado --[aguardar 30min]--> Deslogado
```

---

### Card 4 - State Table (K3)
**Q:** Como representar State Transition em tabela?
**A:** 
```
Estado Atual | Evento        | Próximo Estado | Ação
-------------|---------------|----------------|-------------
Deslogado    | Login OK      | Logado         | Mostrar dashboard
Deslogado    | Login Erro    | Deslogado      | Contador++
Deslogado    | 3 erros       | Bloqueado      | Bloquear conta
```

---

### Card 5 - Cobertura 0-Switch (K3)
**Q:** O que é cobertura 0-switch (All States)?
**A:** Testar todos os estados pelo menos uma vez. Cobertura mínima e fraca.

---

### Card 6 - Cobertura 1-Switch (K3)
**Q:** O que é cobertura 1-switch (All Transitions)?
**A:** Testar todas as transições válidas pelo menos uma vez. Cobertura padrão recomendada.

---

### Card 7 - Cobertura 2-Switch (K4)
**Q:** O que é cobertura 2-switch (All Transition Pairs)?
**A:** Testar todos os pares de transições consecutivas. Ex: A→B→C, B→C→D. Cobertura mais rigorosa.

---

### Card 8 - Transições Inválidas (K4)
**Q:** Como testar transições inválidas?
**A:** Tentar eventos que não deveriam causar mudança de estado. Ex: Logout quando já está Deslogado. Sistema deve permanecer no mesmo estado.

---

### Card 9 - Exemplo Prático (K4)
**Q:** Caixa eletrônico: Inativo → Cartão Inserido → PIN Correto → Transação → Inativo. Quantos casos para 1-switch?
**A:** 
- Mínimo 4 casos (uma passagem completa)
- Ideal: testar cada transição isoladamente + fluxo completo
- Incluir transições inválidas (ex: transação sem PIN)

---

### Card 10 - Quando Usar (K3)
**Q:** Quando State Transition Testing é mais eficaz?
**A:** 
- Sistemas com estados distintos (login, carrinho, workflow)
- Máquinas de estado finito
- Protocolos de comunicação
- Sistemas embarcados

---

### Card 11 - Derivação de Casos (K4)
**Q:** Como derivar casos de teste de State Transition?
**A:** 
1. Identificar todos os estados
2. Mapear todas as transições
3. Definir nível de cobertura (0/1/2-switch)
4. Criar sequências de eventos
5. Incluir transições inválidas

---

### Card 12 - Limitações (K4)
**Q:** Quais as limitações de State Transition Testing?
**A:** 
- Explosão de estados em sistemas complexos
- Difícil manutenção com mudanças frequentes
- Não testa lógica interna dos estados
- Pode ser complexo para 2-switch+

---

## 🎯 USE CASE TESTING

### Card 13 - Conceito Básico (K2)
**Q:** O que é Use Case Testing?
**A:** Técnica que deriva casos de teste de use cases (casos de uso), focando em cenários de interação usuário-sistema.

---

### Card 14 - Componentes de Use Case (K2)
**Q:** Quais os componentes de um Use Case?
**A:** 
- **Actor (Ator):** Quem interage (usuário, sistema externo)
- **Preconditions (Pré-condições):** Estado inicial
- **Main Flow (Fluxo principal):** Caminho feliz
- **Alternative Flows (Fluxos alternativos):** Variações
- **Exception Flows (Fluxos de exceção):** Erros
- **Postconditions (Pós-condições):** Estado final

---

### Card 15 - Exemplo Básico (K3)
**Q:** Use Case "Fazer Compra Online". Identifique fluxos.
**A:** 
- **Main:** Selecionar produto → Adicionar carrinho → Pagar → Confirmar
- **Alternative:** Aplicar cupom de desconto
- **Exception:** Pagamento recusado, produto sem estoque

---

### Card 16 - Fluxo Principal (K3)
**Q:** Como testar o Main Flow?
**A:** Criar 1 caso de teste que percorre todo o caminho feliz sem desvios, validando pós-condições.

---

### Card 17 - Fluxos Alternativos (K3)
**Q:** Como testar Alternative Flows?
**A:** Criar casos de teste que desviam do main flow mas ainda completam o use case com sucesso. Ex: Login com biometria vs senha.

---

### Card 18 - Fluxos de Exceção (K4)
**Q:** Como testar Exception Flows?
**A:** Criar casos que provocam erros e validam tratamento adequado. Ex: Senha incorreta → mensagem de erro + permanecer na tela de login.

---

### Card 19 - Cobertura de Use Case (K4)
**Q:** Como medir cobertura em Use Case Testing?
**A:** 
- **Básica:** Main flow testado
- **Intermediária:** Main + alternative flows
- **Completa:** Main + alternative + exception flows
- **Métrica:** % de fluxos testados

---

### Card 20 - Use Case vs User Story (K3)
**Q:** Diferença entre Use Case e User Story?
**A:** 
- **Use Case:** Detalhado, formal, múltiplos fluxos
- **User Story:** Concisa, ágil, foco em valor ("Como... quero... para...")
- Use Case → testes mais completos

---

### Card 21 - Derivação de Casos (K4)
**Q:** Como derivar casos de teste de um Use Case?
**A:** 
1. Identificar todos os fluxos (main/alt/exception)
2. Criar 1 caso para main flow
3. Criar 1 caso para cada alternative flow
4. Criar 1 caso para cada exception flow
5. Combinar fluxos se necessário

---

### Card 22 - Exemplo Completo (K4)
**Q:** Use Case "Sacar Dinheiro" tem 1 main, 2 alternatives, 3 exceptions. Quantos casos mínimos?
**A:** 
- 1 caso main flow
- 2 casos alternative flows
- 3 casos exception flows
**Total mínimo:** 6 casos de teste

---

### Card 23 - Quando Usar (K3)
**Q:** Quando Use Case Testing é mais eficaz?
**A:** 
- Sistemas orientados a transações
- Aplicações com múltiplos atores
- Requisitos documentados em use cases
- Testes de aceitação

---

### Card 24 - Limitações (K4)
**Q:** Quais as limitações de Use Case Testing?
**A:** 
- Depende de use cases bem escritos
- Pode não cobrir requisitos não-funcionais
- Foco em fluxos, não em dados
- Pode gerar redundância entre use cases

---

## 🎯 CLASSIFICATION TREES

### Card 25 - Conceito Básico (K2)
**Q:** O que é Classification Tree Method (CTM)?
**A:** Técnica que organiza partições de teste em estrutura hierárquica (árvore), facilitando identificação de combinações relevantes.

---

### Card 26 - Componentes (K2)
**Q:** Quais os componentes de uma Classification Tree?
**A:** 
- **Root (Raiz):** Funcionalidade sendo testada
- **Classifications (Classificações):** Aspectos/dimensões
- **Classes (Classes):** Valores possíveis de cada classificação
- **Test Cases (Casos):** Combinações selecionadas

---

### Card 27 - Exemplo Básico (K3)
**Q:** Sistema de busca. Crie classification tree básica.
**A:** 
```
Busca de Produtos
├─ Tipo de Busca
│  ├─ Por nome
│  ├─ Por categoria
│  └─ Por preço
├─ Ordenação
│  ├─ Crescente
│  └─ Decrescente
└─ Filtros
   ├─ Com filtro
   └─ Sem filtro
```

---

### Card 28 - Combinações (K3)
**Q:** Árvore com 3 classificações (3, 2, 2 classes). Quantas combinações possíveis?
**A:** 3 × 2 × 2 = **12 combinações possíveis**

---

### Card 29 - Seleção de Combinações (K4)
**Q:** Como selecionar combinações relevantes em CTM?
**A:** 
- **All combinations:** Testar todas (exaustivo)
- **Each choice:** Cada classe testada pelo menos 1x (mínimo)
- **Pairwise:** Cada par de classes testado (balanceado)
- **Risk-based:** Priorizar por risco

---

### Card 30 - CTM vs EP (K4)
**Q:** Diferença entre Classification Tree e Equivalence Partitioning?
**A:** 
- **EP:** Foca em partições individuais
- **CTM:** Organiza partições hierarquicamente e facilita combinações
- CTM é evolução/extensão do EP

---

### Card 31 - Exemplo Prático (K4)
**Q:** Login: Usuário (válido/inválido), Senha (válida/inválida), Captcha (correto/incorreto). Crie árvore e selecione casos.
**A:** 
```
Login
├─ Usuário: Válido, Inválido
├─ Senha: Válida, Inválida
└─ Captcha: Correto, Incorreto

Casos selecionados (pairwise):
1. Válido + Válida + Correto (sucesso)
2. Inválido + Válida + Correto
3. Válido + Inválida + Correto
4. Válido + Válida + Incorreto
```

---

### Card 32 - Constraints (K4)
**Q:** O que são constraints em Classification Trees?
**A:** Restrições que eliminam combinações impossíveis/inválidas. Ex: "Desconto de estudante" só se "Idade < 25".

---

### Card 33 - Ferramentas (K2)
**Q:** Existem ferramentas para Classification Trees?
**A:** Sim. Exemplos:
- **CTE XL:** Plugin Excel
- **TESTONA:** Ferramenta comercial
- **Diagramas manuais:** Draw.io, Lucidchart

---

### Card 34 - Quando Usar (K3)
**Q:** Quando Classification Trees são mais eficazes?
**A:** 
- Múltiplas variáveis independentes
- Necessidade de visualização hierárquica
- Combinações complexas
- Documentação de estratégia de teste

---

### Card 35 - Processo de Criação (K4)
**Q:** Quais os passos para criar uma Classification Tree?
**A:** 
1. Identificar funcionalidade (root)
2. Identificar classificações (aspectos)
3. Identificar classes (valores)
4. Definir constraints
5. Selecionar combinações (estratégia)
6. Derivar casos de teste

---

### Card 36 - Limitações (K4)
**Q:** Quais as limitações de Classification Trees?
**A:** 
- Pode ser complexa para sistemas simples
- Requer treinamento para usar efetivamente
- Manutenção trabalhosa em mudanças
- Explosão combinatória sem boa estratégia

---

## 📊 Resumo do Deck 2.2

**Técnicas Cobertas:**
- ✅ State Transition Testing (12 cards)
- ✅ Use Case Testing (12 cards)
- ✅ Classification Trees (12 cards)

**Distribuição por K-Level:**
- K2 (Conhecimento): 8 cards
- K3 (Aplicação): 16 cards
- K4 (Análise): 12 cards

**Próximo Deck:** 2.3 - White-Box + Experience-Based Testing

---

**Revisão Sugerida (Spaced Repetition):**
- Dia 1: Todos os 36 cards
- Dia 3: Cards marcados como "difícil"
- Dia 7: Todos os cards novamente
- Dia 14: Cards "difícil" + revisão geral
- Dia 30: Revisão final antes do exame

---

**Progresso Total Cap 2:**
- ✅ Deck 2.1: 36 cards (EP, BVA, Decision Tables)
- ✅ Deck 2.2: 36 cards (State Transition, Use Case, Classification Trees)
- ⏳ Deck 2.3: Pendente (White-Box + Experience-Based)

**Total até agora:** 72 flashcards
