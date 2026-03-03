# ISTQB CTAL-TA - Study System

A comprehensive Flask web application for preparing and mastering the **ISTQB CTAL-TA** certification with interactive learning tools, intelligent question generation powered by AI, and real-time progress tracking.

## Core Features

### 📝 Interactive Simulations
- **Chapter-based exams**: Practice specific certification topics with curated question sets
- **Full practice tests**: Complete mock exams simulating real certification conditions
- **Instant feedback**: Detailed analysis of your answers with explanations and correct alternatives
- **Performance analytics**: Track your improvement over time with detailed metrics and progress charts

### 🎯 Digital Flashcards
- **Organized decks**: Pre-built flashcard collections organized by certification chapters
- **Active recall**: Space-repetition learning system for optimal knowledge retention
- **Daily review**: Dedicated interface for daily practice and quick revision sessions
- **Customizable filters**: Study by topic, difficulty, or personal learning path

### 📊 Personalized Dashboard
- **Progress tracking**: Real-time monitoring of your certification readiness
- **Performance metrics**: View your simulations results, average scores, and success rate
- **Study statistics**: Time spent studying, questions answered, and weak areas identified
- **Study recommendations**: Personalized suggestions based on your performance patterns

### 🤖 AI-Powered Question Generation
- **Intelligent creation**: Generate custom questions from your own study materials (PDF/TXT)
- **Multiple LLM providers**: Choose from Ollama (local), HuggingFace, or OpenAI models
- **Batch processing**: Asynchronous job system for generating large question sets without blocking
- **Quality review**: Edit and validate AI-generated questions before saving to your question bank
- **Flexible topics**: Assign generated questions to any certification chapter dynamically

### 📚 Study Materials Library
- **Unified library**: Access both annexed materials and uploaded study resources in one place
- **Multiple formats**: Support for PDF documents and text files
- **Efficient management**: Upload, organize, and manage your study materials easily
- **Content preview**: Quick access to view or open materials directly from the app

### 🔄 Asynchronous Generation Pipeline
- **Background processing**: Create questions without waiting for AI responses
- **Job tracking**: Monitor generation status in real-time (pending → processing → complete)
- **Error handling**: Automatic retry logic and detailed error messages
- **Scalable architecture**: Support for multiple concurrent generation jobs

---

## Quick Start

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lucasteixeirati/ISTQB-CTAL-TA.git
   cd ISTQB-CTAL-TA
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a `.env` file from `.env.example` for custom configuration.

4. Start the application:
   ```bash
   python app.py
   ```

5. Access the web interface:
   ```
   http://localhost:5000
   ```

---

## Project Structure

```
├── app.py                          # Flask application initialization & main routes
├── app/
│   ├── routes/                     # API route blueprints
│   │   ├── geracoes.py            # Async generation job endpoints
│   │   └── __init__.py            # Blueprint registration
│   └── services/                   # Business logic & integrations
│       ├── simulado_service.py    # LLM integration & question generation
│       ├── geracoes_service.py    # Job persistence & management
│       └── flashcards_service.py  # Flashcard operations (placeholder)
├── templates/                      # Jinja2 HTML templates for pages
│   ├── index.html
│   ├── simulado.html
│   ├── arquivos.html
│   ├── geracoes.html
│   ├── flashcards.html
│   ├── dashboard.html
│   └── estudos.html
├── static/
│   ├── css/                        # Stylesheets
│   │   └── style.css
│   └── js/                         # Frontend scripts by feature
│       ├── simulado.js
│       ├── arquivos.js
│       ├── geracoes.js
│       ├── flashcards.js
│       └── dashboard.js
├── flashcards/                     # Pre-built flashcard decks (Markdown format)
├── simulados/                      # Practice exam question sets by chapter
├── resumos/                        # Study summaries & reference materials
├── uploads/                        # User-uploaded study materials (PDFs/TXTs)
├── screenshots.html                # Gallery of system screenshots
├── prints/                         # Screenshots & system screenshots
├── banco_questoes.json             # Generated & saved questions database
├── arquivos_anexados.json          # Metadata of uploaded files
├── geracoes_questoes.json          # Async generation job state
├── progresso_simulados.json        # Simulation progress tracking
└── requirements.txt                # Python dependencies
```

---

## Features Overview by Page

### 1. Simulations (`/simulado`)
- **Exam mode**: Full-length simulations with 40+ questions from the entire CTAL-TA syllabus
- **Chapter-focused**: Practice specific certification topics in isolation
- **Real-time feedback**: Immediate results with correct answers and justifications
- **Time tracking**: Optional time limits to simulate exam conditions

### 2. Files & AI Generation (`/arquivos`)
- **Upload interface**: Drag-and-drop upload for PDF and TXT files
- **Material library**: Unified view of all study materials and uploaded documents
- **AI generation**: Select files and generate custom questions with configurable parameters:
  - Number of questions to generate
  - LLM provider selection (Ollama local / HuggingFace / OpenAI)
  - Target certification chapter assignment
- **Question review**: Edit and validate before saving to your question bank

### 3. Async Generations (`/geracoes`)
- **Job dashboard**: Monitor status of all question generation jobs
- **Real-time updates**: Track progress of long-running AI generation tasks
- **Batch processing**: Create multiple generation jobs and manage them concurrently
- **Save to bank**: Finalize reviewed questions and add them to your question collection

### 4. Flashcards (`/flashcards`)
- **Deck browser**: Browse pre-built flashcard collections by chapter
- **Study mode**: Interactive card-flipping interface with instant reveal
- **Filter options**: Study by topic, difficulty, or custom selections
- **Progress tracking**: See which cards you've mastered and which need more practice

### 5. Dashboard (`/dashboard`)
- **Statistics**: Overall accuracy rate, total questions answered, time invested
- **Progress chart**: Visual representation of performance trends over time
- **Recent results**: View details of your last 10 simulation attempts
- **Weak areas**: Identify topics that need more study based on performance data

---

## API Endpoints Summary

### Simulations
- `POST /api/iniciar-simulado` — Start a new simulation session
- `POST /api/finalizar-simulado` — Submit simulation answers and get results

### File Management
- `GET /api/arquivos` — List uploaded study materials
- `POST /api/upload` — Upload a new PDF or TXT file
- `DELETE /api/deletar-arquivo/<id>` — Remove an uploaded file
- `POST /api/gerar-questoes/<id>` — Generate questions from a file (synchronous)
- `POST /api/arquivos/salvar-questoes/<id>` — Save reviewed questions to the database

### Async Generation Jobs
- `POST /api/geracoes` — Create a new async generation job
- `GET /api/geracoes` — List all generation jobs with summary
- `GET /api/geracoes/<job_id>` — Get details of a specific job
- `POST /api/geracoes/<job_id>/salvar` — Save job's generated questions to database

### Flashcards
- `GET /api/flashcards` — Retrieve flashcards with optional filtering
- `GET /api/flashcards/decks` — List all available flashcard decks

### Statistics & Config
- `GET /api/estatisticas` — Get dashboard statistics and progress data
- `GET /api/llm-opcoes` — List available LLM provider options
- `GET /api/materiais` — List study materials from uploads folder

---

## Configuration

Configure the application via environment variables in `.env`:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000

# File Storage
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# Question Generation
GERACOES_FILE=geracoes_questoes.json
ARQUIVOS_FILE=arquivos_anexados.json
ENABLE_GERACOES_WORKER=1  # Set to enable async worker

# LLM Configuration
OLLAMA_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
HUGGINGFACE_API_KEY=your-hf-api-key
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini  # or your chosen model

# Logging
LOG_LEVEL=INFO
```

---

## Running with Async Worker

To enable background question generation processing:

```powershell
$env:ENABLE_GERACOES_WORKER="1"; python app.py
```

The worker will automatically process pending generation jobs in the background without blocking the web interface.

---

## Screenshots

**[View system screenshots & feature demonstrations](https://lucasteixeirati.github.io/ISTQB-CTAL-TA/screenshots.html)**

Screenshots showcase:
- Dashboard with real-time statistics
- Full simulation workflow
- Flashcard study interface
- File upload and question generation UI
- Async job monitoring
- Question review and editing
- Study material library

---

## Technical Documentation

- [**Architecture Document**](ARQUITETURA.md) — Detailed system design, data flows, and component interactions
- [**Quick Start Guide**](GUIA_USO_RAPIDO.md) — Rapid deployment guide and troubleshooting
- [**API Reference**](INTERFACE_WEB.md) — Complete endpoint documentation

---

## License

MIT License — See [LICENSE](LICENSE) for details.

---

## Contributing

Contributions are welcome! Feel free to:
- Report bugs and suggest improvements
- Submit pull requests with enhancements
- Help translate documentation to other languages
- Expand the question database and study materials

---

**Built for ISTQB CTAL-TA Certification Excellence** 🚀
