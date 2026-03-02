"""Serviço de persistência e manipulação de jobs de geração.

Armazena jobs em um arquivo JSON (por padrão, `geracoes_questoes.json`).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class GeracoesService:
    geracoes_file: str

    def carregar(self) -> dict[str, Any]:
        if os.path.exists(self.geracoes_file):
            with open(self.geracoes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"jobs": []}

    def salvar(self, dados: dict[str, Any]) -> None:
        with open(self.geracoes_file, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def criar_job(
        self,
        arquivo: dict[str, Any],
        num_questoes: int,
        provider: str,
        capitulo_id: str = "importados",
        capitulo_nome: str = "Importados / Outros",
    ) -> dict[str, Any]:
        dados = self.carregar()
        now = datetime.now()
        job_id = now.strftime("%Y%m%d_%H%M%S_") + str(len(dados.get("jobs", [])) + 1)
        job = {
            "id": job_id,
            "arquivo_id": arquivo["id"],
            "arquivo_nome": arquivo.get("nome"),
            "provider": provider,
            "num_questoes": num_questoes,
            "capitulo_id": capitulo_id,
            "capitulo_nome": capitulo_nome,
            "status": "pendente",
            "erro_msg": None,
            "criado_em": now.strftime("%Y-%m-%d %H:%M:%S"),
            "atualizado_em": now.strftime("%Y-%m-%d %H:%M:%S"),
            "questoes": [],
        }
        dados.setdefault("jobs", []).append(job)
        self.salvar(dados)
        return job

    def atualizar_job(self, job_id: str, **kwargs: Any) -> dict[str, Any] | None:
        dados = self.carregar()
        for job in dados.get("jobs", []):
            if job.get("id") == job_id:
                job.update(kwargs)
                job["atualizado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.salvar(dados)
                return job
        return None

    def buscar_job(self, job_id: str) -> dict[str, Any] | None:
        dados = self.carregar()
        return next((j for j in dados.get("jobs", []) if j.get("id") == job_id), None)

    def listar_jobs_resumo(self) -> list[dict[str, Any]]:
        dados = self.carregar()
        return [
            {
                "id": j["id"],
                "arquivo_nome": j.get("arquivo_nome"),
                "provider": j.get("provider"),
                "num_questoes": j.get("num_questoes"),
                "capitulo_id": j.get("capitulo_id"),
                "capitulo_nome": j.get("capitulo_nome"),
                "status": j.get("status"),
                "criado_em": j.get("criado_em"),
                "atualizado_em": j.get("atualizado_em"),
            }
            for j in dados.get("jobs", [])
        ]
