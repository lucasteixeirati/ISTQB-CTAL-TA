# OBSOLETO: Simulado completo agora é gerado a partir dos capítulos individuais.
Consulte os arquivos de capítulo em `simulados/` para conteúdo atualizado.

# ISTQB CTAL-TA - Simulado 05: COMPLETO FINAL

**Capítulos:** Todos (1-5)  
**Questões:** 40  
**Tempo:** 120 minutos (CRONOMETRADO)  
**Aprovação:** 26/40 (65%)  
**Meta:** 32/40 (80%)

---

## ⚠️ INSTRUÇÕES IMPORTANTES

1. **Reserve 120 minutos ininterruptos**
2. **Não consulte material durante o simulado**
3. **Marque suas respostas em papel separado**
4. **Simule condições reais de exame**
5. **Analise TODOS os erros ao final**

---

## CAPÍTULO 1: RISK-BASED TESTING (6 questões)

### Questão 1 (K2)
O que é Risk-Based Testing?

A) Testar apenas funcionalidades de alto risco  
B) Priorizar testes baseados em probabilidade e impacto  
C) Executar testes aleatórios  
D) Focar apenas em testes de segurança

**Resposta:** B

---

### Questão 2 (K3)
Sistema tem: Login (P=2, I=5), Pagamento (P=4, I=5), Relatório (P=3, I=2). Qual a ordem de priorização?

A) Pagamento > Login > Relatório  
B) Login > Pagamento > Relatório  
C) Pagamento > Relatório > Login  
D) Relatório > Login > Pagamento

**Resposta:** A  
**Cálculo:** Pagamento(20) > Login(10) > Relatório(6)

---

### Questão 3 (K2)
Diferença entre Product Risk e Project Risk?

A) Product Risk afeta cronograma; Project Risk afeta qualidade  
B) Não há diferença  
C) Product Risk são falhas no software; Project Risk são problemas no processo  
D) Product Risk é mais grave

**Resposta:** C

---

### Questão 4 (K4)
Módulo de pagamento usa nova API e processa transações críticas. Como classificar?

A) Baixa probabilidade, baixo impacto  
B) Alta probabilidade, baixo impacto  
C) Baixa probabilidade, alto impacto  
D) Alta probabilidade, alto impacto

**Resposta:** D  
**Justificativa:** Nova tecnologia = alta probabilidade; Transações críticas = alto impacto

---

### Questão 5 (K3)
Quando re-avaliar riscos?

A) Apenas no início do projeto  
B) Quando há mudanças nos requisitos ou novos defeitos  
C) Apenas no final do projeto  
D) Nunca, análise inicial é suficiente

**Resposta:** B

---

### Questão 6 (K3)
40 horas para testar 5 módulos: A(20), B(15), C(8), D(5), E(3). Como distribuir tempo?

A) 8h cada (igual)  
B) A:15h, B:12h, C:8h, D:3h, E:2h  
C) Testar apenas A e B  
D) A:20h, B:20h, ignorar resto

**Resposta:** B  
**Justificativa:** Distribuição proporcional ao risco mantendo cobertura mínima

---

## CAPÍTULO 2: TEST TECHNIQUES (20 questões)

### Questão 7 (K3) - EP
Campo aceita 18-65 anos. Quantas partições?

A) 2  
B) 3  
C) 4  
D) 5

**Resposta:** B  
**Justificativa:** 1 válida [18-65], 2 inválidas [<18][>65]

---

### Questão 8 (K3) - BVA
Range [1-100]. BVA 3-value testa quais valores?

A) 0, 1, 100, 101  
B) 1, 50, 100  
C) 0, 1, 2, 99, 100, 101  
D) 1, 2, 99, 100

**Resposta:** C

---

### Questão 9 (K3) - Decision Table
2 condições booleanas. Quantas regras em tabela completa?

A) 2  
B) 3  
C) 4  
D) 8

**Resposta:** C  
**Justificativa:** 2^2 = 4

---

### Questão 10 (K4) - Decision Table Collapsed
R1(Y,Y→A) e R2(Y,N→A) podem ser collapsed?

A) Não  
B) Sim, (Y,-→A)  
C) Sim, (-,Y→A)  
D) Apenas com 3 condições

**Resposta:** B

---

### Questão 11 (K3) - State Transition
3 estados, 4 transições válidas. Casos mínimos para 1-switch?

A) 3  
B) 4  
C) 6  
D) 9

**Resposta:** B  
**Justificativa:** 1-switch = todas as transições

---

### Questão 12 (K4) - State Transition Coverage
Diferença entre 0-switch e 1-switch?

A) 0-switch testa estados, 1-switch testa transições  
B) 0-switch é mais rigoroso  
C) Não há diferença  
D) 0-switch testa transições inválidas

**Resposta:** A

---

### Questão 13 (K3) - Use Case
Use Case: 1 main, 2 alternative, 3 exception. Casos mínimos?

A) 3  
B) 4  
C) 6  
D) 12

**Resposta:** C  
**Justificativa:** 1+2+3=6

---

### Questão 14 (K3) - Use Case vs User Story
Qual afirmação está CORRETA?

A) Use Case é mais adequado para ágil  
B) User Story é mais detalhada  
C) Use Case inclui fluxos alternativos e de exceção  
D) User Story substitui Use Case

**Resposta:** C

---

### Questão 15 (K3) - Classification Tree
3 classificações (3, 2, 2 classes). Quantas combinações?

A) 7  
B) 12  
C) 18  
D) 24

**Resposta:** B  
**Justificativa:** 3×2×2=12

---

### Questão 16 (K4) - Classification Tree Strategy
Melhor custo-benefício em seleção de combinações?

A) All combinations  
B) Each choice  
C) Pairwise  
D) Random

**Resposta:** C

---

### Questão 17 (K2) - White-Box
O que mede Statement Coverage?

A) % de decisões  
B) % de linhas executadas  
C) % de branches  
D) % de caminhos

**Resposta:** B

---

### Questão 18 (K3) - Branch Coverage
5 IFs (10 branches), 8 cobertos. Qual a cobertura?

A) 50%  
B) 60%  
C) 80%  
D) 100%

**Resposta:** C  
**Justificativa:** 8/10×100=80%

---

### Questão 19 (K4) - Statement vs Branch
100% Statement mas <100% Branch é possível?

A) Não, são equivalentes  
B) Sim, Statement é mais fraco  
C) Não, Branch é mais fraco  
D) Apenas em linguagens específicas

**Resposta:** B

---

### Questão 20 (K2) - Error Guessing
O que é Error Guessing?

A) Técnica formal baseada em specs  
B) Técnica que usa experiência para antecipar erros  
C) Ferramenta automatizada  
D) Método de análise estática

**Resposta:** B

---

### Questão 21 (K3) - Exploratory Testing
Qual característica NÃO é típica?

A) Design e execução simultâneos  
B) Scripts detalhados pré-definidos  
C) Aprendizado contínuo  
D) Adaptação baseada em resultados

**Resposta:** B

---

### Questão 22 (K3) - Session-Based Testing
O que é Charter?

A) Relatório final  
B) Objetivo da sessão exploratória  
C) Ferramenta de automação  
D) Métrica de cobertura

**Resposta:** B

---

### Questão 23 (K4) - Checklist-Based
Principal LIMITAÇÃO?

A) Muito caro  
B) Requer ferramentas especializadas  
C) Pode ficar desatualizado e criar "checkbox mentality"  
D) Não pode ser usado em ágil

**Resposta:** C

---

### Questão 24 (K4) - Combinação de Técnicas
Melhor estratégia?

A) Apenas técnicas formais  
B) Apenas experience-based  
C) Formais primeiro, depois experience-based para gaps  
D) Escolher apenas uma

**Resposta:** C

---

### Questão 25 (K3) - Seleção de Técnica
Sistema bancário com cálculos complexos. Técnica MAIS apropriada?

A) Exploratory  
B) Decision Tables  
C) State Transition  
D) Error Guessing

**Resposta:** B

---

### Questão 26 (K4) - Técnicas por Nível
Técnica MAIS apropriada para testes de INTEGRAÇÃO?

A) Statement Coverage  
B) Branch Coverage  
C) State Transition  
D) Exploratory

**Resposta:** C

---

## CAPÍTULO 3: QUALITY CHARACTERISTICS (8 questões)

### Questão 27 (K2) - ISO 25010
Quantas características principais?

A) 5  
B) 6  
C) 8  
D) 10

**Resposta:** C

---

### Questão 28 (K3) - Functional Suitability
Sistema calcula impostos corretamente e fornece todas as funções. Quais sub-características?

A) Apenas Correctness  
B) Completeness e Correctness  
C) Apenas Appropriateness  
D) Todas as três

**Resposta:** B

---

### Questão 29 (K3) - Performance Efficiency
Responder <2s com 500 usuários usando max 70% CPU. Quais sub-características?

A) Apenas Time Behaviour  
B) Time Behaviour e Capacity  
C) Time Behaviour, Resource Utilization e Capacity  
D) Apenas Resource Utilization

**Resposta:** C

---

### Questão 30 (K3) - Compatibility
Funcionar em Chrome/Firefox/Safari e integrar com API externa. Quais sub-características?

A) Apenas Co-existence  
B) Apenas Interoperability  
C) Co-existence e Interoperability  
D) Isso é Portability

**Resposta:** C

---

### Questão 31 (K4) - Usability
Acessível para deficientes visuais. Sub-característica MAIS relevante?

A) Learnability  
B) Operability  
C) Accessibility  
D) User Interface Aesthetics

**Resposta:** C

---

### Questão 32 (K3) - Reliability
99.9% uptime e recuperar dados após falha. Quais sub-características?

A) Maturity e Availability  
B) Availability e Recoverability  
C) Fault Tolerance e Maturity  
D) Apenas Availability

**Resposta:** B

---

### Questão 33 (K3) - Security
Apenas autorizados acessam dados e ações são rastreáveis. Quais sub-características?

A) Confidentiality e Accountability  
B) Integrity e Non-repudiation  
C) Apenas Authenticity  
D) Todas

**Resposta:** A

---

### Questão 34 (K4) - Priorização
E-commerce crítico, tempo limitado. Como priorizar?

A) Testar todas igualmente  
B) Focar em Functional Suitability, Security e Performance  
C) Apenas Usability  
D) Apenas características funcionais

**Resposta:** B

---

## CAPÍTULO 4: REVIEWS (4 questões)

### Questão 35 (K2) - Tipos de Review
Tipo MAIS formal?

A) Informal  
B) Walkthrough  
C) Technical Review  
D) Inspection

**Resposta:** D

---

### Questão 36 (K3) - Walkthrough
Papel principal do AUTOR?

A) Observar passivamente  
B) Conduzir a apresentação  
C) Documentar defeitos  
D) Moderar

**Resposta:** B

---

### Questão 37 (K3) - Inspection - Fases
Sequência CORRETA?

A) Planning → Preparation → Meeting → Rework → Follow-up  
B) Preparation → Planning → Meeting → Follow-up → Rework  
C) Planning → Meeting → Preparation → Rework → Follow-up  
D) Meeting → Planning → Preparation → Rework → Follow-up

**Resposta:** A

---

### Questão 38 (K4) - Fatores de Sucesso
Fator MAIS crítico?

A) Usar sempre Inspection  
B) Cultura positiva e não-punitiva  
C) Ferramentas caras  
D) Reviews apenas no final

**Resposta:** B

---

## CAPÍTULO 5: TEST TOOLS (2 questões)

### Questão 39 (K3) - Pilot Project
Por que fazer Pilot Project?

A) Economizar dinheiro  
B) Validar compatibilidade e treinar equipe em escala pequena  
C) Obrigatório por normas  
D) Impressionar stakeholders

**Resposta:** B

---

### Questão 40 (K4) - Quando NÃO Automatizar
Situação onde automação NÃO é recomendada?

A) Regressão executada frequentemente  
B) Funcionalidade estável  
C) Testes raros em funcionalidade instável  
D) Testes de API

**Resposta:** C

---

## GABARITO COMPLETO

**Cap 1 (Q1-6):** 1-B | 2-A | 3-C | 4-D | 5-B | 6-B  
**Cap 2 (Q7-26):** 7-B | 8-C | 9-C | 10-B | 11-B | 12-A | 13-C | 14-C | 15-B | 16-C | 17-B | 18-C | 19-B | 20-B | 21-B | 22-B | 23-C | 24-C | 25-B | 26-C  
**Cap 3 (Q27-34):** 27-C | 28-B | 29-C | 30-C | 31-C | 32-B | 33-A | 34-B  
**Cap 4 (Q35-38):** 35-D | 36-B | 37-A | 38-B  
**Cap 5 (Q39-40):** 39-B | 40-C

---

## ANÁLISE DE DESEMPENHO

**Sua pontuação:** ___/40

### Classificação Geral
- **36-40 (90-100%):** 🏆 EXCELENTE! Pronto para o exame
- **32-35 (80-89%):** ✅ MUITO BOM! Revisar pontos fracos
- **26-31 (65-79%):** ⚠️ BOM. Estudar mais antes do exame
- **0-25 (<65%):** ❌ INSUFICIENTE. Estudo intensivo necessário

### Análise por Capítulo
**Cap 1 - Risk-Based (Q1-6):** ___/6 (___%)  
**Cap 2 - Test Techniques (Q7-26):** ___/20 (___%)  
**Cap 3 - Quality (Q27-34):** ___/8 (___%)  
**Cap 4 - Reviews (Q35-38):** ___/4 (___%)  
**Cap 5 - Tools (Q39-40):** ___/2 (___%)

### Análise por K-Level
**K2 (Conhecimento):** ___/12  
**K3 (Aplicação):** ___/20  
**K4 (Análise):** ___/8

---

## PRÓXIMOS PASSOS

### Se pontuou 80%+ (32/40)
✅ **Você está pronto!**
- [ ] Revisar questões erradas
- [ ] Revisar flashcards dos tópicos fracos
- [ ] Agendar o exame
- [ ] Fazer mais 1-2 simulados para manter ritmo

### Se pontuou 65-79% (26-31/40)
⚠️ **Mais 2 semanas de estudo**
- [ ] Identificar capítulos com <70%
- [ ] Estudar syllabus desses capítulos
- [ ] Revisar todos os flashcards 2x
- [ ] Refazer este simulado em 1 semana
- [ ] Meta: 80%+ antes de agendar exame

### Se pontuou <65% (<26/40)
❌ **Estudo intensivo necessário**
- [ ] Revisar TODO o syllabus
- [ ] Estudar todos os 189 flashcards
- [ ] Refazer simulados 01-04
- [ ] Criar exemplos práticos de cada técnica
- [ ] Refazer este simulado em 2 semanas
- [ ] Não agendar exame ainda

---

## 📊 ESTATÍSTICAS DO SIMULADO

**Distribuição de Questões:**
- Cap 1 (Risk): 15% (6 questões)
- Cap 2 (Techniques): 50% (20 questões) ⭐
- Cap 3 (Quality): 20% (8 questões)
- Cap 4 (Reviews): 10% (4 questões)
- Cap 5 (Tools): 5% (2 questões)

**Níveis K:**
- K2: 30% (12 questões)
- K3: 50% (20 questões)
- K4: 20% (8 questões)

---

## 💡 DICAS FINAIS

1. **Cap 2 é 50% do exame** - Domine técnicas de teste!
2. **Memorize ISO 25010** - 8 características sempre caem
3. **Diferencie tipos de review** - Inspection vs Technical vs Walkthrough
4. **Pratique cálculos** - Risco, cobertura, combinações
5. **Gerencie tempo** - 3 minutos por questão
6. **Leia com atenção** - Palavras como "MAIS", "MENOS", "NÃO"
7. **Elimine alternativas** - Descarte as obviamente erradas
8. **Confie no estudo** - Você se preparou bem!

---

**BOA SORTE! 🍀**

**Lembre-se:** 65% para passar, mas busque 80%+ para ter margem de segurança!
