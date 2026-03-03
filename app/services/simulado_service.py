# Serviços relacionados a simulados
# Funções de lógica de negócio serão migradas do script original posteriormente

import random
from datetime import datetime
import os
import json
import requests
import re
import logging

logger = logging.getLogger(__name__)


def _carregar_questoes_db() -> dict:
    """Carrega questões a partir do banco consolidado `questoes_banco.json`.

    Fallbacks:
    - Se o arquivo consolidado não existir, tenta `banco_questoes.json` (legado).
    - Em erro de leitura/parsing, retorna dict vazio para evitar crash no import.
    """
    candidatos = ["questoes_banco.json", "banco_questoes.json"]
    for path in candidatos:
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                dados = json.load(f)

            if path == "questoes_banco.json":
                questoes = dados.get("questoes", {})
                if isinstance(questoes, dict):
                    return questoes
                logger.warning("Formato inesperado em %s: chave 'questoes' inválida", path)
                return {}

            if isinstance(dados, dict):
                return dados
            logger.warning("Formato inesperado em %s: conteúdo não é objeto JSON", path)
            return {}
        except Exception:
            logger.exception("Erro ao carregar banco de questões: %s", path)
            return {}

    logger.warning("Nenhum arquivo de banco de questões encontrado (%s)", ", ".join(candidatos))
    return {}


QUESTOES_DB = _carregar_questoes_db()

# --------- LLM (HuggingFace / Ollama / OpenAI) ---------

def _extrair_json_lista(generated: str):
    """Best-effort extraction of a JSON *array* from a model-generated string.

    This function is intentionally tolerant to common LLM output issues such as:
      - Markdown fences (```json ... ```
      - Extra text before/after the JSON payload
      - Multiple JSON-like segments (we try the first array found)

    Returns:
        list | None: The parsed JSON array, or None if it cannot be parsed.
    """
    if not generated:
        return None

    txt = generated.strip()

    # remove fences ```json ... ```
    m = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", txt, flags=re.DOTALL | re.IGNORECASE)
    if m:
        candidate = m.group(1)
        try:
            obj = json.loads(candidate)
            return obj if isinstance(obj, list) else None
        except Exception:
            pass

    # tenta pegar o primeiro array JSON bem formado pelo menor trecho entre [ ... ]
    start = txt.find('[')
    if start == -1:
        return None

    # busca o fechamento correspondente mais à direita (fallback) e tenta também o primeiro possível
    end_last = txt.rfind(']')
    candidates = []
    if end_last != -1 and end_last > start:
        candidates.append(txt[start:end_last + 1])

    # tenta achar um fechamento mais cedo para evitar pegar lixo depois
    for end in range(start + 1, min(len(txt), start + 20000)):
        if txt[end] == ']':
            candidates.insert(0, txt[start:end + 1])
            break

    for json_text in candidates:
        try:
            obj = json.loads(json_text)
            return obj if isinstance(obj, list) else None
        except Exception:
            continue

    return None


def _ollama_is_online(base_url: str = "http://localhost:11434", timeout: int = 2) -> bool:
    """Quick healthcheck for Ollama local server."""
    try:
        r = requests.get(f"{base_url}/api/tags", timeout=timeout)
        ok = r.status_code == 200
        logger.debug("Ollama healthcheck: url=%s ok=%s", base_url, ok)
        return ok
    except Exception:
        logger.debug("Ollama healthcheck falhou: url=%s", base_url, exc_info=True)
        return False


def _normalizar_e_validar_questoes_llm(questoes_raw, num_perguntas: int | None = None):
    """Normalize and validate question objects received from an LLM.

    Accepts multiple input shapes:
      - {pergunta, alternativas:[...], resposta:'A', justificativa}
      - {question, options:[...], answer:'B'}
      - {pergunta, opcoes:{A,B,C,D}, resposta:'C'}

    A question is considered valid only if it contains:
      - a non-empty question text
      - exactly 4 alternatives
      - an answer in A/B/C/D

    Returns:
        (ok, errors):
          ok: list[dict] normalized to {pergunta, alternativas, resposta, justificativa}
          errors: list[str] human-readable issues for logging/debug
    """
    erros: list[str] = []
    ok: list[dict] = []

    if not isinstance(questoes_raw, list):
        return [], ["LLM não retornou uma lista JSON de questões."]

    for i, q in enumerate(questoes_raw):
        if not isinstance(q, dict):
            erros.append(f"Q{i+1}: item não é objeto JSON")
            continue

        pergunta = (q.get("pergunta") or q.get("question") or "").strip()

        alternativas: list[str] = []
        if isinstance(q.get("alternativas"), list):
            alternativas = [str(x).strip() for x in (q.get("alternativas") or []) if str(x).strip()]
        elif isinstance(q.get("options"), list):
            alternativas = [str(x).strip() for x in (q.get("options") or []) if str(x).strip()]
        elif isinstance(q.get("opcoes"), dict):
            op = q.get("opcoes") or {}
            alternativas = [str(op.get(l, "")).strip() for l in ("A", "B", "C", "D") if str(op.get(l, "")).strip()]

        resposta = (q.get("resposta") or q.get("answer") or "").strip()
        justificativa = (q.get("justificativa") or q.get("rationale") or "").strip()

        problemas_item = []
        if not pergunta:
            problemas_item.append("pergunta ausente")
        if len(alternativas) != 4:
            problemas_item.append(f"alternativas inválidas (esperado 4, veio {len(alternativas)})")
        if resposta.upper() not in ("A", "B", "C", "D"):
            problemas_item.append("resposta inválida (esperado A/B/C/D)")

        if problemas_item:
            # logar um preview para análise, sem explodir o log
            preview = json.dumps(q, ensure_ascii=False)[:600]
            erros.append(f"Q{i+1}: {', '.join(problemas_item)} | preview={preview}")
            continue

        ok.append({
            "pergunta": pergunta,
            "alternativas": alternativas[:4],
            "resposta": resposta.upper(),
            "justificativa": justificativa,
        })

    # aviso se quantidade gerada não bate com a solicitada
    if num_perguntas is not None and ok and len(ok) != int(num_perguntas):
        erros.append(f"Quantidade de questões válidas diferente do solicitado: ok={len(ok)} solicitado={num_perguntas}")

    return ok, erros


def gerar_perguntas_ollama(texto, num_perguntas=3, model=None, base_url: str = "http://localhost:11434"):
    """Generate multiple-choice questions using a local Ollama model."""
    model = model or os.getenv("OLLAMA_MODEL") or "phi3"

    # limitar texto e tornar o prompt mais "inviolável" para JSON
    max_chars = int(os.getenv("OLLAMA_MAX_CHARS", "2500"))
    texto_curto = (texto or "")[:max_chars]

    prompt = (
        "Você é um gerador de questões para estudo ISTQB CTAL-TA. "
        "A partir do TEXTO a seguir, gere questões de múltipla escolha de alta qualidade.\n\n"
        "REQUISITOS DE SAÍDA (OBRIGATÓRIO):\n"
        f"1) Gere EXATAMENTE {num_perguntas} itens.\n"
        "2) Responda SOMENTE com JSON válido (sem markdown, sem comentários, sem texto fora do JSON).\n"
        "3) O JSON deve ser um ARRAY (lista) de objetos.\n"
        "4) Cada objeto deve conter exatamente os campos: \"pergunta\" (string), \"alternativas\" (array com 4 strings), \"resposta\" (A|B|C|D), \"justificativa\" (string).\n"
        "5) Não use campos extras, não numere as questões fora do JSON.\n"
        "6) As alternativas devem ser plausíveis, com apenas UMA correta.\n\n"
        "TEXTO:\n" + texto_curto
    )

    num_predict = int(os.getenv("OLLAMA_NUM_PREDICT", "450"))
    timeout_sec = int(os.getenv("OLLAMA_TIMEOUT", "90"))
    max_output_chars = int(os.getenv("OLLAMA_MAX_OUTPUT_CHARS", "20000"))

    payload = {
        "model": model,
        "prompt": prompt,
        # streaming ON para evitar ficar preso esperando o fim
        "stream": True,
        "options": {
            "temperature": 0.4,
            "num_predict": num_predict,
        },
    }

    logger.info(
        "OLLAMA gerar_perguntas: model=%s num_perguntas=%s chars=%s num_predict=%s timeout=%s",
        model,
        num_perguntas,
        len(texto_curto),
        num_predict,
        timeout_sec,
    )

    t0 = datetime.now()
    try:
        # read timeout: se parar de chegar chunk por timeout_sec, aborta
        with requests.post(
            f"{base_url}/api/generate",
            json=payload,
            stream=True,
            timeout=(5, timeout_sec),
        ) as r:
            r.raise_for_status()

            partes = []
            total_chars = 0
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue

                chunk = obj.get("response") or ""
                if chunk:
                    partes.append(chunk)
                    total_chars += len(chunk)
                    if total_chars >= max_output_chars:
                        logger.warning("OLLAMA output truncado: max_output_chars=%s", max_output_chars)
                        break

                if obj.get("done") is True:
                    break

        generated = "".join(partes).strip()

    except requests.exceptions.Timeout as e:
        dur_ms = int((datetime.now() - t0).total_seconds() * 1000)
        logger.warning("OLLAMA timeout: dur_ms=%s", dur_ms)
        raise RuntimeError(f"Ollama timeout após {timeout_sec}s") from e

    dur_ms = int((datetime.now() - t0).total_seconds() * 1000)
    logger.info("OLLAMA resposta recebida: dur_ms=%s chars_saida=%s", dur_ms, len(generated))
    logger.debug("OLLAMA texto gerado (completo): %s", generated)

    questoes_raw = _extrair_json_lista(generated)
    if isinstance(questoes_raw, list) and questoes_raw:
        questoes_ok, erros = _normalizar_e_validar_questoes_llm(questoes_raw, num_perguntas=num_perguntas)
        logger.info(
            "OLLAMA parse JSON: raw=%s ok=%s invalidas=%s",
            len(questoes_raw),
            len(questoes_ok),
            max(0, len(questoes_raw) - len(questoes_ok)),
        )
        if erros:
            logger.warning("OLLAMA itens invalidos: %s", " || ".join(erros[:6]))

        if questoes_ok:
            return questoes_ok

    logger.warning("OLLAMA nao retornou JSON valido/itens completos; usando parser heuristico")
    heur = parsear_questoes_geradas(generated)
    # parser heurístico não garante 4 alternativas/resposta A-D; logar para diagnóstico
    logger.info("OLLAMA heuristico: questoes=%s", len(heur) if isinstance(heur, list) else 0)
    return heur


def gerar_perguntas_openai(texto, num_perguntas=3, model: str | None = None):
    """Gera perguntas usando a API da OpenAI, com o mesmo contrato das demais funções.

    Espera que OPENAI_API_KEY esteja definido no ambiente.
    Usa o mesmo formato de JSON de saída para reaproveitar o parser existente.
    """
    import os
    import requests

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não definido no ambiente.")

    model = model or os.getenv("OPENAI_MODEL") or "gpt-4.1-mini"

    # Limita o texto para evitar excesso de tokens/contexto
    texto_curto = (texto or "")[:6000]
    logger.info("OpenAI gerar_perguntas: model=%s num_perguntas=%s chars=%s", model, num_perguntas, len(texto_curto))

    prompt = (
        "Você é um gerador de questões para estudo ISTQB CTAL-TA. "
        "A partir do TEXTO a seguir, crie questões de múltipla escolha alinhadas ao syllabus. "
        "Responda SOMENTE com um JSON válido, sem markdown, sem comentários e sem texto fora do JSON. "
        "Formato: lista JSON de objetos com os campos: pergunta (string), alternativas (lista com 4 strings), "
        "resposta (A/B/C/D), justificativa (string). "
        f"Gere EXATAMENTE {num_perguntas} questões bem distribuídas nos conceitos do texto.\n\n"
        "TEXTO:\n" + texto_curto
    )

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Você é um assistente que gera APENAS JSON válido conforme solicitado."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
        "response_format": {"type": "json_object"},
    }

    t0 = datetime.now()
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=90)
        resp.raise_for_status()
    except requests.exceptions.Timeout as e:
        dur_ms = int((datetime.now() - t0).total_seconds() * 1000)
        logger.warning("OpenAI timeout: dur_ms=%s", dur_ms)
        raise RuntimeError("OpenAI timeout ao gerar questões") from e

    dur_ms = int((datetime.now() - t0).total_seconds() * 1000)
    data = resp.json()
    logger.info("OpenAI resposta recebida: dur_ms=%s", dur_ms)

    # Com response_format=json_object, o conteúdo vem como um JSON em string dentro de content
    try:
        content = data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.exception("OpenAI: estrutura inesperada de resposta: %s", e)
        raise RuntimeError("Resposta inesperada da OpenAI") from e

    # Esperamos que 'content' seja uma string JSON.
    # Pode ser um objeto com campo "questoes" ou um array diretamente.
    questoes_raw = None
    try:
        parsed = json.loads(content)
        if isinstance(parsed, list):
            questoes_raw = parsed
        elif isinstance(parsed, dict):
            # tenta alguns campos comuns
            for key in ("questoes", "questions", "itens"):
                if key in parsed and isinstance(parsed[key], list):
                    questoes_raw = parsed[key]
                    break
    except Exception:
        logger.exception("OpenAI: falha ao fazer json.loads do content")

    if questoes_raw is None:
        # como fallback interno apenas de parse, reutiliza o extrator generico
        questoes_raw = _extrair_json_lista(content)

    if (not isinstance(questoes_raw, list)) or (not questoes_raw):
        # ultimo fallback: tentar parser heuristico em texto livre
        logger.warning("OpenAI nao retornou JSON de lista; tentando parser heuristico de texto")
        try:
            questoes_raw = parsear_questoes_geradas(content)
        except Exception:
            logger.exception("OpenAI: falha tambem no parser heuristico")
            questoes_raw = []

    if (not isinstance(questoes_raw, list)) or (not questoes_raw):
        logger.error("OpenAI nao produziu questoes aproveitaveis (JSON ou heuristica).")
        return []

    questoes_ok, erros = _normalizar_e_validar_questoes_llm(questoes_raw, num_perguntas=num_perguntas)
    logger.info(
        "OpenAI parse JSON: raw=%s ok=%s invalidas=%s",
        len(questoes_raw),
        len(questoes_ok),
        max(0, len(questoes_raw) - len(questoes_ok)),
    )
    if erros:
        logger.warning("OpenAI itens invalidos: %s", " || ".join(erros[:6]))

    if not questoes_ok:
        logger.error("OpenAI retornou itens, mas nenhum passou na validacao de formato.")
        return []

    return questoes_ok


def gerar_perguntas_llm(texto, num_perguntas=3):
    """Selects the configured LLM provider and generates questions."""
    provider = (os.getenv("LLM_PROVIDER") or "auto").strip().lower()
    logger.info("LLM provider selecionado: %s", provider)

    if provider in ("ollama", "auto"):
        if _ollama_is_online():
            try:
                return gerar_perguntas_ollama(texto, num_perguntas=num_perguntas)
            except Exception as e:
                if provider == "auto":
                    logger.warning("OLLAMA falhou (%s). Fallback para HuggingFace.", e)
                else:
                    # modo forçado ollama: apenas propaga o erro
                    raise
        if provider == "ollama":
            raise RuntimeError("LLM_PROVIDER=ollama, mas o Ollama nao respondeu em http://localhost:11434")

    logger.info("Fallback para HuggingFace")
    try:
        return gerar_perguntas_huggingface(texto, num_perguntas=num_perguntas)
    except Exception as e:
        logger.error("HF (modo auto) falhou: %s", e)
        return []


def gerar_perguntas_llm_escolha(texto, num_perguntas=3, provider: str | None = None):
    """Gera perguntas usando o provider explicito escolhido pelo usuario.

    Providers suportados:
      - auto         -> usar logica padrao (Ollama -> HF)
      - ollama       -> forca Ollama (sem fallback)
      - hf_mistral   -> forca HF com modelo Mistral
      - hf_phi3      -> forca HF com modelo Phi-3
      - hf_zephyr    -> forca HF com modelo Zephyr
      - hf_qwen      -> forca HF com modelo Qwen
      - gpt-4.1-mini -> forca OpenAI gpt-4.1-mini
      - openai_pro   -> forca OpenAI modelo "profissional" (OPENAI_MODEL_PRO ou gpt-4.1)
    """
    provider = (provider or "auto").strip().lower()
    logger.info("LLM provider (escolha usuario): %s", provider)

    if provider == "auto":
        return gerar_perguntas_llm(texto, num_perguntas=num_perguntas)

    if provider == "ollama":
        if not _ollama_is_online():
            raise RuntimeError("Ollama nao esta disponivel em http://localhost:11434")
        return gerar_perguntas_ollama(texto, num_perguntas=num_perguntas)

    if provider in ("hf_mistral", "hf_phi3", "hf_zephyr", "hf_qwen"):
        def _hf_custom(texto_inner, num_inner):
            token = os.getenv("HF_API_TOKEN")
            if not token:
                raise RuntimeError("HF_API_TOKEN nao definido no ambiente.")

            headers = {"Authorization": f"Bearer {token}"}
            if provider == "hf_mistral":
                modelos = ["https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"]
            elif provider == "hf_phi3":
                modelos = ["https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"]
            elif provider == "hf_zephyr":
                modelos = ["https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"]
            else:
                modelos = ["https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"]

            texto_curto = (texto_inner or "")[:6000]
            logger.info("HF (%s) gerar_perguntas: num_perguntas=%s chars=%s", provider, num_inner, len(texto_curto))

            prompt = (
                "Voce e um gerador de questoes para estudo ISTQB. "
                "Crie questoes de multipla escolha a partir do TEXTO. "
                "Responda SOMENTE com um JSON valido (sem markdown, sem explicacoes fora do JSON). "
                "Formato: lista JSON de objetos com os campos: pergunta (string), alternativas (lista com 4 strings), "
                "resposta (A/B/C/D), justificativa (string). "
            )
            prompt += f"Gere EXATAMENTE {num_inner} questoes.\n\n"
            prompt += "TEXTO:\n" + texto_curto

            timeout = int(os.getenv("HF_TIMEOUT", "90"))

            ult_err = None
            for model_url in modelos:
                try:
                    payload = {"inputs": prompt, "options": {"wait_for_model": True}}
                    resp = _hf_post_model(model_url, headers, payload, timeout)
                    if resp.status_code == 503:
                        ult_err = f"Modelo {model_url} indisponivel (503)."
                        continue
                    resp.raise_for_status()

                    data = resp.json()
                    if isinstance(data, list) and data and isinstance(data[0], dict) and "generated_text" in data[0]:
                        generated = data[0]["generated_text"]
                    else:
                        generated = json.dumps(data, ensure_ascii=False)

                    questoes_raw = _extrair_json_lista(generated)
                    if not isinstance(questoes_raw, list) or not questoes_raw:
                        raise RuntimeError("HF nao retornou JSON de questoes.")

                    questoes_ok, erros = _normalizar_e_validar_questoes_llm(questoes_raw, num_perguntas=num_inner)
                    logger.info(
                        "HF (%s) parse JSON: raw=%s ok=%s invalidas=%s",
                        provider,
                        len(questoes_raw),
                        len(questoes_ok),
                        max(0, len(questoes_raw) - len(questoes_ok)),
                    )
                    if erros:
                        logger.warning("HF (%s) itens invalidos: %s", provider, " || ".join(erros[:6]))

                    if not questoes_ok:
                        raise RuntimeError("HF retornou itens, mas nenhum passou na validacao.")

                    return questoes_ok

                except Exception as e:
                    ult_err = str(e)
                    logger.warning("HF (%s) falhou em %s: %s", provider, model_url, e)

            logger.error("HF (%s) falhou em todos os modelos: %s", provider, ult_err)
            return []

        return _hf_custom(texto, num_perguntas)

    if provider == "gpt-4.1-mini":
        # forca modelo mini
        return gerar_perguntas_openai(texto, num_perguntas=num_perguntas, model="gpt-4.1-mini")

    if provider == "openai_pro":
        # modelo "pro" pode ser configurado por env, com default gpt-4.1
        model_pro = os.getenv("OPENAI_MODEL_PRO") or "gpt-4.1"
        return gerar_perguntas_openai(texto, num_perguntas=num_perguntas, model=model_pro)

    # Provider desconhecido -> volta para auto
    logger.warning("Provider LLM desconhecido: %s; usando 'auto'", provider)
    return gerar_perguntas_llm(texto, num_perguntas=num_perguntas)

def gerar_simulado(capitulo="todos", num_questoes=10, k_levels=None):
    """Return a random sample of questions for a chapter (and optional K-level filters)."""
    if capitulo == "todos":
        questoes_disponiveis = []
        for cap in QUESTOES_DB.values():
            questoes_disponiveis.extend(cap)
    else:
        questoes_disponiveis = QUESTOES_DB.get(capitulo, [])
    if k_levels:
        questoes_disponiveis = [q for q in questoes_disponiveis if q['k_level'] in k_levels]
    num_questoes = min(num_questoes, len(questoes_disponiveis))
    return random.sample(questoes_disponiveis, num_questoes)

def identificar_capitulo(id_questao):
    """Map a numeric question id to its syllabus chapter label."""
    if id_questao <= 52:
        return "Cap 1: Risk-Based Testing"
    elif id_questao <= 75:
        return "Cap 2: Test Techniques"
    elif id_questao <= 82:
        return "Cap 3: Quality Characteristics"
    elif id_questao <= 87:
        return "Cap 4: Reviews"
    else:
        return "Cap 5: Test Tools"

def salvar_no_tracking(capitulo, total, acertos, tempo):
    """Append a simulation attempt into the tracking JSON file.

    This is the single source of truth used by both the web app and legacy CLI.
    """
    tracking_file = "progresso_simulados.json"
    if os.path.exists(tracking_file):
        with open(tracking_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    else:
        dados = {"simulados": []}
    resultado = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "capitulo": capitulo,
        "total_questoes": total,
        "acertos": acertos,
        "percentual": round((acertos / total) * 100, 1),
        "tempo_minutos": tempo,
        "aprovado": acertos >= (total * 0.65)
    }
    dados["simulados"].append(resultado)
    xp_ganho = total * 10 + acertos * 20
    if acertos >= (total * 0.65):
        xp_ganho += 100
    if acertos == total and total >= 5:
        xp_ganho += 300
    logger.info("GAMIFICATION xp_ganho=%s capitulo=%s total=%s acertos=%s", xp_ganho, capitulo, total, acertos)
    with open(tracking_file, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def analisar_pontos_fracos():
    """Identify chapters below the configured performance threshold (default: < 70%)."""
    tracking_file = "progresso_simulados.json"
    if not os.path.exists(tracking_file):
        return []
    with open(tracking_file, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    stats = {}
    for sim in dados.get("simulados", []):
        cap = sim['capitulo']
        if cap == "completo":
            continue
        if cap not in stats:
            stats[cap] = {'acertos': 0, 'total': 0}
        stats[cap]['acertos'] += sim['acertos']
        stats[cap]['total'] += sim['total_questoes']
    fracos = []
    for cap, s in stats.items():
        if s['total'] > 0:
            media = s['acertos'] / s['total']
            if media < 0.70:
                fracos.append(cap)
    return fracos

# NOTE:
# The functions below were legacy CLI stubs and are not used by the web API.
# They were removed to keep this module focused and avoid confusion.
# (Full implementations remain in the legacy CLI scripts, if needed.)

def _hf_post_model(model_url, headers, payload, timeout):
    return requests.post(model_url, headers=headers, json=payload, timeout=timeout)


def gerar_perguntas_huggingface(texto, num_perguntas=3):
    """Gera perguntas de multipla escolha usando HuggingFace Inference API."""
    token = os.getenv("HF_API_TOKEN")
    if not token:
        raise RuntimeError("Token da HuggingFace nao encontrado. Defina a variavel de ambiente HF_API_TOKEN.")
    headers = {"Authorization": f"Bearer {token}"}

    # Modelos em ordem de tentativa (alguns endpoints podem retornar 410/indisponivel)
    modelos = [
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
        "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
        "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct",
        "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct",
    ]

    # Limita o texto para evitar excesso de tokens/contexto
    texto_curto = (texto or "")[:6000]
    logger.info("HF gerar_perguntas: num_perguntas=%s chars=%s", num_perguntas, len(texto_curto))

    prompt = (
        "Voce e um gerador de questoes para estudo ISTQB CTAL-TA. "
        "Crie questoes de multipla escolha a partir do TEXTO. "
        "Responda SOMENTE com um JSON valido (sem markdown, sem explicacoes fora do JSON). "
        "Formato: lista JSON de objetos com os campos: pergunta (string), alternativas (lista com 4 strings), "
        "resposta (A/B/C/D), justificativa (string). "
        f"Gere EXATAMENTE {num_perguntas} questoes. "
        "As alternativas devem ser plausiveis e apenas uma correta. TEXTO:\n" + texto_curto
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 900,
            "temperature": 0.4,
            "return_full_text": False
        }
    }

    last_err = None
    for API_URL in modelos:
        try:
            logger.info("HF tentativa modelo: %s", API_URL)
            response = _hf_post_model(API_URL, headers, payload, timeout=180)
            if response.status_code == 410:
                last_err = RuntimeError(f"Modelo indisponivel (410 Gone): {API_URL}")
                logger.warning("HF modelo indisponivel (410): %s", API_URL)
                continue
            response.raise_for_status()

            raw = response.json()
            if isinstance(raw, list) and raw and isinstance(raw[0], dict):
                generated = raw[0].get('generated_text') or ''
            elif isinstance(raw, dict):
                generated = raw.get('generated_text') or raw.get('output_text') or str(raw)
            else:
                generated = str(raw)

            logger.debug("HF texto gerado (inicio): %s", generated[:500])

            questoes = _extrair_json_lista(generated)
            if isinstance(questoes, list) and questoes:
                logger.info("HF parse JSON OK: questoes=%s", len(questoes))
                return questoes

            logger.warning("HF nao retornou JSON valido; usando parser heuristico")
            return parsear_questoes_geradas(generated)

        except Exception as e:
            last_err = e
            logger.warning("HF falhou no modelo: %s err=%s", API_URL, e)
            continue

    logger.error("Falha ao gerar questoes via HuggingFace. Ultimo erro: %s", last_err)
    return []


def parsear_questoes_geradas(texto):
    """Extrai perguntas, alternativas e resposta correta do texto gerado pela IA."""
    questoes = []
    blocos = re.split(r'\n\s*\n', texto)
    for bloco in blocos:
        linhas = [l.strip() for l in bloco.split('\n') if l.strip()]
        pergunta = ''
        alternativas = []
        resposta = ''
        for l in linhas:
            if l.lower().startswith('pergunta') or l.endswith('?'):
                pergunta = l.replace('Pergunta:', '').strip()
            elif re.match(r'^[A-Da-d][\)|\.]', l):
                alternativas.append(re.sub(r'^[A-Da-d][\)|\.]\s*', '', l))
            elif l.lower().startswith('resposta'):
                resposta = l.split(':',1)[-1].strip()
        if pergunta and alternativas and resposta:
            questoes.append({
                'pergunta': pergunta,
                'alternativas': alternativas,
                'resposta': resposta
            })
    return questoes
