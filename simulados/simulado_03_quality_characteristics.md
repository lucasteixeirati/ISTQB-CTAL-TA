# ISTQB CTAL-TA - Simulado 03: Quality Characteristics

**Capítulo:** 3 - Testing Software Quality Characteristics  
**Questões:** 10  
**Tempo sugerido:** 30 minutos  
**Aprovação:** 7/10 (70%)

---

## Questão 1 (K2) - ISO 25010
Quantas características de qualidade principais a ISO/IEC 25010 define?

A) 5 características  
B) 6 características  
C) 8 características  
D) 10 características

**Resposta:** C  
**Justificativa:** ISO 25010 define 8 características: Functional Suitability, Performance Efficiency, Compatibility, Usability, Reliability, Security, Maintainability, Portability.

---

## Questão 2 (K3) - Functional Suitability
Sistema deve calcular impostos corretamente e fornecer todas as funções necessárias. Quais sub-características de Functional Suitability estão envolvidas?

A) Apenas Functional Correctness  
B) Functional Completeness e Functional Correctness  
C) Functional Appropriateness apenas  
D) Todas as três sub-características

**Resposta:** B  
**Justificativa:** 
- Functional Completeness: Todas as funções necessárias
- Functional Correctness: Resultados corretos (cálculos)

---

## Questão 3 (K3) - Performance Efficiency
Sistema deve responder em <2s com 500 usuários simultâneos usando no máximo 70% de CPU. Quais sub-características são testadas?

A) Apenas Time Behaviour  
B) Time Behaviour e Capacity  
C) Time Behaviour, Resource Utilization e Capacity  
D) Apenas Resource Utilization

**Resposta:** C  
**Justificativa:** 
- Time Behaviour: <2s resposta
- Resource Utilization: 70% CPU
- Capacity: 500 usuários simultâneos

---

## Questão 4 (K3) - Compatibility
Aplicação web deve funcionar em Chrome, Firefox e Safari, e integrar com API de pagamento externa. Quais sub-características?

A) Apenas Co-existence  
B) Apenas Interoperability  
C) Co-existence e Interoperability  
D) Nenhuma, isso é Portability

**Resposta:** C  
**Justificativa:** 
- Co-existence: Funcionar em múltiplos browsers
- Interoperability: Integrar com API externa

---

## Questão 5 (K4) - Usability
Sistema deve ser acessível para pessoas com deficiência visual. Qual sub-característica de Usability é MAIS relevante?

A) Learnability  
B) Operability  
C) Accessibility  
D) User Interface Aesthetics

**Resposta:** C  
**Justificativa:** Accessibility trata especificamente de tornar o sistema utilizável por pessoas com deficiências (visual, auditiva, motora).

---

## Questão 6 (K3) - Reliability
Sistema bancário deve ter 99.9% uptime e recuperar dados em caso de falha. Quais sub-características?

A) Maturity e Availability  
B) Availability e Recoverability  
C) Fault Tolerance e Maturity  
D) Apenas Availability

**Resposta:** B  
**Justificativa:** 
- Availability: 99.9% uptime (sistema disponível)
- Recoverability: Recuperar dados após falha

---

## Questão 7 (K3) - Security
Sistema deve garantir que apenas usuários autorizados acessem dados sensíveis e que todas as ações sejam rastreáveis. Quais sub-características?

A) Confidentiality e Accountability  
B) Integrity e Non-repudiation  
C) Authenticity apenas  
D) Todas as sub-características de Security

**Resposta:** A  
**Justificativa:** 
- Confidentiality: Apenas autorizados acessam
- Accountability: Ações rastreáveis

---

## Questão 8 (K3) - Maintainability
Código deve ser fácil de modificar e testar. Quais sub-características de Maintainability são MAIS relevantes?

A) Modularity e Reusability  
B) Modifiability e Testability  
C) Analysability apenas  
D) Todas igualmente

**Resposta:** B  
**Justificativa:** 
- Modifiability: Facilidade de modificar
- Testability: Facilidade de testar

---

## Questão 9 (K3) - Portability
Aplicação deve ser facilmente instalada em Windows, Linux e Mac. Qual sub-característica?

A) Adaptability  
B) Installability  
C) Replaceability  
D) Todas as três

**Resposta:** B  
**Justificativa:** Installability trata da facilidade de instalar/desinstalar em diferentes ambientes.

---

## Questão 10 (K4) - Priorização
Projeto tem tempo limitado. Sistema é e-commerce crítico. Como priorizar características para teste?

A) Testar todas igualmente  
B) Focar em Functional Suitability, Security e Performance  
C) Focar apenas em Usability  
D) Testar apenas características funcionais

**Resposta:** B  
**Justificativa:** Para e-commerce crítico:
- Functional Suitability: Funções devem funcionar corretamente
- Security: Dados de pagamento sensíveis
- Performance: Experiência do usuário e conversão
Priorizar baseado em risco e criticidade do negócio.

---

## Gabarito Rápido
1-C | 2-B | 3-C | 4-C | 5-C | 6-B | 7-A | 8-B | 9-B | 10-B

---

## Análise de Desempenho

**Sua pontuação:** ___/10

- **9-10 acertos (90-100%):** Excelente! Domínio de ISO 25010
- **7-8 acertos (70-80%):** Bom! Revisar questões erradas
- **5-6 acertos (50-60%):** Regular. Estudar Cap 3 novamente
- **0-4 acertos (<50%):** Insuficiente. Revisar flashcards Cap 3

---

## Análise por Característica

**Conceitos Gerais (Q1):** ___/1

**Características Funcionais (Q2-4):** ___/3
- Functional Suitability
- Performance Efficiency
- Compatibility

**Características de Uso (Q5-7):** ___/3
- Usability
- Reliability
- Security

**Características Técnicas (Q8-9):** ___/2
- Maintainability
- Portability

**Aplicação Prática (Q10):** ___/1

---

## Próximos Passos

**Se acertou 70%+:**
- [ ] Revisar questões erradas
- [ ] Revisar flashcards Cap 3 (30 cards)
- [ ] Avançar para Simulado 04 (Reviews + Tools)

**Se acertou <70%:**
- [ ] Estudar ISO 25010 completo
- [ ] Memorizar as 8 características e sub-características
- [ ] Criar exemplos práticos de cada característica
- [ ] Refazer este simulado em 3 dias

---

**Dica:** Memorize as 8 características e suas sub-características. São frequentemente cobradas no exame!
