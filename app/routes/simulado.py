from flask import Blueprint, jsonify, request
from app.services.simulado_service import gerar_simulado

simulado_bp = Blueprint('simulado', __name__, url_prefix='/simulado')

@simulado_bp.route('/', methods=['GET'])
def get_simulados():
    """Endpoint para gerar um simulado. Parâmetros opcionais: capitulo, num_questoes, k_levels"""
    capitulo = request.args.get('capitulo', 'todos')
    num_questoes = int(request.args.get('num_questoes', 10))
    k_levels = request.args.getlist('k_levels') or None
    questoes = gerar_simulado(capitulo, num_questoes, k_levels)
    # Remover respostas corretas do retorno para não expor via API
    for q in questoes:
        q.pop('resposta', None)
    return jsonify({'questoes': questoes})
