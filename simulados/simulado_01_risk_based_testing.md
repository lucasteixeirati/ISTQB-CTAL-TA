# ISTQB CTAL-TA - Simulado 01: Risk-Based Testing
**Capítulo:** 1 - The Test Analyst's Tasks in Risk-Based Testing  
**Questões:** 10  
**Tempo sugerido:** 30 minutos  
**Aprovação:** 7/10 (70%)

---

## Questão 1 (K2)
Qual das seguintes afirmações descreve MELHOR o conceito de Risk-Based Testing?

A) Testar apenas funcionalidades de alto risco e ignorar as de baixo risco  
B) Priorizar testes baseados na probabilidade e impacto de falhas  
C) Executar testes aleatórios para identificar riscos desconhecidos  
D) Focar exclusivamente em testes de segurança e performance  

**Resposta:** B  
**Justificativa:** Risk-Based Testing prioriza testes baseados no nível de risco (probabilidade × impacto), não ignora baixo risco (A), não é aleatório (C) e não foca apenas segurança (D).

---

## Questão 2 (K2)
Qual é a diferença entre Product Risk e Project Risk?

A) Product Risk afeta o cronograma; Project Risk afeta a qualidade  
B) Product Risk é técnico; Project Risk é gerencial  
C) Product Risk são falhas no software; Project Risk são problemas no processo  
D) Não há diferença, são sinônimos  

**Resposta:** C  
**Justificativa:** Product Risk = falhas no produto (bugs, performance). Project Risk = problemas no projeto (atrasos, falta de recursos).

---

## Questão 3 (K3)
Um sistema bancário tem as seguintes funcionalidades:
- Login (Probabilidade: 2, Impacto: 5)
- Transferência (Probabilidade: 3, Impacto: 5)
- Consulta saldo (Probabilidade: 1, Impacto: 2)
- Relatórios (Probabilidade: 4, Impacto: 3)

Qual a ordem CORRETA de priorização de testes?

A) Transferência > Login > Relatórios > Consulta saldo  
B) Login > Transferência > Consulta saldo > Relatórios  
C) Transferência > Relatórios > Login > Consulta saldo  
D) Relatórios > Transferência > Login > Consulta saldo  

**Resposta:** A  
**Justificativa:** Cálculo de risco (P×I):
- Transferência: 3×5 = 15 (ALTO)
- Login: 2×5 = 10 (MÉDIO)
- Relatórios: 4×3 = 12 (MÉDIO-ALTO)
- Consulta: 1×2 = 2 (BAIXO)
Ordem: 15 > 12 > 10 > 2

---

## Questão 4 (K4)
Você é Test Analyst em um projeto e-commerce. Durante a análise de risco, identifica que o módulo de pagamento tem alta complexidade técnica (nova API de terceiros) e processa transações financeiras críticas. Como você classificaria este risco?

A) Baixa probabilidade, baixo impacto  
B) Alta probabilidade, baixo impacto  
C) Baixa probabilidade, alto impacto  
D) Alta probabilidade, alto impacto  

**Resposta:** D  
**Justificativa:** 
- **Alta probabilidade:** Nova tecnologia + complexidade técnica aumentam chance de falha
- **Alto impacto:** Transações financeiras são críticas para o negócio

---

## Questão 5 (K2)
Qual das seguintes NÃO é uma atividade típica do Test Analyst em Risk-Based Testing?

A) Identificar riscos de produto  
B) Avaliar probabilidade e impacto de riscos  
C) Definir o orçamento do projeto  
D) Priorizar casos de teste baseados em risco  

**Resposta:** C  
**Justificativa:** Definir orçamento é responsabilidade do gerente de projeto, não do Test Analyst.

---

## Questão 6 (K3)
Durante um sprint, novos requisitos são adicionados ao backlog. O que você deve fazer em relação à análise de risco?

A) Manter a análise de risco original sem alterações  
B) Re-avaliar riscos considerando as mudanças  
C) Ignorar os novos requisitos até o próximo sprint  
D) Aumentar automaticamente o risco de todos os itens  

**Resposta:** B  
**Justificativa:** Mudanças nos requisitos exigem re-avaliação de riscos, pois podem introduzir novos riscos ou alterar os existentes.

---

## Questão 7 (K2)
O que é uma Risk Matrix?

A) Documento que lista todos os bugs encontrados  
B) Ferramenta visual que cruza probabilidade e impacto  
C) Planilha de casos de teste priorizados  
D) Relatório de cobertura de código  

**Resposta:** B  
**Justificativa:** Risk Matrix é uma tabela (geralmente 5×5) que visualiza riscos cruzando probabilidade (eixo Y) com impacto (eixo X).

---

## Questão 8 (K4)
Você tem 40 horas para testar um sistema com 5 módulos. A análise de risco resultou em:
- Módulo A: Risco 20 (Alto)
- Módulo B: Risco 15 (Alto)
- Módulo C: Risco 8 (Médio)
- Módulo D: Risco 5 (Baixo)
- Módulo E: Risco 3 (Baixo)

Como você distribuiria o tempo de teste?

A) 8h para cada módulo (distribuição igual)  
B) A:15h, B:12h, C:8h, D:3h, E:2h  
C) A:20h, B:10h, C:5h, D:3h, E:2h  
D) Testar apenas A e B (alto risco)  

**Resposta:** B  
**Justificativa:** Distribuição proporcional ao risco, mas sem ignorar completamente baixo risco. Opção B aloca mais tempo para alto risco mantendo cobertura mínima nos demais.

---

## Questão 9 (K2)
Qual fator NÃO aumenta a probabilidade de risco?

A) Equipe inexperiente na tecnologia  
B) Código legado sem documentação  
C) Funcionalidade crítica de negócio  
D) Mudanças frequentes nos requisitos  

**Resposta:** C  
**Justificativa:** "Funcionalidade crítica de negócio" aumenta o IMPACTO, não a probabilidade. Os demais aumentam a chance de falha (probabilidade).

---

## Questão 10 (K3)
Um risco identificado tem probabilidade 5 (muito alta) e impacto 5 (muito alto). Qual ação é MAIS apropriada?

A) Aceitar o risco e documentar  
B) Transferir o risco para terceiros  
C) Mitigar com testes rigorosos e revisões  
D) Ignorar pois é muito complexo de resolver  

**Resposta:** C  
**Justificativa:** Risco 25 (5×5) é CRÍTICO e exige mitigação ativa através de testes extensivos, revisões de código, pair programming, etc. Não pode ser aceito (A) ou ignorado (D).

---

## Gabarito Rápido
1-B | 2-C | 3-A | 4-D | 5-C | 6-B | 7-B | 8-B | 9-C | 10-C

---

## Análise de Desempenho

**Sua pontuação:** ___/10

- **9-10 acertos (90-100%):** Excelente! Domínio completo do capítulo
- **7-8 acertos (70-80%):** Bom! Revisar questões erradas
- **5-6 acertos (50-60%):** Regular. Estudar novamente o capítulo
- **0-4 acertos (<50%):** Insuficiente. Leitura completa necessária

---

## Próximos Passos
- [ ] Revisar questões erradas
- [ ] Criar flashcards dos conceitos que errou
- [ ] Refazer o simulado em 3 dias
- [ ] Avançar para Capítulo 2 (Test Techniques) quando atingir 80%+
