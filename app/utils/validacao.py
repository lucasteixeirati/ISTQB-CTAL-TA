"""
Módulo de validação de questões - detecção de duplicatas
"""
from difflib import SequenceMatcher
from typing import List, Dict, Tuple


def normalizar_texto(texto: str) -> str:
    """Normaliza texto para comparação (lowercase, sem espaços extras)."""
    return texto.strip().lower()


def calcular_similaridade(texto1: str, texto2: str) -> float:
    """Calcula similaridade entre dois textos usando SequenceMatcher."""
    texto1_norm = normalizar_texto(texto1)
    texto2_norm = normalizar_texto(texto2)
    return SequenceMatcher(None, texto1_norm, texto2_norm).ratio()


def verificar_duplicatas_banco(
    questoes_novas: List[Dict],
    banco_atual: Dict,
    threshold_similaridade: float = 0.95
) -> Tuple[List[Dict], List[Dict], Dict]:
    """
    Verifica duplicatas entre questões novas e o banco existente.
    
    Args:
        questoes_novas: Lista de questões a serem verificadas
        banco_atual: Dicionário com a estrutura do banco (questoes: {cap1:[], cap2:[], ...})
        threshold_similaridade: Limite de similaridade para considerar duplicata (0.0 a 1.0)
    
    Returns:
        Tupla contendo:
        - questoes_unicas: Lista de questões únicas (não duplicadas)
        - questoes_duplicadas: Lista de questões que são duplicatas
        - estatisticas: Dicionário com estatísticas da verificação
    """
    questoes_unicas = []
    questoes_duplicadas = []
    
    # Extrai todas as perguntas existentes no banco
    perguntas_banco = []
    if 'questoes' in banco_atual:
        for capitulo, questoes in banco_atual['questoes'].items():
            if isinstance(questoes, list):
                for q in questoes:
                    if isinstance(q, dict) and 'pergunta' in q:
                        perguntas_banco.append(q['pergunta'])
    
    # Verifica cada questão nova
    for questao_nova in questoes_novas:
        if not isinstance(questao_nova, dict):
            continue
            
        pergunta_nova = questao_nova.get('pergunta', '')
        if not pergunta_nova:
            continue
        
        # Verifica similaridade com todas as perguntas do banco
        eh_duplicata = False
        duplicata_info = None
        
        for pergunta_existente in perguntas_banco:
            similaridade = calcular_similaridade(pergunta_nova, pergunta_existente)
            
            if similaridade >= threshold_similaridade:
                eh_duplicata = True
                duplicata_info = {
                    'pergunta_nova': pergunta_nova,
                    'pergunta_existente': pergunta_existente,
                    'similaridade': round(similaridade, 3)
                }
                break
        
        if eh_duplicata:
            questoes_duplicadas.append({
                **questao_nova,
                '_duplicata_info': duplicata_info
            })
        else:
            questoes_unicas.append(questao_nova)
            # Adiciona à lista de perguntas para evitar duplicatas dentro do próprio lote
            perguntas_banco.append(pergunta_nova)
    
    # Estatísticas
    estatisticas = {
        'total_analisadas': len(questoes_novas),
        'questoes_unicas': len(questoes_unicas),
        'questoes_duplicadas': len(questoes_duplicadas),
        'threshold_usado': threshold_similaridade
    }
    
    return questoes_unicas, questoes_duplicadas, estatisticas
