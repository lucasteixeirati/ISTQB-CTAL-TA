from flask import Blueprint, request, jsonify
from app.services.simulado_service import gerar_perguntas_huggingface
from app.utils.validacao import verificar_duplicatas_banco
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
    
    banco_path = 'questoes_banco.json'
    if os.path.exists(banco_path):
        with open(banco_path, 'r', encoding='utf-8') as f:
            banco = json.load(f)
    else:
        banco = {'questoes': {}}
    
    # Garante estrutura correta
    if 'questoes' not in banco:
        banco['questoes'] = {}
    
    # Verifica duplicatas antes de salvar
    questoes_unicas, questoes_duplicadas, estatisticas = verificar_duplicatas_banco(
        questoes_novas=questoes,
        banco_atual=banco,
        threshold_similaridade=0.95
    )
    
    # Salva apenas questões únicas
    if capitulo not in banco['questoes']:
        banco['questoes'][capitulo] = []
    
    banco['questoes'][capitulo].extend(questoes_unicas)
    
    with open(banco_path, 'w', encoding='utf-8') as f:
        json.dump(banco, f, indent=2, ensure_ascii=False)
    
    # Resposta com informações de duplicatas
    msg_parts = []
    if len(questoes_unicas) > 0:
        msg_parts.append(f'{len(questoes_unicas)} questões salvas no capítulo {capitulo}')
    if len(questoes_duplicadas) > 0:
        msg_parts.append(f'{len(questoes_duplicadas)} questões duplicadas foram ignoradas')
    
    msg = '. '.join(msg_parts) + '.'
    
    return jsonify({
        'success': True,
        'msg': msg,
        'estatisticas': {
            'salvas': len(questoes_unicas),
            'duplicadas': len(questoes_duplicadas),
            'total_analisadas': len(questoes)
        },
        'questoes_duplicadas': [
            {
                'pergunta': q['pergunta'][:100] + '...' if len(q.get('pergunta', '')) > 100 else q.get('pergunta', ''),
                'similaridade': q.get('_duplicata_info', {}).get('similaridade', 0)
            }
            for q in questoes_duplicadas[:5]  # Retorna no máximo 5 exemplos
        ] if questoes_duplicadas else []
    })

