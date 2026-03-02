# ISTQB CTAL-TA - Sistema de Estudos

Aplicação web em Flask para preparação da certificação **ISTQB CTAL-TA**, com:
- simulados por capítulo e completo
- flashcards por deck
- dashboard de progresso
- upload de PDF/TXT
- geração de questões com IA
- pipeline de **gerações assíncronas** (jobs + worker)

> Este repositório **não inclui materiais anexados** da pasta `uploads/`.

## Instalação rápida

1. Clone o projeto e entre na pasta.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. (Opcional) Crie o arquivo `.env` a partir de `.env.example`.
4. Execute:
   ```bash
   python app.py
   ```
5. Acesse: http://localhost:5000

## Estrutura do projeto

- **Frontend:** `templates/` e `static/`
- **Backend:** `app.py`, `app/routes/` e `app/services/`
- **Flashcards:** `flashcards/`
- **Simulados:** `simulados/`
- **Resumos:** `resumos/`

## Principais funcionalidades

- Simulados interativos por capítulo ou completo
- Flashcards digitais para revisão rápida
- Dashboard com estatísticas de desempenho
- Upload de PDF/TXT e geração de questões com IA
- Revisão/edição e salvamento de questões no banco

## Capturas de tela

**[Ver fotos do sistema em funcionamento](https://lucasteixeirati.github.io/ISTQB-CTAL-TA/)**

## Endpoints (resumo)

- **Upload/arquivos**
  - `GET /arquivos`
  - `GET /api/arquivos`
  - `POST /api/upload`
  - `DELETE /api/deletar-arquivo/<arquivo_id>`

- **Geração síncrona por arquivo**
  - `POST /api/gerar-questoes/<arquivo_id>`

- **Salvar questões no banco**
  - `POST /api/arquivos/salvar-questoes/<arquivo_id>`
  - Aceita `alternativas: [..4]` ou `opcoes: {A,B,C,D}`

- **Gerações assíncronas (jobs)**
  - `POST /api/geracoes`
  - `GET /api/geracoes`
  - `GET /api/geracoes/<job_id>`
  - `POST /api/geracoes/<job_id>/salvar`

- **Simulado**
  - `POST /api/iniciar-simulado`
  - `POST /api/finalizar-simulado`

- **Flashcards**
  - `GET /flashcards`
  - `GET /api/flashcards`
  - `GET /api/flashcards/decks`

- **Dashboard**
  - `GET /dashboard`
  - `GET /api/estatisticas`

## Worker de gerações (jobs)

Para habilitar o worker assíncrono, defina a variável antes de iniciar o Flask:

```powershell
$env:ENABLE_GERACOES_WORKER="1"; python app.py
```

> Em `FLASK_DEBUG=1`, o worker evita iniciar no processo duplicado do reloader.

## Licença

MIT. Veja `LICENSE`.
