# ISTQB CTAL-TA - Flashcards: White-Box + Experience-Based Testing

**Capítulo:** 2 - Test Techniques  
**Conteúdo:** White-Box Testing, Experience-Based Testing, Comparação de Técnicas  
**Total:** 32 flashcards  
**Revisão:** Dia 1, 3, 7, 14, 30

---

## 🎯 WHITE-BOX TESTING

### Card 1 - Conceito Básico (K2)
**Q:** O que é White-Box Testing?
**A:** Técnica que testa a estrutura interna do código (lógica, fluxos, caminhos), baseada no conhecimento da implementação.

---

### Card 2 - Statement Coverage (K2)
**Q:** O que é Statement Coverage?
**A:** Métrica que mede a % de linhas de código executadas pelos testes. Cobertura mínima e fraca.

---

### Card 3 - Exemplo Statement (K3)
**Q:** Código tem 10 linhas. Testes executam 8 linhas. Qual a Statement Coverage?
**A:** **80%** (8/10 × 100)

---

### Card 4 - Branch Coverage (K2)
**Q:** O que é Branch Coverage (Decision Coverage)?
**A:** Métrica que mede a % de branches (decisões TRUE/FALSE) executadas. Mais forte que Statement Coverage.

---

### Card 5 - Exemplo Branch (K3)
**Q:** Código tem 4 IFs (8 branches possíveis). Testes cobrem 6 branches. Qual a Branch Coverage?
**A:** **75%** (6/8 × 100)

---

### Card 6 - Statement vs Branch (K3)
**Q:** É possível ter 100% Statement Coverage mas não 100% Branch Coverage?
**A:** **Sim!** Exemplo:
```
if (x > 0) {
    print("Positivo");  // Linha executada
}
// Se testar apenas x=5, Statement=100% mas Branch=50% (só TRUE)
```

---

### Card 7 - Decision Coverage (K3)
**Q:** Diferença entre Branch Coverage e Decision Coverage?
**A:** São equivalentes no ISTQB. Ambos medem TRUE/FALSE de cada decisão. Alguns autores diferenciam, mas no exame são sinônimos.

---

### Card 8 - Quando Usar White-Box (K3)
**Q:** Quando White-Box Testing é mais apropriado?
**A:** 
- Testes unitários
- Código crítico de segurança
- Algoritmos complexos
- Validação de cobertura de testes

---

## 🎯 EXPERIENCE-BASED TESTING

### Card 9 - Conceito Básico (K2)
**Q:** O que é Experience-Based Testing?
**A:** Técnicas que dependem da experiência, intuição e conhecimento do testador, não de especificações formais.

---

### Card 10 - Error Guessing (K2)
**Q:** O que é Error Guessing?
**A:** Técnica onde o testador antecipa erros prováveis baseado em experiência passada, conhecimento de defeitos comuns e intuição.

---

### Card 11 - Exemplo Error Guessing (K3)
**Q:** Testando campo de data. Quais erros você "adivinharia"?
**A:** 
- 29/02 em ano não-bissexto
- 31/04 (abril tem 30 dias)
- Datas futuras inválidas
- Formato incorreto (32/13/2025)
- Valores null ou vazios

---

### Card 12 - Fault Attack (K3)
**Q:** O que é Fault Attack em Error Guessing?
**A:** Abordagem sistemática onde se cria lista de defeitos prováveis e testa especificamente para encontrá-los.

---

### Card 13 - Exploratory Testing (K2)
**Q:** O que é Exploratory Testing?
**A:** Técnica onde design, execução e aprendizado de testes acontecem simultaneamente, sem scripts pré-definidos.

---

### Card 14 - Características Exploratory (K3)
**Q:** Quais as características principais do Exploratory Testing?
**A:** 
- Aprendizado contínuo
- Design de testes em tempo real
- Foco em descoberta
- Adaptação baseada em resultados
- Documentação mínima

---

### Card 15 - Session-Based Testing (K3)
**Q:** O que é Session-Based Exploratory Testing?
**A:** Abordagem estruturada onde testes exploratórios são organizados em sessões com:
- Charter (objetivo)
- Time-box (duração fixa, ex: 90min)
- Debriefing (relatório pós-sessão)

---

### Card 16 - Charter (K3)
**Q:** O que é um Charter em Exploratory Testing?
**A:** Objetivo/missão da sessão exploratória. Exemplo: "Explorar funcionalidade de upload de arquivos focando em tipos de arquivo e tamanhos limites".

---

### Card 17 - Exploratory vs Scripted (K4)
**Q:** Diferença entre Exploratory e Scripted Testing?
**A:** 
- **Exploratory:** Design durante execução, flexível, criativo
- **Scripted:** Design antes da execução, repetível, estruturado
- Ambos têm valor, uso depende do contexto

---

### Card 18 - Quando Usar Exploratory (K3)
**Q:** Quando Exploratory Testing é mais eficaz?
**A:** 
- Requisitos vagos ou mudando
- Pouco tempo disponível
- Complementar testes automatizados
- Buscar defeitos inesperados
- Avaliar usabilidade

---

### Card 19 - Checklist-Based Testing (K2)
**Q:** O que é Checklist-Based Testing?
**A:** Técnica que usa listas de verificação (checklists) criadas a partir de experiência, padrões ou requisitos para guiar os testes.

---

### Card 20 - Exemplo Checklist (K3)
**Q:** Crie checklist básico para testar formulário de login.
**A:** 
- [ ] Campos obrigatórios validados?
- [ ] Senha mascarada?
- [ ] Mensagens de erro claras?
- [ ] Botão "Esqueci senha" funciona?
- [ ] Limite de tentativas implementado?
- [ ] Redirecionamento após login correto?

---

### Card 21 - Vantagens Checklist (K3)
**Q:** Quais as vantagens de Checklist-Based Testing?
**A:** 
- Rápido de criar e usar
- Captura conhecimento da equipe
- Consistência entre testadores
- Fácil manutenção
- Bom para testes de regressão

---

### Card 22 - Limitações Checklist (K4)
**Q:** Quais as limitações de Checklist-Based Testing?
**A:** 
- Pode ficar desatualizado
- Não substitui análise profunda
- Risco de "checkbox mentality"
- Pode perder cenários não listados

---

### Card 23 - Taxonomia de Defeitos (K3)
**Q:** Como usar taxonomia de defeitos em Experience-Based Testing?
**A:** Criar categorias de defeitos comuns (ex: validação, segurança, performance) e usar como base para Error Guessing e Checklists.

---

### Card 24 - Combinação de Técnicas (K4)
**Q:** Como combinar Experience-Based com outras técnicas?
**A:** 
- Usar técnicas formais (EP, BVA) primeiro
- Aplicar Exploratory para áreas não cobertas
- Error Guessing para casos extremos
- Checklist para validação final

---

## 🎯 COMPARAÇÃO DE TÉCNICAS

### Card 25 - Black-Box vs White-Box (K4)
**Q:** Quando escolher Black-Box vs White-Box?
**A:** 
- **Black-Box:** Testes funcionais, aceitação, sem acesso ao código
- **White-Box:** Testes unitários, cobertura de código, otimização
- **Ideal:** Combinar ambas

---

### Card 26 - Técnicas Estáticas vs Dinâmicas (K3)
**Q:** Diferença entre técnicas estáticas e dinâmicas?
**A:** 
- **Estáticas:** Sem executar código (reviews, análise estática)
- **Dinâmicas:** Executando código (todos os tipos de teste)

---

### Card 27 - Seleção de Técnica (K4)
**Q:** Quais fatores considerar ao selecionar técnica de teste?
**A:** 
- Tipo de sistema e tecnologia
- Nível de risco
- Requisitos disponíveis
- Tempo e recursos
- Habilidades da equipe
- Fase do projeto

---

### Card 28 - Técnicas por Nível de Teste (K4)
**Q:** Quais técnicas são mais usadas em cada nível?
**A:** 
- **Unitário:** White-box (Statement, Branch)
- **Integração:** State Transition, Use Case
- **Sistema:** EP, BVA, Decision Tables
- **Aceitação:** Use Case, Exploratory

---

### Card 29 - Cobertura Combinada (K4)
**Q:** Como medir cobertura usando múltiplas técnicas?
**A:** 
- Mapear requisitos testados
- Rastrear técnicas aplicadas por requisito
- Identificar gaps de cobertura
- Aplicar técnicas complementares nos gaps

---

### Card 30 - Técnicas Ágeis (K3)
**Q:** Quais técnicas são mais adequadas para ambientes ágeis?
**A:** 
- **Exploratory Testing:** Flexível, rápido
- **Checklist-Based:** Regressão rápida
- **Use Case/User Story:** Alinhado com backlog
- **Pairwise:** Otimiza combinações

---

### Card 31 - ROI de Técnicas (K4)
**Q:** Como avaliar ROI (retorno) de técnicas de teste?
**A:** 
- Defeitos encontrados vs tempo investido
- Custo de criação vs reuso
- Manutenibilidade
- Confiança gerada
- Automação possível

---

### Card 32 - Matriz de Decisão (K4)
**Q:** Crie matriz para escolher técnica baseada em contexto.
**A:** 
```
Contexto              | Técnica Recomendada
----------------------|--------------------
Requisitos claros     | EP, BVA, Decision Tables
Requisitos vagos      | Exploratory, Error Guessing
Sistema com estados   | State Transition
Múltiplas variáveis   | Classification Trees
Código crítico        | White-Box (Branch Coverage)
Pouco tempo           | Checklist, Risk-Based
Interação usuário     | Use Case Testing
```

---

## 📊 Resumo do Deck 2.3

**Técnicas Cobertas:**
- ✅ White-Box Testing (8 cards)
- ✅ Experience-Based Testing (16 cards)
- ✅ Comparação de Técnicas (8 cards)

**Distribuição por K-Level:**
- K2 (Conhecimento): 8 cards
- K3 (Aplicação): 14 cards
- K4 (Análise): 10 cards

---

## 🎉 CAPÍTULO 2 COMPLETO!

**Progresso Total Cap 2:**
- ✅ Deck 2.1: 36 cards (EP, BVA, Decision Tables)
- ✅ Deck 2.2: 36 cards (State Transition, Use Case, Classification Trees)
- ✅ Deck 2.3: 32 cards (White-Box + Experience-Based)

**TOTAL CAPÍTULO 2:** 104 flashcards  
**TOTAL GERAL:** 124 flashcards (Cap 1 + Cap 2)

---

**Revisão Sugerida (Spaced Repetition):**
- Dia 1: Todos os 32 cards
- Dia 3: Cards marcados como "difícil"
- Dia 7: Todos os cards novamente
- Dia 14: Revisão completa Cap 2 (104 cards)
- Dia 30: Revisão final antes do exame

---

**Próximos Capítulos:**
- ⏳ Cap 3: Quality Characteristics (ISO 25010)
- ⏳ Cap 4: Reviews
- ⏳ Cap 5: Test Tools

**Quer continuar com flashcards dos outros capítulos ou passar para outro item?**
