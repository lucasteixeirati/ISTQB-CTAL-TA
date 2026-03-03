# ISTQB CTAL-TA - Sistema de Estudos

Uma aplicação web completa em Flask para preparação e domínio da certificação **ISTQB CTAL-TA** com ferramentas de aprendizado interativo, geração inteligente de questões com IA e acompanhamento de progresso em tempo real.

## Funcionalidades Principais

### 📝 Simulados Interativos
- **Exames por capítulo**: Pratique tópicos específicos da certificação com conjuntos curados de questões
- **Testes completos**: Simulações de exame completo simulando as condições reais da certificação
- **Feedback instantâneo**: Análise detalhada das respostas com explicações e alternativas corretas
- **Análise de desempenho**: Acompanhe sua evolução ao longo do tempo com métricas detalhadas

### 🎯 Flashcards Digitais
- **Decks organizados**: Coleções de flashcards pré-construídos organizados por capítulos da certificação
- **Aprendizado ativo**: Sistema de repetição espaçada para retenção ótima de conhecimento
- **Revisão diária**: Interface dedicada para prática diária e sessões rápidas de revisão
- **Filtros personalizáveis**: Estude por tópico, dificuldade ou seu próprio caminho de aprendizado

### 📊 Dashboard Personalizado
- **Acompanhamento de progresso**: Monitoramento em tempo real de sua prontidão para a certificação
- **Métricas de desempenho**: Visualize resultados de simulados, pontuação média e taxa de sucesso
- **Estatísticas de estudo**: Tempo investido, questões respondidas, áreas fracas identificadas
- **Recomendações personalizadas**: Sugestões baseadas no seu histórico de desempenho

### 🤖 Geração de Questões com IA
- **Criação inteligente**: Gere questões personalizadas a partir de materiais de estudo em PDF/TXT
- **Múltiplos provedores de LLM**: Escolha entre Ollama (local), HuggingFace ou OpenAI
- **Processamento em lote**: Sistema assíncrono de jobs para gerar grandes volumes sem bloquear
- **Revisão de qualidade**: Edite e valide questões geradas pela IA antes de salvar no banco
- **Tópicos flexíveis**: Atribua questões geradas a qualquer capítulo da certificação dinamicamente

### 📚 Biblioteca Unificada de Materiais
- **Biblioteca unificada**: Acesse materiais anexados e materiais carregados em um único lugar
- **Múltiplos formatos**: Upload de qualquer tipo de arquivo para organização da biblioteca
- **Gerenciamento eficiente**: Carregue, organize e gerencie seus materiais de estudo facilmente
- **Visualização rápida**: Acesso direto para visualizar ou abrir materiais do aplicativo

### 🔄 Pipeline Assíncrono de Geração
- **Processamento em background**: Crie questões sem aguardar respostas da IA
- **Rastreamento de jobs**: Monitore status em tempo real (pendente → processando → concluído)
- **Tratamento de erros**: Lógica automática de retry com mensagens de erro detalhadas
- **Arquitetura escalável**: Suporte para múltiplos jobs de geração simultâneos

---

## Instalação Rápida

### Requisitos
- Python 3.8+
- pip (gestor de pacotes Python)

### Passo a Passo

1. Clone o repositório:
   ```bash
   git clone https://github.com/lucasteixeirati/ISTQB-CTAL-TA.git
   cd ISTQB-CTAL-TA
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. (Opcional) Crie um arquivo `.env` a partir de `.env.example` para configuração personalizada.

4. Inicie a aplicação:
   ```bash
   python app.py
   ```

5. Acesse a interface web:
   ```
   http://localhost:5000
   ```

---

## Estrutura do Projeto

```
├── app.py                          # Inicialização Flask & rotas principais
├── app/
│   ├── routes/                     # Blueprints de rotas da API
│   │   ├── geracoes.py            # Endpoints de jobs assíncronos
│   │   └── __init__.py            # Registro de blueprints
│   └── services/                   # Lógica de negócio & integrações
│       ├── simulado_service.py    # Integração LLM & geração de questões
│       ├── geracoes_service.py    # Persistência e gerenciamento de jobs
│       └── flashcards_service.py  # Operações de flashcards (placeholder)
├── templates/                      # Templates Jinja2 das páginas
├── static/
│   ├── css/                        # Folhas de estilo
│   └── js/                         # Scripts frontend por funcionalidade
├── flashcards/                     # Decks de flashcards pré-construídos
├── simulados/                      # Conjuntos de questões de prova
├── resumos/                        # Resumos de estudo
├── uploads/                        # Materiais carregados pelo usuário
├── arquivos_anexados.json          # Metadados de arquivos
├── questoes_banco.json             # Banco consolidado: questões + jobs assíncronos + metadados
├── questoes_rotacao.json           # Rastreamento de uso para rotating inteligente
├── progresso_simulados.json        # Rastreamento de progresso dos simulados
└── requirements.txt                # Dependências Python
```

---

## Visão Geral das Funcionalidades por Página

### 1. Simulados (`/simulado`)
- **Modo exame**: Simulações de corpo inteiro com 40+ questões do syllabus completo
- **Focado por capítulo**: Pratique tópicos específicos isoladamente
- **Feedback em tempo real**: Resultados imediatos com respostas corretas e justificativas
- **Rastreamento de tempo**: Limites de tempo opcionais para simular condições de exame

### 2. Arquivos & Geração com IA (`/arquivos`)
- **Interface de upload**: Carregamento via arrastar-soltar para qualquer tipo de arquivo
- **Biblioteca de materiais**: Visualização unificada de todos os materiais de estudo
- **Geração com IA**: Selecione arquivos PDF/TXT e gere questões personalizadas:
  - Número de questões a gerar
  - Seleção de provedor LLM (Ollama local / HuggingFace / OpenAI)
  - Atribuição de capítulo da certificação
- **Revisão de questões**: Edite e valide antes de salvar no banco

### 3. Gerações Assíncronas (`/geracoes`)
- **Dashboard de jobs**: Monitore o status de todos os jobs de geração
- **Atualizações em tempo real**: Acompanhe o progresso das tarefas de IA de longa duração
- **Processamento em lote**: Crie múltiplos jobs e gerencie simultaneamente
- **Salvar no banco**: Finalize questões revisadas e adicione à sua coleção

### 4. Flashcards (`/flashcards`)
- **Explorador de decks**: Navegue por coleções pré-construídas de flashcards
- **Modo de estudo**: Interface interativa de inversão de cartões com revelação instantânea
- **Opções de filtro**: Estude por tópico, dificuldade ou seleções personalizadas
- **Rastreamento de progresso**: Veja quais cartões você dominou e quais precisam de prática

### 5. Dashboard (`/dashboard`)
- **Estatísticas**: Taxa geral de acurácia, total de questões, tempo investido
- **Gráfico de progresso**: Representação visual das tendências de desempenho ao longo do tempo
- **Resultados recentes**: Visualize detalhes de seus últimas 10 tentativas
- **Áreas fracas**: Identifique tópicos que precisam de mais estudo

---

## Endpoints da API (Resumo)

### Simulados
- `POST /api/iniciar-simulado` — Inicia uma nova sessão de simulado
- `POST /api/finalizar-simulado` — Envia respostas e obtém resultados

### Gerenciamento de Arquivos
- `GET /api/arquivos` — Lista materiais de estudo carregados
- `POST /api/upload` — Carrega um novo arquivo (qualquer tipo)
- `DELETE /api/deletar-arquivo/<id>` — Remove um arquivo carregado
- `POST /api/gerar-questoes/<id>` — Gera questões de um arquivo PDF/TXT (síncrono)
- `POST /api/arquivos/salvar-questoes/<id>` — Salva questões revisadas no banco

### Jobs de Geração Assíncrona
- `POST /api/geracoes` — Cria um novo job assíncrono
- `GET /api/geracoes` — Lista todos os jobs com resumo
- `GET /api/geracoes/<job_id>` — Obtém detalhes de um job específico
- `POST /api/geracoes/<job_id>/salvar` — Salva questões do job no banco

### Flashcards
- `GET /api/flashcards` — Recupera flashcards com filtros opcionais
- `GET /api/flashcards/decks` — Lista todos os decks disponíveis

### Estatísticas & Configuração
- `GET /api/estatisticas` — Obtém dados do dashboard e progresso
- `GET /api/llm-opcoes` — Lista opções de provedores LLM
- `GET /api/materiais` — Lista materiais de estudo da pasta uploads

---

## Configuração

Configure a aplicação via variáveis de ambiente em `.env`:

```bash
# Configuração Flask
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000

# Armazenamento de Arquivos
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
QUESTOES_BANCO_FILE=questoes_banco.json

# Geração de Questões
ARQUIVOS_FILE=arquivos_anexados.json
ENABLE_GERACOES_WORKER=1

# Configuração de LLM
OLLAMA_MODEL=phi3
HUGGINGFACE_API_KEY=sua-chave-hf-aqui
OPENAI_API_KEY=sua-chave-openai-aqui

# Logging
LOG_LEVEL=INFO
```

---

## Executando com Worker Assíncrono

Para habilitar processamento de geração em background:

```powershell
$env:ENABLE_GERACOES_WORKER="1"; python app.py
```

O worker processará automaticamente jobs pendentes em background.

---

## Capturas de Tela

**[Ver capturas de tela e demonstrações do sistema](https://lucasteixeirati.github.io/ISTQB-CTAL-TA/screenshots.html)**

---

## Documentação Técnica

- [**Documento de Arquitetura**](ARQUITETURA.md) — Design do sistema, fluxos de dados e componentes
- [**Guia de Uso Rápido**](GUIA_USO_RAPIDO.md) — Implantação rápida e solução de problemas

**English Documentation:**
- [**Architecture Document**](ARCHITECTURE.md)
- [**Quick Start Guide**](QUICK_START_GUIDE.md)
- [**README (English)**](README_EN.md)

---

## Licença

Licença MIT — Veja [LICENSE](LICENSE) para detalhes.

## Autor

Lucas Teixeira 
Quality Assurance Specialist

---

