# QUICK START GUIDE - ISTQB CTAL-TA

---

## Quick Tips

- Always use chapter-specific question sets for up-to-date content
- **Flashcards**: Review daily for optimal knowledge retention and spaced repetition
- **Dashboard**: Monitor your progress weekly to track improvement over time
- **Exam simulations**: Practice under real exam conditions to build test confidence and time management

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module import errors | Verify you're in the correct project directory and all files exist |
| Progress file not found | Don't worry — it will be created automatically on first use |
| Simulations not generating questions | Test the question bank with: `python banco_questoes_completo.py` |
| Questions not appearing in review modal | Ensure browser console has no errors (F12) and flashcards are loaded |
| Generation job stuck | Check worker status: ensure `ENABLE_GERACOES_WORKER=1` is set |

---

## Quick Commands

### Start the web application
```bash
# Standard mode
python app.py

# With async worker enabled
$env:ENABLE_GERACOES_WORKER="1"; python app.py
```

### Question bank operations
```bash
# Load and verify question database
python banco_questoes_completo.py
```

### Generate simulations
```bash
# Create new exam question sets
python gerador_simulados_v3.py
```

### Monitor study progress
```bash
# View detailed progress tracking
python tracking_progresso_v2.py
```

---

## Feature Quick Start

### 📝 First Simulation
1. Open the app at `http://localhost:5000`
2. Click **Simulados** (Simulations)
3. Select **Simulado Completo** (Full Test) or a specific chapter
4. Answer all questions within the time limit
5. Review your results with explanations

### 🤖 Generate Questions from Your Material
1. Click **Arquivos & LLM** (Files & AI)
2. Upload a PDF or TXT file containing your study material
3. Click **Examinar e Gerar Questões** (Examine and Generate Questions)
4. Configure:
   - Number of questions (1-20)
   - LLM provider (Auto, Ollama, HuggingFace, OpenAI)
   - Target chapter for classification
5. Review generated questions in the modal
6. Click **Salvar Questões** (Save Questions) to add them to your bank

### ⚙️ Monitor Async Generation
1. Click **Gerações** (Generations)
2. See all active and completed generation jobs
3. Click on a job to see its status and generated questions
4. Save completed jobs to your question database

### 🎯 Study with Flashcards
1. Click **Flashcards**
2. Choose a deck by topic
3. Flip cards to reveal answers
4. Review challenging topics repeatedly

### 📊 Track Your Progress
1. Click **Dashboard**
2. View your performance metrics:
   - Average accuracy rate
   - Total questions answered
   - Study time invested
   - Performance trends
3. Identify weak areas for focused review

---

## LLM Provider Configuration

### Option 1: Ollama (Local - Recommended for privacy)
```bash
# Install Ollama: https://ollama.ai

# Start Ollama server
ollama serve

# In another terminal, pull a model
ollama pull phi3

# Set environment
$env:OLLAMA_MODEL="phi3"
$env:OLLAMA_BASE_URL="http://localhost:11434"

# Start app
python app.py
```

### Option 2: HuggingFace (Free cloud API)
```bash
# Get your API key at: https://huggingface.co/settings/tokens

# Set environment
$env:HUGGINGFACE_API_KEY="your-api-key-here"

# Start app
python app.py
```

### Option 3: OpenAI (Premium, high quality)
```bash
# Get your API key at: https://platform.openai.com/api-keys

# Set environment
$env:OPENAI_API_KEY="your-api-key-here"
$env:OPENAI_MODEL="gpt-4.1-mini"

# Start app
python app.py
```

---

## Study Strategy Tips

### For Exam Preparation
1. **Week 1-2**: Take full-length simulations weekly to identify weak areas
2. **Week 3-4**: Use flashcards daily for 10-15 minutes each morning
3. **Week 5-6**: Generate custom questions from your study notes
4. **Final week**: Do daily simulations with strict time limits

### For Topic Deep-Dive
1. Use chapter-specific simulations to master individual topics
2. Generate questions from related materials using AI
3. Review with flashcards created by experts
4. Track your accuracy per topic on the dashboard

### For Time-Constrained Study
- Use flashcards (5-10 min/day)
- Take mini-tests (Chapter simulations - 15-20 min)
- Skip full exams initially; focus on problem areas

---

## Backing Up Your Progress

### Manual Backup
Copy these files to a safe location:
- `banco_questoes.json` — Your custom question bank
- `progresso_simulados.json` — Your exam records
- `geracoes_questoes.json` — Your generation job history

### Restore from Backup
Replace the files in the project directory with your backup copies.

---

## Performance Tips

**For better AI generation results:**
- Use clear, well-formatted study materials
- Extract key concepts to your text files before uploading
- Generate 5-10 questions at a time for better quality
- Review and refine generated questions before saving

**For faster question generation:**
- Use Ollama locally to avoid API latency
- Generate during off-peak hours if using cloud providers
- Ensure sufficient server resources (CPU for LLMs)

---

## Common Workflows Video Guide

**Coming soon:** Step-by-step video tutorials for:
- First-time setup
- Uploading and generating questions
- Running simulations in exam mode
- Reviewing results and weak areas

---

**For more detailed technical information, see [ARCHITECTURE.md](ARCHITECTURE.md)**
