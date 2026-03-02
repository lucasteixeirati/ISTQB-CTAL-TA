# ISTQB CTAL-TA - Flashcards: Quality Characteristics

**Capítulo:** 3 - Testing Software Quality Characteristics  
**Conteúdo:** ISO/IEC 25010 Quality Model  
**Total:** 30 flashcards  
**Revisão:** Dia 1, 3, 7, 14, 30

---

## 🎯 ISO/IEC 25010 - VISÃO GERAL

### Card 1 - Conceito Básico (K2)
**Q:** O que é ISO/IEC 25010?
**A:** Modelo internacional que define 8 características de qualidade de software e suas sub-características.

---

### Card 2 - As 8 Características (K2)
**Q:** Quais as 8 características de qualidade da ISO 25010?
**A:** 
1. Functional Suitability
2. Performance Efficiency
3. Compatibility
4. Usability
5. Reliability
6. Security
7. Maintainability
8. Portability

---

### Card 3 - Uso pelo Test Analyst (K3)
**Q:** Como o Test Analyst usa ISO 25010?
**A:** 
- Identificar requisitos não-funcionais
- Derivar casos de teste específicos
- Priorizar testes por característica
- Comunicar riscos de qualidade

---

## 🎯 FUNCTIONAL SUITABILITY

### Card 4 - Conceito (K2)
**Q:** O que é Functional Suitability?
**A:** Grau em que o produto fornece funções que atendem necessidades declaradas e implícitas sob condições especificadas.

---

### Card 5 - Sub-características (K2)
**Q:** Quais as sub-características de Functional Suitability?
**A:** 
- **Functional Completeness:** Todas as funções necessárias
- **Functional Correctness:** Resultados corretos
- **Functional Appropriateness:** Funções facilitam tarefas

---

### Card 6 - Como Testar (K3)
**Q:** Como testar Functional Suitability?
**A:** 
- EP, BVA, Decision Tables
- Use Case Testing
- Testes de aceitação
- Validação de requisitos funcionais

---

## 🎯 PERFORMANCE EFFICIENCY

### Card 7 - Conceito (K2)
**Q:** O que é Performance Efficiency?
**A:** Desempenho relativo à quantidade de recursos usados sob condições estabelecidas.

---

### Card 8 - Sub-características (K2)
**Q:** Quais as sub-características de Performance Efficiency?
**A:** 
- **Time Behaviour:** Tempos de resposta
- **Resource Utilization:** Uso de CPU, memória, rede
- **Capacity:** Limites máximos suportados

---

### Card 9 - Como Testar (K3)
**Q:** Como testar Performance Efficiency?
**A:** 
- Testes de carga (load testing)
- Testes de stress
- Testes de volume
- Monitoramento de recursos
- Benchmarking

---

### Card 10 - Exemplo Prático (K3)
**Q:** Sistema deve responder em <2s para 1000 usuários simultâneos. Qual característica e como testar?
**A:** 
- **Característica:** Performance Efficiency (Time Behaviour + Capacity)
- **Teste:** Load test com 1000 usuários virtuais, medir tempo de resposta

---

## 🎯 COMPATIBILITY

### Card 11 - Conceito (K2)
**Q:** O que é Compatibility?
**A:** Grau em que o produto pode trocar informações e/ou executar funções enquanto compartilha ambiente com outros produtos.

---

### Card 12 - Sub-características (K2)
**Q:** Quais as sub-características de Compatibility?
**A:** 
- **Co-existence:** Funcionar junto com outros produtos
- **Interoperability:** Trocar e usar informações com outros sistemas

---

### Card 13 - Como Testar (K3)
**Q:** Como testar Compatibility?
**A:** 
- Testes de integração com sistemas externos
- Testes em múltiplos browsers/dispositivos
- Testes de APIs (interoperability)
- Testes de instalação em ambientes compartilhados

---

## 🎯 USABILITY

### Card 14 - Conceito (K2)
**Q:** O que é Usability?
**A:** Grau em que o produto pode ser usado por usuários específicos para atingir objetivos com efetividade, eficiência e satisfação.

---

### Card 15 - Sub-características (K2)
**Q:** Quais as sub-características de Usability?
**A:** 
- **Appropriateness Recognizability:** Usuário reconhece se é apropriado
- **Learnability:** Facilidade de aprender
- **Operability:** Facilidade de operar
- **User Error Protection:** Proteção contra erros
- **User Interface Aesthetics:** Interface agradável
- **Accessibility:** Acessível para pessoas com deficiências

---

### Card 16 - Como Testar (K3)
**Q:** Como testar Usability?
**A:** 
- Testes de usabilidade com usuários reais
- Heurísticas de Nielsen
- Testes de acessibilidade (WCAG)
- Análise de fluxos de navegação
- Testes A/B

---

### Card 17 - Accessibility (K3)
**Q:** O que testar em Accessibility?
**A:** 
- Navegação por teclado
- Compatibilidade com leitores de tela
- Contraste de cores (WCAG)
- Textos alternativos em imagens
- Tamanho de fonte ajustável

---

## 🎯 RELIABILITY

### Card 18 - Conceito (K2)
**Q:** O que é Reliability?
**A:** Grau em que o sistema executa funções especificadas sob condições especificadas por período de tempo especificado.

---

### Card 19 - Sub-características (K2)
**Q:** Quais as sub-características de Reliability?
**A:** 
- **Maturity:** Frequência de falhas
- **Availability:** Sistema operacional quando necessário
- **Fault Tolerance:** Opera apesar de falhas
- **Recoverability:** Recupera dados após falha

---

### Card 20 - Como Testar (K3)
**Q:** Como testar Reliability?
**A:** 
- Testes de longa duração (soak testing)
- Testes de recuperação (recovery testing)
- Testes de failover
- Injeção de falhas
- Monitoramento de uptime

---

## 🎯 SECURITY

### Card 21 - Conceito (K2)
**Q:** O que é Security?
**A:** Grau em que o produto protege informações e dados para que pessoas/sistemas tenham acesso apropriado ao seu nível de autorização.

---

### Card 22 - Sub-características (K2)
**Q:** Quais as sub-características de Security?
**A:** 
- **Confidentiality:** Dados acessíveis apenas a autorizados
- **Integrity:** Prevenção de modificação não autorizada
- **Non-repudiation:** Ações podem ser provadas
- **Accountability:** Ações rastreáveis
- **Authenticity:** Identidade comprovável

---

### Card 23 - Como Testar (K3)
**Q:** Como testar Security?
**A:** 
- Testes de penetração
- Análise de vulnerabilidades (OWASP Top 10)
- Testes de autenticação/autorização
- Testes de criptografia
- SQL Injection, XSS, CSRF

---

## 🎯 MAINTAINABILITY

### Card 24 - Conceito (K2)
**Q:** O que é Maintainability?
**A:** Grau de efetividade e eficiência com que o produto pode ser modificado para melhorias, correções ou adaptações.

---

### Card 25 - Sub-características (K2)
**Q:** Quais as sub-características de Maintainability?
**A:** 
- **Modularity:** Componentes independentes
- **Reusability:** Componentes reutilizáveis
- **Analysability:** Facilidade de diagnosticar problemas
- **Modifiability:** Facilidade de modificar
- **Testability:** Facilidade de testar

---

### Card 26 - Como Testar (K3)
**Q:** Como avaliar Maintainability?
**A:** 
- Análise de código (complexidade ciclomática)
- Code reviews
- Análise de cobertura de testes
- Métricas de acoplamento/coesão
- Tempo para implementar mudanças

---

## 🎯 PORTABILITY

### Card 27 - Conceito (K2)
**Q:** O que é Portability?
**A:** Grau de efetividade e eficiência com que o sistema pode ser transferido de um ambiente para outro.

---

### Card 28 - Sub-características (K2)
**Q:** Quais as sub-características de Portability?
**A:** 
- **Adaptability:** Adapta-se a diferentes ambientes
- **Installability:** Facilidade de instalar
- **Replaceability:** Pode substituir outro produto

---

### Card 29 - Como Testar (K3)
**Q:** Como testar Portability?
**A:** 
- Testes em múltiplos SOs (Windows, Linux, Mac)
- Testes de instalação/desinstalação
- Testes de migração de dados
- Testes em diferentes configurações de hardware
- Testes de containerização (Docker)

---

## 🎯 APLICAÇÃO PRÁTICA

### Card 30 - Priorização (K4)
**Q:** Como priorizar características de qualidade para teste?
**A:** 
1. Identificar características críticas para o negócio
2. Avaliar riscos por característica
3. Considerar requisitos não-funcionais
4. Alocar tempo proporcionalmente ao risco
5. Documentar decisões de priorização

---

## 📊 Resumo do Deck 3

**Características Cobertas:**
- ✅ ISO 25010 Overview (3 cards)
- ✅ Functional Suitability (3 cards)
- ✅ Performance Efficiency (4 cards)
- ✅ Compatibility (3 cards)
- ✅ Usability (4 cards)
- ✅ Reliability (3 cards)
- ✅ Security (3 cards)
- ✅ Maintainability (3 cards)
- ✅ Portability (3 cards)
- ✅ Aplicação Prática (1 card)

**Distribuição por K-Level:**
- K2 (Conhecimento): 17 cards
- K3 (Aplicação): 12 cards
- K4 (Análise): 1 card

**Próximo Deck:** Cap 4 - Reviews

---

**Revisão Sugerida (Spaced Repetition):**
- Dia 1: Todos os 30 cards
- Dia 3: Cards marcados como "difícil"
- Dia 7: Todos os cards novamente
- Dia 14: Revisão geral
- Dia 30: Revisão final antes do exame

---

**Progresso Total:**
- ✅ Cap 1: 20 cards (Risk-Based Testing)
- ✅ Cap 2: 104 cards (Test Techniques)
- ✅ Cap 3: 30 cards (Quality Characteristics)
- ⏳ Cap 4: Pendente (Reviews)
- ⏳ Cap 5: Pendente (Test Tools)

**TOTAL ATÉ AGORA:** 154 flashcards
