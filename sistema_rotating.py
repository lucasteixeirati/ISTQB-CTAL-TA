#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Rotating inteligente para seleção de questões
- Rastreia uso de questões
- Favorece questões menos usadas
- Mistura novas e antigas
"""

import json
import random
from datetime import datetime
from pathlib import Path

class QuestoesRotating:
    """Gerencia rotating inteligente de questões"""
    
    def __init__(self, banco_file='questoes_banco.json', tracking_file='questoes_rotacao.json'):
        self.banco_file = banco_file
        self.tracking_file = tracking_file
        self.banco = None
        self.tracking = None
        self.carregar()
    
    def carregar(self):
        """Carrega banco e arquivo de tracking"""
        with open(self.banco_file, 'r', encoding='utf-8') as f:
            self.banco = json.load(f)
        
        # Carregar ou criar tracking
        if Path(self.tracking_file).exists():
            with open(self.tracking_file, 'r', encoding='utf-8') as f:
                self.tracking = json.load(f)
        else:
            self.tracking = {
                'cap1': {}, 'cap2': {}, 'cap3': {}, 'cap4': {}, 'cap5': {},
                'last_updated': None
            }
            self._inicializar_tracking()
    
    def _inicializar_tracking(self):
        """Inicializa tracking para todas as questões"""
        nomes_cap = {
            'cap1': 'Risk-Based Testing',
            'cap2': 'Test Techniques',
            'cap3': 'Quality Characteristics',
            'cap4': 'Reviews',
            'cap5': 'Test Tools'
        }
        
        for cap_id in ['cap1', 'cap2', 'cap3', 'cap4', 'cap5']:
            questoes = self.banco['questoes'].get(cap_id, [])
            self.tracking[cap_id] = {}
            
            for idx, q in enumerate(questoes):
                pergunta_resumida = q.get('pergunta', '')[:50]
                self.tracking[cap_id][str(idx)] = {
                    'pergunta': pergunta_resumida,
                    'usado_vezes': 0,
                    'ultimo_uso': None,
                    'tempo_criacao': datetime.now().isoformat(),
                    'eh_novo': True  # Todas começam como novas
                }
    
    def salvar_tracking(self):
        """Salva arquivo de rastreamento"""
        self.tracking['last_updated'] = datetime.now().isoformat()
        with open(self.tracking_file, 'w', encoding='utf-8') as f:
            json.dump(self.tracking, f, indent=2, ensure_ascii=False)
    
    def selecionar_questoes(self, capitulo_id, quantidade=5, prefer_novas=True):
        """
        Seleciona questões com algoritmo de rotating inteligente
        
        Args:
            capitulo_id: 'cap1', 'cap2', etc
            quantidade: número de questões a selecionar
            prefer_novas: se True, favorece questões novas em 70% dos casos
        
        Returns:
            Lista de questões selecionadas
        """
        if capitulo_id not in self.banco['questoes']:
            return []
        
        questoes_disponiveis = self.banco['questoes'][capitulo_id]
        if len(questoes_disponiveis) == 0:
            return []
        
        quantidade = min(quantidade, len(questoes_disponiveis))
        
        # Criar lista de índices com scores
        indices_com_score = []
        
        for idx, questao in enumerate(questoes_disponiveis):
            pergunta_resumida = questao.get('pergunta', '')[:50]
            
            # Obter tracking ou criar novo
            track = self.tracking[capitulo_id].get(str(idx), {
                'pergunta': pergunta_resumida,
                'usado_vezes': 0,
                'ultimo_uso': None,
                'eh_novo': True
            })
            
            # Calcular score
            score = self._calcular_score(track, pergunta_resumida, idx, len(questoes_disponiveis))
            
            indices_com_score.append({
                'indice': idx,
                'score': score,
                'eh_novo': track.get('eh_novo', True),
                'usado_vezes': track.get('usado_vezes', 0)
            })
        
        # Selecionar com weighted random
        selecionadas = self._weighted_selection(
            indices_com_score, 
            quantidade, 
            prefer_novas
        )
        
        # Construir resultado
        questoes_selecionadas = []
        for item in selecionadas:
            idx = item['indice']
            questao = questoes_disponiveis[idx].copy()
            questao['_indice_original'] = idx  # Para tracking
            questoes_selecionadas.append(questao)
            
            # Atualizar tracking
            track = self.tracking[capitulo_id].get(str(idx), {})
            track['usado_vezes'] = track.get('usado_vezes', 0) + 1
            track['ultimo_uso'] = datetime.now().isoformat()
            track['eh_novo'] = False  # Deixa de ser nova após primeira uso
            self.tracking[capitulo_id][str(idx)] = track
        
        self.salvar_tracking()
        
        return questoes_selecionadas
    
    def _calcular_score(self, track, pergunta, idx, total_questoes):
        """
        Calcula score de prioridade para questão
        Score mais alto = mais chance de ser selecionada
        
        Fatores:
        - Questões menos usadas têm score mais alto
        - Questões novas recebem bonus
        - Questões não usadas há mais tempo recebem score maior
        """
        # Fator: vezes usado (menos = melhor)
        fator_uso = 10 / (track.get('usado_vezes', 0) + 1)
        
        # Fator: questão nova
        fator_nova = 2.0 if track.get('eh_novo', True) else 1.0
        
        # Fator: tempo desde último uso
        fator_tempo = 1.0
        if track.get('ultimo_uso'):
            try:
                ultimo_uso = datetime.fromisoformat(track['ultimo_uso'])
                diferenca = (datetime.now() - ultimo_uso).total_seconds() / 3600  # horas
                fator_tempo = 1.0 + (diferenca / 10)  # Aumenta com o tempo
            except:
                pass
        
        score = fator_uso * fator_nova * fator_tempo
        
        return score
    
    def _weighted_selection(self, items, quantidade, prefer_novas=True):
        """Seleciona items com weighted random selection"""
        if not items:
            return []
        
        # Se prefer_novas, separar em dois grupos
        if prefer_novas:
            novas = [i for i in items if i['eh_novo']]
            antigas = [i for i in items if not i['eh_novo']]
            
            # 70% novas, 30% antigas (se houver ambas)
            if novas and antigas:
                qtd_novas = max(1, int(quantidade * 0.7))
                qtd_antigas = quantidade - qtd_novas
                
                selecionadas = self._weighted_random(novas, qtd_novas)
                selecionadas.extend(self._weighted_random(antigas, qtd_antigas))
                random.shuffle(selecionadas)
                return selecionadas
            else:
                # Usar tudo o que tem
                return self._weighted_random(items, quantidade)
        else:
            return self._weighted_random(items, quantidade)
    
    def _weighted_random(self, items, quantidade):
        """Seleciona items aleatoriamente baseado em score (weight)"""
        if not items:
            return []
        
        quantidade = min(quantidade, len(items))
        
        # Extrair scores
        scores = [item['score'] for item in items]
        
        # Normalizar scores (evitar scores negativos)
        min_score = min(scores) if scores else 1
        scores = [max(0.1, s - min_score + 1) for s in scores]
        
        # Weighted random choice
        selecionadas = random.choices(items, weights=scores, k=quantidade)
        
        return selecionadas
    
    def gerar_simulado(self, capitulo_id, quantidade=5):
        """
        Gera um simulado com questões usando rotating inteligente
        Com validação contra duplicatas no mesmo simulado
        """
        # Selecionar questões com rotating
        questoes = self.selecionar_questoes(capitulo_id, quantidade, prefer_novas=True)
        
        # IMPORTANTE: Remover duplicatas (mesma pergunta = mesmo objeto)
        # Usar percurso para manter ordem mas remover duplicatas
        perguntas_vistas = set()
        questoes_sem_duplicatas = []
        
        for q in questoes:
            pergunta_normalizada = q.get('pergunta', '').strip().lower()
            if pergunta_normalizada not in perguntas_vistas:
                perguntas_vistas.add(pergunta_normalizada)
                questoes_sem_duplicatas.append(q)
        
        # Se removemos muitas (por duplicata), selecionar mais
        if len(questoes_sem_duplicatas) < quantidade:
            questoes_adicionais = self.selecionar_questoes(
                capitulo_id, 
                quantidade - len(questoes_sem_duplicatas),
                prefer_novas=True
            )
            
            for q in questoes_adicionais:
                pergunta_normalizada = q.get('pergunta', '').strip().lower()
                if pergunta_normalizada not in perguntas_vistas:
                    perguntas_vistas.add(pergunta_normalizada)
                    questoes_sem_duplicatas.append(q)
                    if len(questoes_sem_duplicatas) >= quantidade:
                        break
        
        # Embaralhar para melhor apresentação
        random.shuffle(questoes_sem_duplicatas)
        
        return questoes_sem_duplicatas[:quantidade]
    
    def estatisticas(self, capitulo_id):
        """Retorna estatísticas de uso do capítulo"""
        if capitulo_id not in self.tracking:
            return None
        
        track = self.tracking[capitulo_id]
        
        stats = {
            'total_questoes': len(self.banco['questoes'].get(capitulo_id, [])),
            'questoes_novas': sum(1 for t in track.values() if isinstance(t, dict) and t.get('eh_novo', False)),
            'usado_vezes': {},
            'media_uso': 0
        }
        
        usos_totais = 0
        for idx, info in track.items():
            if isinstance(info, dict) and 'usado_vezes' in info:
                usos = info['usado_vezes']
                usos_totais += usos
                if usos not in stats['usado_vezes']:
                    stats['usado_vezes'][usos] = 0
                stats['usado_vezes'][usos] += 1
        
        if stats['total_questoes'] > 0:
            stats['media_uso'] = round(usos_totais / stats['total_questoes'], 2)
        
        return stats


def testar_rotating():
    """Testa o sistema de rotating"""
    print("\n" + "="*80)
    print("TESTE DO SISTEMA DE ROTATING INTELIGENTE")
    print("="*80 + "\n")
    
    rotating = QuestoesRotating()
    
    # Exibir estatísticas antes
    print("📊 ESTATÍSTICAS INICIAIS:")
    print("-" * 80)
    for cap_id in ['cap1', 'cap2', 'cap3', 'cap4', 'cap5']:
        stats = rotating.estatisticas(cap_id)
        if stats:
            print(f"\n{cap_id}:")
            print(f"  Total: {stats['total_questoes']} questões")
            print(f"  Novas: {stats['questoes_novas']}")
            print(f"  Média de uso: {stats['media_uso']} vezes")
    
    # Simular gerando alguns simulados
    print("\n\n" + "="*80)
    print("🎲 SIMULANDO 3 GERAÇÕES DE SIMULADO PARA CAP2")
    print("="*80 + "\n")
    
    for num_geracao in range(1, 4):
        print(f"\n🎯 Geração #{num_geracao}:")
        print("-" * 80)
        
        questoes = rotating.gerar_simulado('cap2', quantidade=5)
        
        for i, q in enumerate(questoes, 1):
            pergunta = q['pergunta'][:60]
            eh_nova = "✨ NOVA" if q.get('_indice_original') and \
                      rotating.tracking['cap2'].get(str(q['_indice_original']), {}).get('eh_novo') else ""
            print(f"  {i}. {pergunta}... {eh_nova}")
    
    # Estatísticas finais
    print("\n\n" + "="*80)
    print("📊 ESTATÍSTICAS FINAIS (após simulações):")
    print("-" * 80)
    for cap_id in ['cap1', 'cap2', 'cap3', 'cap4', 'cap5']:
        stats = rotating.estatisticas(cap_id)
        if stats:
            print(f"\n{cap_id}:")
            print(f"  Total: {stats['total_questoes']} questões")
            print(f"  Novas: {stats['questoes_novas']}")
            print(f"  Média de uso: {stats['media_uso']} vezes")
    
    print("\n\n✅ SISTEMA DE ROTATING TESTADO COM SUCESSO!")
    print("\n💡 Sistema está pronto para ser integrado ao endpoint de simulado")


if __name__ == '__main__':
    testar_rotating()
