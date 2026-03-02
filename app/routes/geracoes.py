"""Rotas relacionadas a gerações assíncronas de questões (jobs)."""

from __future__ import annotations

import json
import os

from flask import Blueprint, jsonify, request, current_app

from app.services.geracoes_service import GeracoesService


geracoes_bp = Blueprint("geracoes", __name__)


def _service() -> GeracoesService:
    return GeracoesService(geracoes_file=current_app.config["GERACOES_FILE"])


def _carregar_arquivos_storage() -> list[dict]:
    """Carrega a lista de arquivos do mesmo storage usado no app principal.

    Mantém o blueprint desacoplado de handlers HTTP.
    """
    arquivos_file = current_app.config.get("ARQUIVOS_FILE") or "arquivos_anexados.json"
    if os.path.exists(arquivos_file):
        with open(arquivos_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


@geracoes_bp.get("/api/geracoes")
def listar_geracoes():
    jobs_resumo = _service().listar_jobs_resumo()
    return jsonify({"success": True, "jobs": jobs_resumo})


@geracoes_bp.post("/api/geracoes")
def criar_geracao():
    data = request.get_json(silent=True) or {}
    arquivo_id = data.get("arquivo_id")
    num_questoes = int(data.get("num_questoes") or 5)
    provider = (data.get("provider") or "auto").strip().lower()

    capitulo_id = data.get("capitulo_id") or "importados"
    capitulo_nome = data.get("capitulo_nome") or "Importados / Outros"

    arquivos = _carregar_arquivos_storage()
    arquivo = next((a for a in arquivos if a.get("id") == arquivo_id), None)
    if not arquivo:
        return jsonify({"success": False, "error": "Arquivo não encontrado"}), 404

    job = _service().criar_job(
        arquivo=arquivo,
        num_questoes=num_questoes,
        provider=provider,
        capitulo_id=capitulo_id,
        capitulo_nome=capitulo_nome,
    )
    return jsonify({"success": True, "job_id": job["id"]})


@geracoes_bp.get("/api/geracoes/<job_id>")
def obter_geracao(job_id: str):
    job = _service().buscar_job(job_id)
    if not job:
        return jsonify({"success": False, "error": "Job não encontrado"}), 404
    return jsonify({"success": True, "job": job})


@geracoes_bp.post("/api/geracoes/<job_id>/salvar")
def salvar_geracao(job_id: str):
    job = _service().buscar_job(job_id)
    if not job:
        return jsonify({"success": False, "error": "Job não encontrado"}), 404

    payload = request.get_json(silent=True) or {}
    questoes_payload = payload.get("questoes") or job.get("questoes") or []

    capitulo_id = payload.get("capitulo_id") or job.get("capitulo_id") or "importados"
    capitulo_nome = payload.get("capitulo_nome") or job.get("capitulo_nome") or capitulo_id

    # Reuso da lógica da rota de salvar questões de arquivo.
    with current_app.test_request_context(
        json={
            "questoes": questoes_payload,
            "capitulo_id": capitulo_id,
            "capitulo_nome": capitulo_nome,
        }
    ):
        resp = current_app.view_functions["salvar_questoes_geradas"](job.get("arquivo_id"))

        if isinstance(resp, tuple):
            resp_obj, _status = resp
        else:
            resp_obj = resp

        try:
            data_resp = resp_obj.get_json()
        except Exception:
            data_resp = {}

    if data_resp.get("success"):
        _service().atualizar_job(job_id, status="concluido_salvo")

    return jsonify(data_resp)
