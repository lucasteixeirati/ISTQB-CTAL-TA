# ISTQB CTAL-TA - Fluxograma de Seleção de Técnicas

**Capítulo:** 2 - Test Techniques  
**Objetivo:** Guia de decisão rápida para escolher técnica apropriada

---

## 🎯 FLUXOGRAMA PRINCIPAL

```
INÍCIO: Preciso testar uma funcionalidade
│
├─ Tenho acesso ao CÓDIGO-FONTE?
│  │
│  ├─ SIM → WHITE-BOX TESTING
│  │  │
│  │  ├─ Nível UNITÁRIO?
│  │  │  ├─ SIM → Statement Coverage + Branch Coverage
│  │  │  └─ NÃO → Considerar Black-Box
│  │  │
│  │  └─ Precisa COBERTURA DE CÓDIGO?
│  │     ├─ Básica → Statement Coverage
│  │     └─ Rigorosa → Branch Coverage
│  │
│  └─ NÃO → BLACK-BOX TESTING (continua abaixo)
│
├─ Tipo de INPUT/DADOS?
│  │
│  ├─ RANGES NUMÉRICOS (ex: idade 18-65)
│  │  └─ EP (partições) + BVA (fronteiras)
│  │
│  ├─ MÚLTIPLAS CONDIÇÕES/REGRAS (ex: desconto baseado em VIP + valor)
│  │  └─ Decision Tables
│  │
│  ├─ MÚLTIPLAS VARIÁVEIS INDEPENDENTES (ex: busca com tipo+ordem+filtro)
│  │  └─ Classification Trees
│  │
│  └─ LISTAS DE VALORES DISCRETOS (ex: estado civil)
│     └─ EP (uma partição por valor)
│
├─ Sistema tem ESTADOS/FLUXOS?
│  │
│  ├─ ESTADOS DISTINTOS (ex: login, carrinho, checkout)
│  │  └─ State Transition Testing
│  │
│  ├─ CENÁRIOS DE USUÁRIO (ex: comprar produto)
│  │  └─ Use Case Testing
│  │
│  └─ WORKFLOWS COMPLEXOS
│     └─ State Transition + Use Case
│
├─ Contexto do PROJETO?
│  │
│  ├─ REQUISITOS VAGOS/MUDANDO
│  │  └─ Exploratory Testing
│  │
│  ├─ POUCO TEMPO DISPONÍVEL
│  │  └─ Checklist-Based + Exploratory
│  │
│  ├─ REGRESSÃO RÁPIDA
│  │  └─ Checklist-Based
│  │
│  └─ COMPLEMENTAR TESTES FORMAIS
│     └─ Error Guessing + Exploratory
│
└─ FIM: Técnica selecionada
```

---

## 🔍 ÁRVORE DE DECISÃO DETALHADA

### Decisão 1: Acesso ao Código?

```
Tenho acesso ao código-fonte?
│
├─ SIM
│  └─ É teste UNITÁRIO?
│     ├─ SIM → WHITE-BOX (Statement/Branch Coverage)
│     └─ NÃO → BLACK-BOX (mais apropriado para integração/sistema)
│
└─ NÃO
   └─ Prosseguir para BLACK-BOX
```

---

### Decisão 2: Tipo de Entrada/Dados?

```
Qual o tipo de entrada?
│
├─ RANGES/INTERVALOS (numéricos, datas, tamanhos)
│  │
│  ├─ Precisa testar PARTIÇÕES?
│  │  └─ SIM → Equivalence Partitioning
│  │
│  └─ Precisa testar FRONTEIRAS?
│     └─ SIM → Boundary Value Analysis
│     └─ IDEAL → EP + BVA (combinados)
│
├─ CONDIÇÕES BOOLEANAS (múltiplos IFs)
│  │
│  ├─ 2-3 condições simples
│  │  └─ Decision Tables
│  │
│  └─ Muitas condições (>4)
│     └─ Decision Tables (considerar collapsed)
│
├─ MÚLTIPLAS VARIÁVEIS INDEPENDENTES
│  │
│  ├─ Precisa VISUALIZAÇÃO HIERÁRQUICA?
│  │  └─ SIM → Classification Trees
│  │
│  └─ Precisa OTIMIZAR COMBINAÇÕES?
│     └─ SIM → Classification Trees (pairwise)
│
└─ LISTAS DISCRETAS (dropdown, radio buttons)
   └─ Equivalence Partitioning (1 partição por opção)
```

---

### Decisão 3: Sistema tem Estados?

```
Sistema muda de estado?
│
├─ SIM - Estados DISTINTOS (login, bloqueado, ativo)
│  │
│  ├─ Precisa testar TRANSIÇÕES?
│  │  └─ State Transition Testing
│  │     ├─ Cobertura básica → 0-switch (todos os estados)
│  │     ├─ Cobertura padrão → 1-switch (todas as transições)
│  │     └─ Cobertura rigorosa → 2-switch (pares de transições)
│  │
│  └─ Precisa testar TRANSIÇÕES INVÁLIDAS?
│     └─ SIM → State Transition (incluir casos negativos)
│
├─ SIM - FLUXOS DE USUÁRIO (compra, cadastro)
│  │
│  └─ Use Case Testing
│     ├─ Main Flow (caminho feliz)
│     ├─ Alternative Flows (variações)
│     └─ Exception Flows (erros)
│
└─ NÃO
   └─ Considerar outras técnicas
```

---

### Decisão 4: Contexto do Projeto?

```
Qual o contexto?
│
├─ REQUISITOS BEM DEFINIDOS
│  └─ Técnicas FORMAIS (EP, BVA, Decision Tables, Use Case)
│
├─ REQUISITOS VAGOS/INCOMPLETOS
│  └─ Exploratory Testing (aprender enquanto testa)
│
├─ POUCO TEMPO DISPONÍVEL
│  │
│  ├─ Primeira vez testando?
│  │  └─ Exploratory (rápido e efetivo)
│  │
│  └─ Já testou antes?
│     └─ Checklist-Based (regressão rápida)
│
├─ COMPLEMENTAR TESTES EXISTENTES
│  │
│  ├─ Buscar BUGS INESPERADOS?
│  │  └─ Error Guessing + Exploratory
│  │
│  └─ Validação FINAL?
│     └─ Checklist-Based
│
└─ PROJETO ÁGIL (sprints curtos)
   └─ Use Case (user stories) + Exploratory + Checklist
```

---

## 🎯 GUIA RÁPIDO POR CENÁRIO

### Cenário 1: Campo de Formulário

```
Campo de formulário (ex: idade, CEP, email)
│
├─ Tem RANGE/LIMITE?
│  └─ SIM → EP + BVA
│     Exemplo: Idade [18-65]
│     - EP: 3 partições (<18, 18-65, >65)
│     - BVA: Testar 17, 18, 19, 64, 65, 66
│
├─ Tem FORMATO ESPECÍFICO?
│  └─ SIM → EP (válido/inválido) + Error Guessing
│     Exemplo: Email
│     - EP: formato válido, formato inválido
│     - Error Guessing: casos especiais (@@ , espaços, etc)
│
└─ É LISTA FECHADA?
   └─ SIM → EP (1 partição por opção)
      Exemplo: Estado Civil (Solteiro, Casado, Divorciado, Viúvo)
      - 4 partições válidas + 1 inválida
```

---

### Cenário 2: Regra de Negócio

```
Regra de negócio complexa
│
├─ Tem MÚLTIPLAS CONDIÇÕES?
│  └─ SIM → Decision Tables
│     Exemplo: Desconto baseado em VIP + Valor + Cupom
│     - Criar tabela com todas as combinações
│     - Considerar collapsed se muitas regras
│
├─ Tem CÁLCULOS COMPLEXOS?
│  └─ SIM → EP + BVA + Decision Tables
│     Exemplo: Cálculo de juros
│     - EP/BVA para valores de entrada
│     - Decision Tables para regras de aplicação
│
└─ Tem DEPENDÊNCIAS ENTRE CONDIÇÕES?
   └─ SIM → Decision Tables + Classification Trees
```

---

### Cenário 3: Fluxo de Processo

```
Fluxo de processo (ex: compra, cadastro)
│
├─ Tem ESTADOS CLAROS?
│  └─ SIM → State Transition
│     Exemplo: Carrinho (vazio → com itens → checkout → pago)
│     - Mapear todos os estados
│     - Testar transições válidas e inválidas
│
├─ Tem INTERAÇÃO COM USUÁRIO?
│  └─ SIM → Use Case Testing
│     Exemplo: Comprar produto
│     - Main: Selecionar → Adicionar → Pagar → Confirmar
│     - Alternative: Aplicar cupom, escolher frete
│     - Exception: Pagamento recusado, sem estoque
│
└─ É WORKFLOW COMPLEXO?
   └─ SIM → State Transition + Use Case (combinados)
```

---

### Cenário 4: Sistema Legado/Sem Documentação

```
Sistema legado sem documentação
│
├─ PRIMEIRA VEZ TESTANDO?
│  └─ SIM → Exploratory Testing
│     - Session-based (90min com charter)
│     - Aprender sistema enquanto testa
│     - Documentar descobertas
│
├─ JÁ CONHECE O SISTEMA?
│  └─ SIM → Checklist-Based
│     - Criar checklist baseado em experiência
│     - Regressão rápida
│
└─ PRECISA COBERTURA SISTEMÁTICA?
   └─ SIM → Reverse Engineering
      - Mapear funcionalidades
      - Aplicar EP, BVA, Use Case
```

---

## 📊 MATRIZ DE DECISÃO RÁPIDA

| Se você tem... | Use... |
|----------------|--------|
| Range numérico | EP + BVA |
| Múltiplas condições | Decision Tables |
| Estados do sistema | State Transition |
| Cenários de usuário | Use Case |
| Múltiplas variáveis | Classification Trees |
| Código-fonte (unitário) | White-Box (Statement/Branch) |
| Requisitos vagos | Exploratory |
| Pouco tempo | Checklist + Exploratory |
| Complementar testes | Error Guessing |
| Regressão rápida | Checklist-Based |

---

## 🎓 PERGUNTAS PARA GUIAR A DECISÃO

Faça estas perguntas para escolher a técnica:

1. **Tenho acesso ao código?**
   - SIM → Considerar White-Box
   - NÃO → Black-Box

2. **Qual o tipo de entrada?**
   - Ranges → EP + BVA
   - Condições → Decision Tables
   - Variáveis múltiplas → Classification Trees

3. **Sistema muda de estado?**
   - SIM → State Transition
   - NÃO → Outras técnicas

4. **Há fluxos de usuário?**
   - SIM → Use Case
   - NÃO → Outras técnicas

5. **Requisitos estão claros?**
   - SIM → Técnicas formais
   - NÃO → Exploratory

6. **Quanto tempo tenho?**
   - Muito → Técnicas formais completas
   - Pouco → Checklist + Exploratory

7. **É primeira vez testando?**
   - SIM → Exploratory + técnicas formais
   - NÃO → Checklist (regressão)

---

## 💡 DICA FINAL

**Na dúvida, combine técnicas!**

Estratégia recomendada:
1. **Base:** EP + BVA (sempre aplicável)
2. **Complemento:** Decision Tables ou State Transition (se aplicável)
3. **Finalização:** Error Guessing + Exploratory (gaps)
4. **Regressão:** Checklist-Based (manutenção)

---

**Use este fluxograma durante o estudo e no exame para decisões rápidas!**
