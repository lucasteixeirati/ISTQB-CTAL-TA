# ISTQB CTAL-TA - Resumo Visual ISO/IEC 25010

**Capítulo:** 3 - Testing Software Quality Characteristics  
**Objetivo:** Memorização rápida das 8 características e sub-características

---

## 🎯 VISÃO GERAL - AS 8 CARACTERÍSTICAS

```
ISO/IEC 25010 - SOFTWARE QUALITY MODEL
│
├─ 1. FUNCTIONAL SUITABILITY (Adequação Funcional)
├─ 2. PERFORMANCE EFFICIENCY (Eficiência de Performance)
├─ 3. COMPATIBILITY (Compatibilidade)
├─ 4. USABILITY (Usabilidade)
├─ 5. RELIABILITY (Confiabilidade)
├─ 6. SECURITY (Segurança)
├─ 7. MAINTAINABILITY (Manutenibilidade)
└─ 8. PORTABILITY (Portabilidade)
```

---

## 📊 DETALHAMENTO COMPLETO

### 1️⃣ FUNCTIONAL SUITABILITY
**Definição:** Grau em que o produto fornece funções que atendem necessidades

```
FUNCTIONAL SUITABILITY
├─ Functional Completeness (Completude)
│  └─ Todas as funções necessárias estão presentes?
├─ Functional Correctness (Correção)
│  └─ Resultados corretos e precisos?
└─ Functional Appropriateness (Apropriação)
   └─ Funções facilitam as tarefas?
```

**Como Testar:**
- EP, BVA, Decision Tables
- Use Case Testing
- Testes de aceitação

**Exemplo:** Sistema de e-commerce deve calcular frete corretamente (Correctness), ter todas as formas de pagamento (Completeness), e facilitar a compra (Appropriateness).

---

### 2️⃣ PERFORMANCE EFFICIENCY
**Definição:** Desempenho relativo aos recursos usados

```
PERFORMANCE EFFICIENCY
├─ Time Behaviour (Comportamento Temporal)
│  └─ Tempos de resposta, processamento, throughput
├─ Resource Utilization (Utilização de Recursos)
│  └─ CPU, memória, disco, rede
└─ Capacity (Capacidade)
   └─ Limites máximos suportados
```

**Como Testar:**
- Load Testing (JMeter, Gatling)
- Stress Testing
- Volume Testing
- Monitoramento de recursos

**Exemplo:** Sistema deve responder em <2s (Time), usar max 70% CPU (Resource), suportar 1000 usuários simultâneos (Capacity).

---

### 3️⃣ COMPATIBILITY
**Definição:** Grau de troca de informações e coexistência com outros produtos

```
COMPATIBILITY
├─ Co-existence (Coexistência)
│  └─ Funciona junto com outros produtos no mesmo ambiente?
└─ Interoperability (Interoperabilidade)
   └─ Troca informações com outros sistemas?
```

**Como Testar:**
- Testes de integração
- Testes multi-browser/dispositivo
- Testes de API
- Testes de instalação compartilhada

**Exemplo:** App funciona em Chrome/Firefox/Safari (Co-existence) e integra com API de pagamento (Interoperability).

---

### 4️⃣ USABILITY
**Definição:** Grau de uso efetivo, eficiente e satisfatório

```
USABILITY
├─ Appropriateness Recognizability (Reconhecimento de Adequação)
│  └─ Usuário reconhece se é apropriado para suas necessidades?
├─ Learnability (Aprendizagem)
│  └─ Fácil de aprender a usar?
├─ Operability (Operabilidade)
│  └─ Fácil de operar e controlar?
├─ User Error Protection (Proteção contra Erro)
│  └─ Protege usuário de cometer erros?
├─ User Interface Aesthetics (Estética da Interface)
│  └─ Interface agradável e satisfatória?
└─ Accessibility (Acessibilidade)
   └─ Utilizável por pessoas com deficiências?
```

**Como Testar:**
- Testes de usabilidade com usuários
- Heurísticas de Nielsen
- Testes de acessibilidade (WCAG)
- Testes A/B

**Exemplo:** Sistema bancário deve ser intuitivo (Learnability), prevenir transferências erradas (Error Protection), e funcionar com leitores de tela (Accessibility).

---

### 5️⃣ RELIABILITY
**Definição:** Grau de execução de funções sob condições por período especificado

```
RELIABILITY
├─ Maturity (Maturidade)
│  └─ Frequência de falhas é baixa?
├─ Availability (Disponibilidade)
│  └─ Sistema operacional quando necessário?
├─ Fault Tolerance (Tolerância a Falhas)
│  └─ Opera apesar de falhas de hardware/software?
└─ Recoverability (Recuperabilidade)
   └─ Recupera dados e restabelece estado após falha?
```

**Como Testar:**
- Soak Testing (longa duração)
- Recovery Testing
- Failover Testing
- Injeção de falhas
- Monitoramento de uptime

**Exemplo:** Sistema deve ter 99.9% uptime (Availability), continuar operando se um servidor cair (Fault Tolerance), e recuperar dados após crash (Recoverability).

---

### 6️⃣ SECURITY
**Definição:** Grau de proteção de informações e dados

```
SECURITY
├─ Confidentiality (Confidencialidade)
│  └─ Dados acessíveis apenas a autorizados?
├─ Integrity (Integridade)
│  └─ Previne modificação não autorizada?
├─ Non-repudiation (Não-repúdio)
│  └─ Ações podem ser provadas?
├─ Accountability (Responsabilização)
│  └─ Ações rastreáveis a uma entidade?
└─ Authenticity (Autenticidade)
   └─ Identidade pode ser provada?
```

**Como Testar:**
- Penetration Testing
- Vulnerability Scanning (OWASP Top 10)
- Testes de autenticação/autorização
- Testes de criptografia
- SQL Injection, XSS, CSRF

**Exemplo:** Sistema deve criptografar senhas (Confidentiality), registrar todas as ações (Accountability), e validar identidade com 2FA (Authenticity).

---

### 7️⃣ MAINTAINABILITY
**Definição:** Grau de efetividade para modificar o produto

```
MAINTAINABILITY
├─ Modularity (Modularidade)
│  └─ Componentes independentes e isolados?
├─ Reusability (Reusabilidade)
│  └─ Componentes podem ser reutilizados?
├─ Analysability (Analisabilidade)
│  └─ Fácil diagnosticar problemas e causas?
├─ Modifiability (Modificabilidade)
│  └─ Fácil modificar sem introduzir defeitos?
└─ Testability (Testabilidade)
   └─ Fácil testar modificações?
```

**Como Testar:**
- Code Reviews
- Análise de complexidade ciclomática
- Métricas de acoplamento/coesão
- Análise de cobertura de testes
- Tempo para implementar mudanças

**Exemplo:** Código bem modularizado (Modularity), com funções reutilizáveis (Reusability), e alta cobertura de testes (Testability).

---

### 8️⃣ PORTABILITY
**Definição:** Grau de transferência entre ambientes

```
PORTABILITY
├─ Adaptability (Adaptabilidade)
│  └─ Adapta-se a diferentes ambientes?
├─ Installability (Instalabilidade)
│  └─ Fácil instalar/desinstalar?
└─ Replaceability (Substituibilidade)
   └─ Pode substituir outro produto similar?
```

**Como Testar:**
- Testes em múltiplos SOs (Windows, Linux, Mac)
- Testes de instalação/desinstalação
- Testes de migração de dados
- Testes em diferentes configurações
- Containerização (Docker)

**Exemplo:** App funciona em Windows/Linux/Mac (Adaptability), instala em 3 cliques (Installability), e pode substituir sistema legado (Replaceability).

---

## 🎯 MNEMÔNICO PARA MEMORIZAR

**F**uncional **P**erformance **C**ompatibility **U**sability **R**eliability **S**ecurity **M**aintainability **P**ortability

**Frase:** **"F**aça **P**rojetos **C**om **U**ma **R**igidez **S**obre **M**anutenção e **P**ortabilidade"

---

## 📊 TABELA RESUMO - CARACTERÍSTICAS E SUB-CARACTERÍSTICAS

| # | Característica | Sub-características (Total) | Foco Principal |
|---|----------------|----------------------------|----------------|
| 1 | Functional Suitability | 3 | O QUE o sistema faz |
| 2 | Performance Efficiency | 3 | QUÃO RÁPIDO faz |
| 3 | Compatibility | 2 | INTEGRAÇÃO com outros |
| 4 | Usability | 6 | FACILIDADE de uso |
| 5 | Reliability | 4 | CONFIANÇA no sistema |
| 6 | Security | 5 | PROTEÇÃO de dados |
| 7 | Maintainability | 5 | FACILIDADE de manter |
| 8 | Portability | 3 | TRANSFERÊNCIA entre ambientes |

**Total:** 8 características, 31 sub-características

---

## 🎓 DICAS PARA O EXAME

### Perguntas Típicas

**Tipo 1:** "Sistema deve [requisito]. Qual característica?"
- Identifique palavras-chave (tempo → Performance, segurança → Security)

**Tipo 2:** "Quais sub-características estão envolvidas?"
- Leia com atenção, pode ter múltiplas (ex: "responder rápido com muitos usuários" = Time Behaviour + Capacity)

**Tipo 3:** "Como testar [característica]?"
- Functional → técnicas black-box
- Performance → load/stress testing
- Security → penetration testing
- Usability → testes com usuários

### Palavras-Chave por Característica

| Característica | Palavras-Chave |
|----------------|----------------|
| Functional | Funções, requisitos, correto, completo |
| Performance | Tempo, resposta, CPU, memória, usuários simultâneos |
| Compatibility | Integração, API, browser, coexistir |
| Usability | Fácil, intuitivo, aprender, acessível, deficiência |
| Reliability | Disponível, uptime, falha, recuperar |
| Security | Senha, criptografia, autorização, vulnerabilidade |
| Maintainability | Modificar, manter, código, modular |
| Portability | Instalar, SO, ambiente, migrar |

---

## 💡 PRIORIZAÇÃO DE CARACTERÍSTICAS

### Por Tipo de Sistema

| Tipo de Sistema | Características Prioritárias |
|-----------------|------------------------------|
| **E-commerce** | Functional, Security, Performance, Usability |
| **Sistema Bancário** | Security, Reliability, Functional |
| **Aplicativo Mobile** | Usability, Performance, Compatibility |
| **Sistema Crítico (Saúde)** | Reliability, Security, Functional |
| **Software Open Source** | Maintainability, Portability, Functional |
| **Sistema Legado** | Maintainability, Portability |

---

## 📝 CHECKLIST DE MEMORIZAÇÃO

Teste seu conhecimento:

- [ ] Consigo listar as 8 características de memória?
- [ ] Sei quantas sub-características cada uma tem?
- [ ] Consigo dar exemplo de cada característica?
- [ ] Sei como testar cada característica?
- [ ] Consigo identificar característica por palavras-chave?
- [ ] Sei priorizar características por tipo de sistema?

**Meta:** Responder SIM para todas antes do exame!

---

**Use este resumo para revisão rápida antes do exame!**
