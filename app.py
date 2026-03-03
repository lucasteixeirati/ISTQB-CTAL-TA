"""
ISTQB CTAL-TA - Web Interface
Flask app exposing upload, question generation, flashcards and simulation endpoints.
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
import random
from werkzeug.utils import secure_filename
import PyPDF2
import re
import glob
import logging
import threading
import time

from app.services.simulado_service import salvar_no_tracking
from app.services.geracoes_service import GeracoesService

from app.services.simulado_service import gerar_perguntas_llm_escolha

# Registrar blueprints (rotas modularizadas em app/routes)
from app.routes import register_routes

# Logging (controlado por LOG_LEVEL=DEBUG/INFO/WARNING/ERROR)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("istqb-web")

app = Flask(__name__)

# Registrar rotas via blueprints (gera7oes, etc.)
register_routes(app)

# Config via env (com defaults compatíveis)
# - SECRET_KEY: defina em produção (não logar o valor)
_secret_from_env = os.getenv('SECRET_KEY')
app.secret_key = _secret_from_env or 'istqb-ctal-ta-secret-key-2025'
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', str(16 * 1024 * 1024)))
app.config['QUESTOES_BANCO_FILE'] = os.getenv('QUESTOES_BANCO_FILE', 'questoes_banco.json')

# Hardening básico de cookies de sessão (ajuda em produção; em HTTP local o Secure pode ser desabilitado via env)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')  # Lax/Strict/None
app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', '0') == '1'

# Extensões suportadas para geração de questões com IA (não limita upload)
AI_GENERATION_EXTENSIONS = {'txt', 'pdf'}
ARQUIVOS_FILE = os.getenv('ARQUIVOS_FILE', 'arquivos_anexados.json')
app.config['ARQUIVOS_FILE'] = ARQUIVOS_FILE

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
logger.info(
    "App inicializado. UPLOAD_FOLDER=%s MAX_CONTENT_LENGTH=%s QUESTOES_BANCO_FILE=%s ARQUIVOS_FILE=%s",
    app.config['UPLOAD_FOLDER'],
    app.config['MAX_CONTENT_LENGTH'],
    app.config['QUESTOES_BANCO_FILE'],
    app.config['ARQUIVOS_FILE'],
)

# Falhar rápido em produção se SECRET_KEY não estiver configurada
_debug_enabled = os.getenv('FLASK_DEBUG', '0') == '1'

# Considera "produção" apenas quando explicitamente indicado.
# Assim, rodar `python app.py` localmente não falha por padrão.
_flask_env = (os.getenv('FLASK_ENV') or os.getenv('ENV') or '').strip().lower()
_is_production = _flask_env == 'production'

if _is_production and not _secret_from_env:
    raise RuntimeError('SECRET_KEY não configurada. Defina SECRET_KEY no ambiente antes de rodar em produção.')


def can_generate_questions(filename):
    """Verifica se o arquivo pode ser usado para gerar questões com IA."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in AI_GENERATION_EXTENSIONS


def carregar_questoes_banco():
    """Carrega o banco consolidado de questões de questoes_banco.json."""
    banco_file = app.config['QUESTOES_BANCO_FILE']
    if os.path.exists(banco_file):
        try:
            with open(banco_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.exception("Erro ao carregar questoes_banco: %s", banco_file)
            return {'questoes': {}, 'geracoes': {'jobs': []}, 'metadata': {}}
    return {'questoes': {}, 'geracoes': {'jobs': []}, 'metadata': {}}


def salvar_questoes_banco(banco_data):
    """Persiste o banco consolidado em questoes_banco.json."""
    banco_file = app.config['QUESTOES_BANCO_FILE']
    try:
        with open(banco_file, 'w', encoding='utf-8') as f:
            json.dump(banco_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.exception("Erro ao salvar questoes_banco: %s", banco_file)


def _upload_mime_ok(file_storage) -> bool:
    """Validação leve de MIME (não substitui antivírus/validação profunda).
    
    Aceita qualquer arquivo, mas registra no log para auditoria.
    """
    try:
        mimetype = (getattr(file_storage, 'mimetype', None) or '').lower()
        filename = (getattr(file_storage, 'filename', '') or '').lower()
        logger.debug(f"Upload: filename={filename} mimetype={mimetype}")
        # Aceita qualquer arquivo - validação específica será feita na geração
        return True
    except Exception:
        return False


def carregar_arquivos():
    """Load uploaded file metadata from JSON storage."""
    if os.path.exists(ARQUIVOS_FILE):
        with open(ARQUIVOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def salvar_arquivos(arquivos):
    """Persist uploaded file metadata to JSON storage."""
    with open(ARQUIVOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(arquivos, f, indent=2, ensure_ascii=False)


def extrair_texto_pdf(filepath):
    """Extract text content from a PDF file using PyPDF2."""
    texto = ""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            texto += page.extract_text()
    return texto


def extrair_texto_txt(filepath):
    """Read the full content of a UTF-8 text file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def carregar_flashcards():
    """Load flashcards from markdown decks under flashcards/deck_*.md."""
    flashcards = []
    arquivos = glob.glob('flashcards/deck_*.md')

    for arquivo in arquivos:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()

            deck_id = os.path.basename(arquivo).replace('.md', '')  # ex: deck_02_1_black_box_part1
            deck_nome = deck_id.replace('deck_', '').replace('_', ' ').title()

            # Suporta 2 formatos:
            # 1) "### Card N ..." (formato atual dos decks)
            # 2) "## Card N" (compatibilidade)
            pattern_h3 = r'###\s*Card\s*(\d+).*?\n\*\*Q:\*\*\s*(.+?)\n\*\*A:\*\*\s*(.+?)(?=\n\s*---\s*\n|\n\s*###\s*Card\s*\d+|\n\s*##\s*🎯|$)'
            pattern_h2 = r'##\s*Card\s*(\d+)\s*\*\*Q:\*\*\s*(.+?)\s*\*\*A:\*\*\s*(.+?)(?=\n---|##\s*Card|$)'

            cards = re.findall(pattern_h3, conteudo, re.DOTALL)
            if not cards:
                cards = re.findall(pattern_h2, conteudo, re.DOTALL)

            for card_num, pergunta, resposta in cards:
                flashcards.append({
                    'id': len(flashcards) + 1,
                    'deck': deck_nome,
                    'deck_id': deck_id,
                    'numero': int(card_num),
                    'pergunta': pergunta.strip(),
                    'resposta': resposta.strip()
                })
        except Exception:
            logger.exception("Erro ao carregar flashcards do arquivo %s", arquivo)

    logger.debug("Flashcards carregados: %s", len(flashcards))
    return flashcards

# Service para jobs de gerações
_geracoes_service = GeracoesService(geracoes_file=app.config['QUESTOES_BANCO_FILE'])


def _worker_geracao_loop(intervalo=3):
    logger.info("Worker de geração de questões iniciado (intervalo=%ss)", intervalo)
    while True:
        try:
            dados = _geracoes_service.carregar()
            pendentes = [j for j in dados['jobs'] if j.get('status') in ('pendente', 'processando')]
            if pendentes:
                job = pendentes[0]
                if job['status'] == 'pendente':
                    job = _geracoes_service.atualizar_job(job['id'], status='processando') or job
                try:
                    arquivos = carregar_arquivos()
                    arquivo = next((a for a in arquivos if a['id'] == job['arquivo_id']), None)
                    if not arquivo:
                        raise RuntimeError(f"Arquivo id={job['arquivo_id']} não encontrado para job {job['id']}")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], arquivo['nome_arquivo'])
                    texto = extrair_texto_pdf(filepath) if arquivo['tipo'] == 'pdf' else extrair_texto_txt(filepath)
                    questoes_ia = gerar_perguntas_llm_escolha(texto, job['num_questoes'], provider=job['provider'])

                    # mesma normalização usada na rota síncrona
                    questoes = []
                    for idx, q in enumerate(questoes_ia, 1):
                        alternativas = q.get('alternativas') or q.get('options') or []
                        opcoes_map = {}
                        letras = ['A', 'B', 'C', 'D']
                        for i, alt in enumerate(alternativas[:4]):
                            opcoes_map[letras[i]] = alt
                        for i in range(len(opcoes_map), 4):
                            opcoes_map[letras[i]] = f"(preencher manualmente {letras[i]})"
                        questoes.append({
                            'id': int(datetime.now().strftime('%H%M%S')) * 100 + idx,
                            'k_level': 'K2',
                            'pergunta': q.get('pergunta') or q.get('question') or '',
                            'opcoes': opcoes_map,
                            'resposta': (q.get('resposta') or q.get('answer') or 'A').strip(),
                            'justificativa': q.get('justificativa') or '',
                            'fonte': 'llm',
                        })

                    _geracoes_service.atualizar_job(job['id'], status='concluido', questoes=questoes, erro_msg=None)
                    logger.info("Job de geração concluído: id=%s questoes=%s", job['id'], len(questoes))

                except Exception as e:
                    logger.exception("Job de geração falhou: id=%s", job['id'])
                    _geracoes_service.atualizar_job(job['id'], status='erro', erro_msg=str(e))
            time.sleep(intervalo)
        except Exception:
            logger.exception("Erro no loop do worker de geração")
            time.sleep(intervalo)


def _start_geracoes_worker_if_enabled():
    """Inicia o worker de geração somente quando explicitamente habilitado via env.

    - ENABLE_GERACOES_WORKER=1: habilita
    - Em modo debug com reloader, evita iniciar no processo "clone".
    """
    enabled = os.getenv("ENABLE_GERACOES_WORKER", "0") == "1"
    if not enabled:
        logger.info("Worker de geracoes desabilitado (defina ENABLE_GERACOES_WORKER=1 para habilitar)")
        return

    # Quando FLASK_DEBUG=1, o reloader inicia 2 processos. O worker deve rodar apenas no principal.
    # WERKZEUG_RUN_MAIN só é "true" no processo principal do reloader.
    is_reloader_main = os.getenv("WERKZEUG_RUN_MAIN") == "true"
    debug_enabled = os.getenv("FLASK_DEBUG", "0") == "1"
    if debug_enabled and not is_reloader_main:
        logger.info("Worker de geracoes: aguardando processo principal do reloader (debug)")
        return

    global _thread_worker
    if globals().get("_thread_worker") is not None and getattr(_thread_worker, "is_alive", lambda: False)():
        logger.warning("Worker de geracoes ja estava em execucao; nao iniciando outro")
        return

    _thread_worker = threading.Thread(target=_worker_geracao_loop, kwargs={'intervalo': 3}, daemon=True)
    _thread_worker.start()
    logger.info("Worker de geracoes iniciado (ENABLE_GERACOES_WORKER=1)")


# iniciar worker em background (apenas se habilitado)
_thread_worker = None
_start_geracoes_worker_if_enabled()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulado')
def simulado():
    return render_template('simulado.html')

@app.route('/api/iniciar-simulado', methods=['POST'])
def iniciar_simulado():
    data = request.get_json(silent=True) or {}
    num_questoes = data.get('num_questoes', 40)
    
    banco = carregar_questoes_banco()
    todas_questoes = []
    for cap_questoes in banco.get('questoes', {}).values():
        if isinstance(cap_questoes, list):
            todas_questoes.extend(cap_questoes)
    
    questoes_selecionadas = random.sample(todas_questoes, min(num_questoes, len(todas_questoes)))
    
    questoes_sem_resposta = [{
        'id': q['id'],
        'k_level': q['k_level'],
        'pergunta': q['pergunta'],
        'opcoes': q['opcoes']
    } for q in questoes_selecionadas]
    
    session['simulado_atual'] = {
        'questoes_completas': questoes_selecionadas,
        'inicio': datetime.now().isoformat(),
        'num_questoes': num_questoes
    }
    
    return jsonify({
        'success': True,
        'questoes': questoes_sem_resposta,
        'tempo_total': num_questoes * 2
    })

@app.route('/api/finalizar-simulado', methods=['POST'])
def finalizar_simulado():
    data = request.get_json(silent=True) or {}
    respostas_usuario = data.get('respostas', {})
    
    simulado = session.get('simulado_atual')
    if not simulado:
        return jsonify({'success': False, 'error': 'Simulado nao encontrado'})
    
    questoes_completas = simulado['questoes_completas']
    acertos = 0
    resultados = []
    
    for q in questoes_completas:
        resposta_user = respostas_usuario.get(str(q['id']))
        correto = resposta_user == q['resposta']
        if correto:
            acertos += 1
        
        resultados.append({
            'id': q['id'],
            'pergunta': q['pergunta'],
            'opcoes': q['opcoes'],
            'resposta_correta': q['resposta'],
            'resposta_usuario': resposta_user,
            'correto': correto,
            'justificativa': q['justificativa']
        })
    
    total = len(questoes_completas)
    percentual = (acertos / total) * 100
    
    # Usar a funcao centralizada de tracking
    tempo_gasto = data.get('tempo_gasto', 0)
    salvar_no_tracking("web_completo", total, acertos, tempo_gasto)
    
    return jsonify({
        'success': True,
        'acertos': acertos,
        'total': total,
        'percentual': round(percentual, 1),
        'aprovado': percentual >= 65,
        'resultados': resultados
    })

@app.route('/arquivos')
def arquivos():
    return render_template('arquivos.html')

@app.route('/api/arquivos', methods=['GET'])
def listar_arquivos():
    return jsonify({'success': True, 'arquivos': carregar_arquivos()})

@app.route('/api/upload', methods=['POST'])
def upload_arquivo():
    if 'file' not in request.files:
        logger.warning("Upload chamado sem 'file' em request.files")
        return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'})

    file = request.files['file']
    if file.filename == '':
        logger.warning("Upload chamado com filename vazio")
        return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'})

    if file and file.filename:
        if not _upload_mime_ok(file):
            logger.warning("Upload bloqueado (validação MIME falhou): filename=%s mimetype=%s", getattr(file, 'filename', None), getattr(file, 'mimetype', None))
            return jsonify({'success': False, 'error': 'Tipo de arquivo inválido (MIME não esperado).'}), 400

        filename = secure_filename(file.filename or '')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_final = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_final)
        file.save(filepath)

        # Detecta extensão
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
        pode_gerar_ia = can_generate_questions(filename)

        arquivos = carregar_arquivos()
        arquivos.append({
            'id': len(arquivos) + 1,
            'nome': filename,
            'nome_arquivo': filename_final,
            'tipo': ext,
            'pode_gerar_ia': pode_gerar_ia,
            'data_upload': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'questoes_geradas': 0
        })
        salvar_arquivos(arquivos)

        logger.info("Upload ok: id=%s nome=%s tipo=%s pode_gerar_ia=%s path=%s", len(arquivos), filename, ext, pode_gerar_ia, filepath)
        return jsonify({'success': True, 'message': 'Arquivo enviado com sucesso'})

    logger.warning("Upload falhou: filename vazio ou inválido")
    return jsonify({'success': False, 'error': 'Erro ao processar arquivo'})

@app.route('/api/deletar-arquivo/<int:arquivo_id>', methods=['DELETE'])
def deletar_arquivo(arquivo_id):
    arquivos = carregar_arquivos()
    arquivo = next((a for a in arquivos if a['id'] == arquivo_id), None)

    if not arquivo:
        logger.warning("Delete arquivo: id=%s nao encontrado", arquivo_id)
        return jsonify({'success': False, 'error': 'Arquivo nao encontrado'})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], arquivo['nome_arquivo'])
    if os.path.exists(filepath):
        os.remove(filepath)

    arquivos = [a for a in arquivos if a['id'] != arquivo_id]
    salvar_arquivos(arquivos)

    logger.info("Arquivo deletado: id=%s path=%s", arquivo_id, filepath)
    return jsonify({'success': True, 'message': 'Arquivo deletado'})

@app.route('/api/gerar-questoes/<int:arquivo_id>', methods=['POST'])
def api_gerar_questoes(arquivo_id):
    data = request.get_json(silent=True) or {}
    # aceita num_questoes (frontend atual) OU num_perguntas (compat)
    num_questoes = int(data.get('num_questoes') or data.get('num_perguntas') or 5)
    provider = (data.get('provider') or 'auto').strip().lower()
    inicio = datetime.now()
    logger.info("Gerar questoes solicitado: arquivo_id=%s num_questoes=%s provider=%s", arquivo_id, num_questoes, provider)

    arquivos = carregar_arquivos()
    arquivo = next((a for a in arquivos if a['id'] == arquivo_id), None)

    if not arquivo:
        logger.warning("Gerar questoes: arquivo_id=%s nao encontrado", arquivo_id)
        return jsonify({'success': False, 'error': 'Arquivo nao encontrado'})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], arquivo['nome_arquivo'])
    try:
        texto = extrair_texto_pdf(filepath) if arquivo['tipo'] == 'pdf' else extrair_texto_txt(filepath)
    except Exception:
        logger.exception("Falha ao extrair texto: arquivo_id=%s path=%s", arquivo_id, filepath)
        return jsonify({'success': False, 'error': 'Erro ao extrair texto do arquivo'}), 500

    logger.debug("Texto extraido: arquivo_id=%s chars=%s", arquivo_id, len(texto or ""))

    # Gera via IA (retorna lista de objetos) usando escolha explícita de LLM
    try:
        questoes_ia = gerar_perguntas_llm_escolha(texto, num_questoes, provider=provider)
    except Exception as e:
        logger.exception("Erro ao gerar via IA: arquivo_id=%s provider=%s", arquivo_id, provider)
        return jsonify({'success': False, 'error': f'Erro ao gerar via IA ({provider}): {e}'}), 500

    # Normaliza para o formato esperado pelo frontend e pelo simulado
    questoes = []
    for idx, q in enumerate(questoes_ia, 1):
        alternativas = q.get('alternativas') or q.get('options') or []
        opcoes_map = {}
        letras = ['A', 'B', 'C', 'D']
        for i, alt in enumerate(alternativas[:4]):
            opcoes_map[letras[i]] = alt
        for i in range(len(opcoes_map), 4):
            opcoes_map[letras[i]] = f"(preencher manualmente {letras[i]})"

        questoes.append({
            'id': int(datetime.now().strftime('%H%M%S')) * 100 + idx,
            'k_level': 'K2',
            'pergunta': q.get('pergunta') or q.get('question') or '',
            'opcoes': opcoes_map,
            'resposta': (q.get('resposta') or q.get('answer') or 'A').strip(),
            'justificativa': q.get('justificativa') or '' ,
            'fonte': 'llm'
        })

    # Carrega banco, adiciona questões temporárias e salva
    banco = carregar_questoes_banco()
    if 'cap_arquivos' not in banco.get('questoes', {}):
        banco['questoes']['cap_arquivos'] = []
    banco['questoes']['cap_arquivos'].extend(questoes)
    salvar_questoes_banco(banco)

    arquivo['questoes_geradas'] += len(questoes)
    salvar_arquivos(arquivos)

    dur_ms = int((datetime.now() - inicio).total_seconds() * 1000)
    logger.info("Geracao concluida: arquivo_id=%s questoes=%s dur_ms=%s", arquivo_id, len(questoes), dur_ms)
    return jsonify({'success': True, 'questoes_geradas': len(questoes), 'questoes': questoes})

@app.route('/api/arquivos/salvar-questoes/<int:arquivo_id>', methods=['POST'])
def salvar_questoes_geradas(arquivo_id):
    data = request.get_json(silent=True) or {}
    questoes = data.get('questoes', [])
    if not questoes or not isinstance(questoes, list):
        logger.warning("Salvar questoes: payload invalido arquivo_id=%s", arquivo_id)
        return jsonify({'success': False, 'error': 'Nenhuma questão recebida.'}), 400

    def _extrair_alternativas(q: dict) -> list[str] | None:
        """Retorna uma lista com 4 alternativas a partir de `alternativas` (lista) ou `opcoes` (dict A-D)."""
        # 1) Formato esperado antigo: alternativas: [..]
        alternativas = q.get("alternativas")
        if isinstance(alternativas, list):
            alternativas_norm = [str(a).strip() for a in alternativas if str(a).strip()]
            if len(alternativas_norm) == 4:
                return alternativas_norm

        # 2) Formato atual do frontend/simulado: opcoes: {A:..,B:..,C:..,D:..}
        opcoes = q.get("opcoes")
        if isinstance(opcoes, dict):
            letras = ("A", "B", "C", "D")
            alternativas_norm = [str(opcoes.get(l, "")).strip() for l in letras]
            if len([a for a in alternativas_norm if a]) == 4:
                return alternativas_norm

        return None

    def _is_questao_completa(q: dict) -> tuple[bool, str, list[str] | None]:
        pergunta = (q.get("pergunta") or "").strip()
        alternativas_norm = _extrair_alternativas(q)
        resposta = (q.get("resposta") or "").strip().upper()

        if not pergunta:
            return False, "pergunta ausente", None
        if not isinstance(alternativas_norm, list) or len(alternativas_norm) != 4:
            return False, "alternativas inválidas (precisa 4 itens)", None
        if resposta not in ("A", "B", "C", "D"):
            return False, "resposta inválida (precisa A/B/C/D)", None
        return True, "", alternativas_norm

    completas = []
    invalidas = []
    for idx, q in enumerate(questoes, 1):
        if not isinstance(q, dict):
            invalidas.append({"idx": idx, "erro": "item não é objeto"})
            continue
        ok, motivo, alternativas_norm = _is_questao_completa(q)
        if ok:
            completas.append({
                "pergunta": (q.get("pergunta") or "").strip(),
                "alternativas": alternativas_norm or [],
                "resposta": (q.get("resposta") or "").strip().upper(),
            })
        else:
            invalidas.append({"idx": idx, "erro": motivo})

    logger.info(
        "Salvar questoes (pre-validacao): arquivo_id=%s recebidas=%s completas=%s invalidas=%s",
        arquivo_id,
        len(questoes),
        len(completas),
        len(invalidas),
    )
    if invalidas:
        logger.warning("Salvar questoes: invalidas=%s", invalidas[:10])

    if len(completas) == 0:
        return jsonify({
            'success': False,
            'error': (
                'As questões geradas vieram incompletas (pergunta + 4 alternativas + resposta A/B/C/D). '
                'Revise/complete manualmente no modal e tente salvar novamente.'
            ),
            'details': invalidas[:10]
        }), 400

    # Carrega o banco consolidado
    banco = carregar_questoes_banco()
    if 'questoes' not in banco:
        banco['questoes'] = {}

    payload = request.get_json(silent=True) or {}
    capitulo_id = (payload.get('capitulo_id') or 'importados').strip() or 'importados'
    capitulo_nome = (payload.get('capitulo_nome') or capitulo_id).strip() or capitulo_id

    # Mantém compatibilidade com o formato antigo (string) e também suporta objeto com label.
    capitulo_key = capitulo_id
    if capitulo_key not in banco['questoes']:
        banco['questoes'][capitulo_key] = []

    for q in completas:
        banco['questoes'][capitulo_key].append({
            'pergunta': q['pergunta'],
            'alternativas': q['alternativas'][:4],
            'resposta': q['resposta'],
            'capitulo_id': capitulo_id,
            'capitulo_nome': capitulo_nome,
        })

    # Atualiza metadados
    if 'metadata' not in banco:
        banco['metadata'] = {}
    banco['metadata']['ultima_atualizacao'] = datetime.now().isoformat()
    total_questoes = sum(len(v) if isinstance(v, list) else 0 for v in banco['questoes'].values())
    banco['metadata']['total_questoes'] = total_questoes
    
    salvar_questoes_banco(banco)

    logger.info(
        "Questoes salvas: arquivo_id=%s salvas=%s capitulo=%s descartadas=%s",
        arquivo_id,
        len(completas),
        capitulo_key,
        len(invalidas),
    )
    return jsonify({
        'success': True,
        'msg': f'{len(completas)} questões salvas no capítulo {capitulo_nome}.',
        'capitulo_id': capitulo_id,
        'capitulo_nome': capitulo_nome,
        'descartadas': len(invalidas)
    })

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/flashcards')
def flashcards():
    return render_template('flashcards.html')

@app.route('/api/flashcards', methods=['GET'])
def listar_flashcards():
    deck = request.args.get('deck', 'todos')
    capitulo_id = (request.args.get('capitulo_id') or 'todos').strip().lower()

    flashcards_list = carregar_flashcards()

    def _map_deck_para_capitulo_id(deck_nome: str, deck_id: str | None = None) -> str:
        # Preferência: deck_id (mais estável)
        did = (deck_id or '').lower()
        if did.startswith('deck_01'):
            return 'cap1'
        if did.startswith('deck_02'):
            return 'cap2'
        if did.startswith('deck_03'):
            return 'cap3'
        if did.startswith('deck_04'):
            return 'cap4'
        if did.startswith('deck_05'):
            return 'cap5'

        # Fallback: heurística por nome
        n = (deck_nome or '').strip().lower()
        if 'risk' in n:
            return 'cap1'
        if 'test techniques' in n or 'black box' in n or 'white box' in n or 'whitebox' in n or 'blackbox' in n:
            return 'cap2'
        if 'quality' in n:
            return 'cap3'
        if 'review' in n:
            return 'cap4'
        if 'tool' in n or 'automation' in n:
            return 'cap5'
        return 'importados'

    if deck != 'todos':
        flashcards_list = [f for f in flashcards_list if deck.lower() in (f.get('deck') or '').lower()]

    if capitulo_id != 'todos':
        flashcards_list = [
            f
            for f in flashcards_list
            if _map_deck_para_capitulo_id(f.get('deck') or '', f.get('deck_id')) == capitulo_id
        ]

    return jsonify({'success': True, 'total': len(flashcards_list), 'flashcards': flashcards_list})

@app.route('/api/flashcards/decks', methods=['GET'])
def listar_decks():
    flashcards_list = carregar_flashcards()
    decks = {}

    for f in flashcards_list:
        deck_nome = f.get('deck')
        deck_id = f.get('deck_id')
        if not deck_nome:
            continue

        if deck_nome not in decks:
            decks[deck_nome] = {"nome": deck_nome, "deck_id": deck_id, "total": 0}
        decks[deck_nome]["total"] += 1

    return jsonify({'success': True, 'decks': list(decks.values())})

@app.route('/api/estatisticas', methods=['GET'])
def estatisticas():
    tracking_file = "progresso_simulados.json"
    
    if not os.path.exists(tracking_file):
        return jsonify({'success': True, 'total_simulados': 0, 'media_geral': 0, 'simulados': []})
    
    with open(tracking_file, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    simulados = dados.get('simulados', [])
    if not simulados:
        return jsonify({'success': True, 'total_simulados': 0, 'media_geral': 0, 'simulados': []})
    
    total_questoes = sum(s['total_questoes'] for s in simulados)
    total_acertos = sum(s['acertos'] for s in simulados)
    media_geral = (total_acertos / total_questoes) * 100 if total_questoes > 0 else 0
    
    return jsonify({
        'success': True,
        'total_simulados': len(simulados),
        'media_geral': round(media_geral, 1),
        'simulados': simulados[-10:]
    })

@app.route('/api/llm-opcoes', methods=['GET'])
def api_llm_opcoes():
    """Retorna as opções de LLM disponíveis para o frontend montar o seletor dinamicamente."""
    opcoes = [
        {
            'id': 'auto',
            'label': 'Automático (Ollama → HuggingFace)',
            'descricao': 'Tenta usar Ollama local; se não estiver disponível, usa HuggingFace.',
        },
        {
            'id': 'ollama',
            'label': 'Ollama local',
            'descricao': 'Usa apenas o modelo configurado no Ollama (variável OLLAMA_MODEL).',
        },
        {
            'id': 'hf_mistral',
            'label': 'HuggingFace – Mistral',
            'descricao': 'Usa o modelo mistralai/Mistral-7B-Instruct-v0.2 na HuggingFace.',
        },
        {
            'id': 'hf_phi3',
            'label': 'HuggingFace – Phi-3',
            'descricao': 'Usa o modelo microsoft/Phi-3-mini-4k-instruct na HuggingFace.',
        },
        {
            'id': 'hf_zephyr',
            'label': 'HuggingFace – Zephyr',
            'descricao': 'Usa o modelo HuggingFaceH4/zephyr-7b-beta na HuggingFace.',
        },
        {
            'id': 'hf_qwen',
            'label': 'HuggingFace – Qwen',
            'descricao': 'Usa o modelo Qwen/Qwen2.5-7B-Instruct na HuggingFace.',
        },
        {
            'id': 'gpt-4.1-mini',
            'label': 'OpenAI – gpt-4.1-mini',
            'descricao': 'Usa o modelo gpt-4.1-mini via API da OpenAI.',
        },
        {
            'id': 'openai_pro',
            'label': 'OpenAI – modelo Pro',
            'descricao': 'Usa o modelo definido em OPENAI_MODEL_PRO (padrão gpt-4.1).',
        },
    ]
    return jsonify({'success': True, 'opcoes': opcoes})

@app.route('/geracoes')

def pagina_geracoes():
    return render_template('geracoes.html')

# --- Materiais de estudo (mídias do uploads/) ---
from flask import send_from_directory, abort
from pathlib import Path

def _materiais_tipo_por_ext(filename: str) -> str:
    ext = (Path(filename).suffix or '').lower().lstrip('.')
    if ext == 'pdf':
        return 'pdf'
    if ext in {'mp3', 'wav', 'm4a', 'aac', 'ogg', 'opus'}:
        return 'audio'
    if ext in {'mp4', 'webm', 'mkv', 'mov'}:
        return 'video'
    return 'outros'

# extensões permitidas para servir pela rota /api/materiais/arquivo/<nome>
_MATERIAIS_ALLOWED_EXT = {
    'pdf',
    'mp3', 'wav', 'm4a', 'aac', 'ogg', 'opus',
    'mp4', 'webm', 'mkv', 'mov',
}

@app.route('/estudos')
def estudos():
    # Página de estudos foi unificada na tela de Arquivos.
    # Mantém compatibilidade com links antigos.
    from flask import redirect
    return redirect('/arquivos', code=302)

@app.route('/api/materiais', methods=['GET'])
def api_materiais_listar():
    try:
        upload_dir = Path(app.config['UPLOAD_FOLDER'])
        upload_dir.mkdir(parents=True, exist_ok=True)

        materiais = []
        # lista apenas a raiz de uploads/ (sem subpastas)
        for p in upload_dir.iterdir():
            if not p.is_file():
                continue

            nome = p.name  # exatamente como está no disco
            ext = (p.suffix or '').lower().lstrip('.')
            if ext and ext not in _MATERIAIS_ALLOWED_EXT:
                # mantém fora da lista para não expor tipos arbitrários
                continue

            stat = p.stat()
            materiais.append({
                'nome': nome,
                'tipo': _materiais_tipo_por_ext(nome),
                'tamanho_bytes': int(stat.st_size),
                'modificado_em': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'url': f"/api/materiais/arquivo/{nome}",
            })

        materiais.sort(key=lambda x: x['nome'].lower())
        return jsonify({'success': True, 'materiais': materiais})
    except Exception as e:
        logger.exception('Erro ao listar materiais')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/materiais/arquivo/<path:filename>', methods=['GET'])
def api_materiais_arquivo(filename):
    # Proteção básica contra path traversal + allowlist de extensões
    p = Path(filename)
    if p.name != filename:
        abort(400)

    ext = (p.suffix or '').lower().lstrip('.')
    if ext and ext not in _MATERIAIS_ALLOWED_EXT:
        abort(404)

    upload_dir = Path(app.config['UPLOAD_FOLDER'])
    return send_from_directory(upload_dir, filename, as_attachment=False)

# --- fim: Materiais de estudo ---

if __name__ == "__main__":
    # opcional: ler PORT ou DEBUG de variáveis de ambiente
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=debug, port=port)
