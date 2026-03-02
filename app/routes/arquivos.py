from flask import Blueprint, request, jsonify
from app.services.simulado_service import gerar_perguntas_huggingface
import json
import os

arquivos_bp = Blueprint('arquivos', __name__, url_prefix='/api/arquivos')

@arquivos_bp.route('/gerar-questoes', methods=['POST'])
def gerar_questoes():
    data = request.get_json()
    texto = data.get('texto', '')
    num_perguntas = int(data.get('num_perguntas', 3))
    if not texto.strip():
        return jsonify({'success': False, 'error': 'Texto não informado.'}), 400
    if num_perguntas < 1 or num_perguntas > 20:
        return jsonify({'success': False, 'error': 'Número de perguntas deve ser entre 1 e 20.'}), 400
    try:
        questoes_geradas = gerar_perguntas_huggingface(texto, num_perguntas)
        return jsonify({'success': True, 'questoes': questoes_geradas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@arquivos_bp.route('/salvar-questoes', methods=['POST'])
def salvar_questoes():
    data = request.get_json()
    questoes = data.get('questoes', [])
    capitulo = data.get('capitulo', 'importados')
    if not questoes or not isinstance(questoes, list):
        return jsonify({'success': False, 'error': 'Nenhuma questão recebida.'}), 400
    banco_path = 'banco_questoes.json'
    if os.path.exists(banco_path):
        with open(banco_path, 'r', encoding='utf-8') as f:
            banco = json.load(f)
    else:
        banco = {}
    if capitulo not in banco:
        banco[capitulo] = []
    banco[capitulo].extend(questoes)
    with open(banco_path, 'w', encoding='utf-8') as f:
        json.dump(banco, f, indent=2, ensure_ascii=False)
    return jsonify({'success': True, 'msg': f'{len(questoes)} questões salvas no capítulo {capitulo}.'})
