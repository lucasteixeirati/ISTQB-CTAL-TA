# ISTQB CTAL-TA - Tabela Comparativa de Técnicas de Teste

**Capítulo:** 2 - Test Techniques  
**Objetivo:** Comparação rápida para seleção de técnica apropriada

---

## 📊 TABELA COMPARATIVA COMPLETA

| Técnica | Tipo | K-Level | Quando Usar | Vantagens | Limitações | Exemplo |
|---------|------|---------|-------------|-----------|------------|---------|
| **Equivalence Partitioning (EP)** | Black-Box | K3 | Ranges numéricos, listas de valores, validações | Reduz casos de teste, cobertura sistemática | Não testa fronteiras, assume uniformidade | Campo idade [18-65] → 3 partições |
| **Boundary Value Analysis (BVA)** | Black-Box | K3 | Limites de ranges, tamanhos, valores ordenados | Encontra defeitos em fronteiras (comum) | Não testa meio das partições, muitos casos | [18-65] → testar 17,18,19,64,65,66 |
| **Decision Tables** | Black-Box | K4 | Múltiplas condições, regras de negócio complexas, lógica booleana | Visualização clara, cobertura completa | Explosão combinatória, difícil manutenção | Desconto: VIP? Compra>100? → 4 regras |
| **State Transition** | Black-Box | K4 | Sistemas com estados distintos, workflows, protocolos | Testa mudanças de estado, transições inválidas | Explosão de estados, complexo para 2-switch | Login: Deslogado→Logado→Bloqueado |
| **Use Case Testing** | Black-Box | K3 | Sistemas transacionais, múltiplos atores, aceitação | Baseado em cenários reais, fácil comunicação | Depende de use cases bem escritos | Compra online: main/alt/exception flows |
| **Classification Trees** | Black-Box | K4 | Múltiplas variáveis independentes, combinações complexas | Visualização hierárquica, facilita combinações | Complexo para sistemas simples | Busca: Tipo(3) × Ordem(2) × Filtro(2) |
| **Statement Coverage** | White-Box | K2 | Testes unitários, cobertura básica | Simples de medir, rápido | Cobertura fraca, não garante qualidade | 8 de 10 linhas executadas = 80% |
| **Branch Coverage** | White-Box | K3 | Testes unitários, validação de decisões | Mais forte que Statement, testa TRUE/FALSE | Não testa combinações de condições | 6 de 8 branches = 75% |
| **Error Guessing** | Experience | K2 | Complementar outras técnicas, casos extremos | Rápido, usa experiência, encontra bugs inesperados | Não sistemático, depende de experiência | Data: 29/02 em ano não-bissexto |
| **Exploratory Testing** | Experience | K3 | Requisitos vagos, pouco tempo, buscar bugs inesperados | Flexível, criativo, aprendizado contínuo | Difícil repetir, documentação mínima | Session 90min: explorar upload de arquivos |
| **Checklist-Based** | Experience | K2 | Regressão rápida, validação final, consistência | Rápido, captura conhecimento, fácil usar | Pode ficar desatualizado, "checkbox mentality" | Login: [ ] Senha mascarada? [ ] Limite tentativas? |

---

## 🎯 MATRIZ DE DECISÃO - QUANDO USAR CADA TÉCNICA

### Por Contexto do Sistema

| Contexto | Técnica Recomendada | Justificativa |
|----------|---------------------|---------------|
| **Campos com ranges numéricos** | EP + BVA | EP para partições, BVA para fronteiras |
| **Regras de negócio complexas** | Decision Tables | Visualiza todas as combinações de condições |
| **Sistema com estados (login, carrinho)** | State Transition | Testa mudanças de estado e transições |
| **Fluxos de usuário (compra, cadastro)** | Use Case Testing | Baseado em cenários reais de uso |
| **Múltiplas variáveis independentes** | Classification Trees | Organiza combinações hierarquicamente |
| **Código crítico de segurança** | White-Box (Branch) | Garante cobertura de todas as decisões |
| **Requisitos vagos ou mudando** | Exploratory Testing | Flexível e adaptável |
| **Regressão rápida** | Checklist-Based | Rápido e consistente |

---

### Por Fase do Projeto

| Fase | Técnicas Recomendadas |
|------|----------------------|
| **Análise de Requisitos** | Use Case, Decision Tables |
| **Testes Unitários** | White-Box (Statement, Branch) |
| **Testes de Integração** | State Transition, Use Case |
| **Testes de Sistema** | EP, BVA, Decision Tables, Classification Trees |
| **Testes de Aceitação** | Use Case, Exploratory |
| **Testes de Regressão** | Checklist-Based, Automação |

---

### Por Nível de Teste

| Nível | Técnicas Principais | Técnicas Complementares |
|-------|---------------------|------------------------|
| **Unitário** | Statement Coverage, Branch Coverage | Error Guessing |
| **Integração** | State Transition, Use Case | EP, BVA |
| **Sistema** | EP, BVA, Decision Tables | Classification Trees, Exploratory |
| **Aceitação** | Use Case Testing | Exploratory, Checklist |

---

## 🔄 COMBINAÇÃO DE TÉCNICAS

### Estratégia Recomendada

```
1. TÉCNICAS FORMAIS (Base)
   ├─ EP: Identificar partições
   ├─ BVA: Testar fronteiras
   ├─ Decision Tables: Regras complexas
   └─ State Transition: Fluxos com estados

2. TÉCNICAS COMPLEMENTARES
   ├─ Use Case: Cenários de usuário
   ├─ Classification Trees: Combinações
   └─ White-Box: Cobertura de código

3. TÉCNICAS EXPERIENCE-BASED (Gaps)
   ├─ Error Guessing: Casos extremos
   ├─ Exploratory: Áreas não cobertas
   └─ Checklist: Validação final
```

---

## 📈 COBERTURA POR TÉCNICA

| Técnica | Tipo de Cobertura | Métrica |
|---------|-------------------|---------|
| **EP** | Partições | % de partições testadas |
| **BVA** | Fronteiras | % de fronteiras testadas |
| **Decision Tables** | Regras | % de regras testadas |
| **State Transition** | Estados/Transições | 0-switch (estados), 1-switch (transições), 2-switch (pares) |
| **Use Case** | Fluxos | % de fluxos testados (main/alt/exception) |
| **Classification Trees** | Combinações | Each choice, Pairwise, All combinations |
| **Statement Coverage** | Linhas de código | % de statements executados |
| **Branch Coverage** | Decisões | % de branches (TRUE/FALSE) executados |

---

## 💰 CUSTO vs BENEFÍCIO

| Técnica | Custo de Criação | Custo de Manutenção | Efetividade | ROI |
|---------|------------------|---------------------|-------------|-----|
| **EP** | Baixo | Baixo | Média | Alto |
| **BVA** | Médio | Baixo | Alta | Alto |
| **Decision Tables** | Médio | Médio | Alta | Médio |
| **State Transition** | Alto | Alto | Alta | Médio |
| **Use Case** | Médio | Médio | Alta | Alto |
| **Classification Trees** | Alto | Médio | Média | Médio |
| **White-Box** | Baixo | Baixo | Média | Alto |
| **Error Guessing** | Muito Baixo | Muito Baixo | Variável | Alto |
| **Exploratory** | Baixo | N/A | Alta | Muito Alto |
| **Checklist** | Baixo | Baixo | Média | Alto |

---

## 🎓 DICAS PARA O EXAME

### Palavras-Chave que Indicam Técnica

| Palavra-Chave | Técnica Sugerida |
|---------------|------------------|
| "Range", "Limite", "Entre X e Y" | EP + BVA |
| "Regras", "Condições", "Se...então" | Decision Tables |
| "Estado", "Transição", "Workflow" | State Transition |
| "Fluxo", "Cenário", "Ator", "Use case" | Use Case Testing |
| "Múltiplas variáveis", "Combinações" | Classification Trees |
| "Cobertura de código", "Linhas", "Branches" | White-Box |
| "Experiência", "Intuição", "Antecipar" | Error Guessing |
| "Explorar", "Descobrir", "Aprender" | Exploratory |
| "Lista de verificação", "Checklist" | Checklist-Based |

### Perguntas Típicas do Exame

1. **"Qual técnica é MAIS apropriada para..."**
   - Analise o contexto (ranges → EP/BVA, regras → Decision Tables, estados → State Transition)

2. **"Quantos casos de teste mínimos..."**
   - EP: 1 por partição
   - BVA: 2-value (4 valores) ou 3-value (6 valores)
   - Decision Tables: 2^n regras
   - State Transition: número de transições (1-switch)
   - Use Case: main + alternatives + exceptions

3. **"Qual a cobertura..."**
   - Statement: linhas executadas / total linhas
   - Branch: branches executados / total branches
   - State: 0-switch (estados), 1-switch (transições)

---

## 📝 RESUMO EXECUTIVO

### Top 5 Técnicas Mais Cobradas no Exame

1. **Equivalence Partitioning + BVA** (sempre juntas)
2. **Decision Tables** (cálculo de regras, collapsed)
3. **State Transition** (cobertura 0/1/2-switch)
4. **Use Case Testing** (fluxos main/alt/exception)
5. **White-Box** (Statement vs Branch Coverage)

### Fórmulas Importantes

- **Decision Tables:** Regras = 2^n (n = número de condições)
- **Statement Coverage:** (Linhas executadas / Total linhas) × 100
- **Branch Coverage:** (Branches executados / Total branches) × 100
- **Risco:** Probabilidade × Impacto
- **Classification Trees:** Combinações = Produto de todas as classes

---

**Use esta tabela como referência rápida durante o estudo e revisão!**
