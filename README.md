# ISTQB CTAL-TA - Sistema de Estudos

Sistema para preparação e revisão para a certificação **ISTQB CTAL-TA**, com interface web (Flask) incluindo:
- simulados
- flashcards
- dashboard de progresso
- upload de PDF/TXT e geração de questões (IA)
- pipeline de **gerações assíncronas** (jobs) com worker

> Este repositório **não inclui materiais anexados** (pasta `uploads/`). Ao baixar, o usuário pode fazer upload dos próprios PDFs/TXTs pela interface.

## Estrutura do Projeto
- **Flashcards:** pasta `flashcards/` (decks em Markdown)
- **Simulados:** pasta `simulados/` (por capítulo)
- **Resumos:** pasta `resumos/`
- **Frontend:** `templates/` e `static/`
- **Backend:** `app.py` (Flask) + `app/routes/*` + `app/services/*`

## Instalação

1. Clone/baixe o projeto e acesse a pasta:
   ```bash
   cd c:\Projetos\ISTQB-CTAL-TA
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração (.env)

- Use o arquivo `.env.example` como base.
- Crie um `.env` local (não versionado) e ajuste as variáveis conforme necessário.

Exemplo (PowerShell):
```powershell
copy .env.example .env
```

## Execução (Web)

Inicie a aplicação:
```bash
python app.py
```
Acesse:
- http://localhost:5000

> Observação: o worker de gerações assíncronas **não inicia por padrão**. Veja a seção **Worker de gerações (jobs)**.

## Principais Funcionalidades
- Simulados interativos por capítulo ou completos
- Flashcards digitais para revisão rápida (com filtro por capítulo)
- Dashboard de progresso e estatísticas
- Upload de PDF/TXT e geração de questões
- Revisão/edição e salvamento no `banco_questoes.json`

## 📸 Capturas de Tela

**[Ver fotos do sistema em funcionamento →](screenshots.html)**

## Endpoints (resumo)

- Upload/arquivos:
  - `GET /arquivos` (página)
  - `GET /api/arquivos`
  - `POST /api/upload`
  - `DELETE /api/deletar-arquivo/<arquivo_id>`

- Geração (síncrona a partir de arquivo):
  - `POST /api/gerar-questoes/<arquivo_id>`

- Salvar questões (valida e persiste em `banco_questoes.json`):
  - `POST /api/arquivos/salvar-questoes/<arquivo_id>`
  - A API aceita tanto `alternativas: [..4]` quanto `opcoes: {A,B,C,D}` e normaliza ao salvar.

- Gerações (assíncrono via jobs):
  - `POST /api/geracoes` (cria job)
  - `GET /api/geracoes` (lista)
  - `GET /api/geracoes/<job_id>` (detalhes)
  - `POST /api/geracoes/<job_id>/salvar` (salvar questões do job no banco)

- Simulado:
  - `POST /api/iniciar-simulado`
  - `POST /api/finalizar-simulado`

- Flashcards:
  - `GET /flashcards` (página)
  - `GET /api/flashcards`
  - `GET /api/flashcards/decks`

- Dashboard:
  - `GET /dashboard` (página)
  - `GET /api/estatisticas`

## Worker de gerações (jobs)

A aplicação suporta geração assíncrona baseada em jobs persistidos em `geracoes_questoes.json`.

### Como habilitar
Defina a variável abaixo **antes de iniciar o Flask**:
- `ENABLE_GERACOES_WORKER=1`

Exemplo (PowerShell):
```powershell
$env:ENABLE_GERACOES_WORKER="1"; python app.py
```

> Em `FLASK_DEBUG=1` o worker evita iniciar no processo duplicado do reloader.


## Licença

MIT. Veja `LICENSE`.
