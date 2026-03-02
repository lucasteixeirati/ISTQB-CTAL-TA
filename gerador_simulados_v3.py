"""
ISTQB CTAL-TA - Gerador de Simulados v3.0

Este script é mantido para uso legado.
A logica de negocio para tracking foi centralizada em app/services/simulado_service.py.
"""

import random
import json
import os
from datetime import datetime
from collections import Counter
import time

from banco_questoes_completo import QUESTOES_DB
from app.services.simulado_service import salvar_no_tracking  # noqa: E402

def gerar_simulado(capitulo="todos", num_questoes=10, k_levels=None):
    """Retorna uma amostra aleatoria de questoes para o capitulo solicitado (e niveis K opcionais)."""
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

def executar_quiz_interativo(questoes, titulo, tag_tracking, tempo_limite_min=None):
    """Executa um quiz interativo e salva o progresso automaticamente"""
    print("\n" + "="*70)
    print(f"SIMULADO: {titulo}")
    print("="*70)
    print(f"Questoes: {len(questoes)}")
    if tempo_limite_min:
        print(f"Tempo limite: {tempo_limite_min} minutos")
    
    input("\nPressione ENTER para iniciar...")
    
    respostas_usuario = {}
    tempo_inicio = time.time()
    tempo_limite_seg = tempo_limite_min * 60 if tempo_limite_min else None
    
    for idx, q in enumerate(questoes, 1):
        tempo_decorrido = int((time.time() - tempo_inicio) / 60)
        
        header_tempo = ""
        if tempo_limite_min:
            tempo_restante = tempo_limite_min - tempo_decorrido
            header_tempo = f" | Tempo restante: {tempo_restante} min"
        
        print(f"\n{'='*70}")
        print(f"Questao {idx}/{len(questoes)}{header_tempo}")
        print(f"{'='*70}")
        print(f"\n({q['k_level']}) {q['pergunta']}\n")
        
        for letra, opcao in sorted(q['opcoes'].items()):
            print(f"{letra}) {opcao}")
        
        while True:
            resposta = input("\nSua resposta (A/B/C/D ou S para pular): ").strip().upper()
            if resposta in ['A', 'B', 'C', 'D', 'S']:
                if resposta != 'S':
                    respostas_usuario[idx] = resposta
                break
            print("Resposta invalida!")
        
        if tempo_limite_seg and (time.time() - tempo_inicio > tempo_limite_seg):
            print("\n\nTEMPO ESGOTADO!")
            break
    
    tempo_total = int((time.time() - tempo_inicio) / 60)
    
    # Calcular resultado
    acertos = sum(1 for idx, q in enumerate(questoes, 1) 
                  if respostas_usuario.get(idx) == q['resposta'])
    total = len(questoes)
    percentual = (acertos / total) * 100
    aprovado = percentual >= 65
    
    # Gerar relatorio HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_html = f"relatorio_{tag_tracking}_{timestamp}.html"
    gerar_relatorio_html(questoes, respostas_usuario, acertos, total, tempo_total, arquivo_html)
    
    # Salvar no tracking
    salvar_no_tracking(tag_tracking, total, acertos, tempo_total)
    
    # Mostrar resultado
    print("\n" + "="*70)
    print("SIMULADO FINALIZADO!")
    print("="*70)
    print(f"\nTempo total: {tempo_total} minutos")
    print(f"Resultado: {acertos}/{total} ({percentual:.1f}%)")
    print(f"Status: {'APROVADO' if aprovado else 'REPROVADO'} (minimo 65%)")
    print(f"\nRelatorio detalhado salvo em: {arquivo_html}")
    print("✅ Resultado registrado automaticamente no historico.")

def modo_exame_real():
    print("\n" + "="*70)
    print("MODO EXAME REAL - ISTQB CTAL-TA")
    print("="*70)
    print("\nSimulacao de exame oficial:")
    print("- 40 questoes")
    print("- 120 minutos (cronometrado)")
    print("- Sem consulta a material")
    
    questoes = gerar_simulado("todos", 40)
    executar_quiz_interativo(questoes, "Exame Oficial Simulado", "completo", 120)

def gerar_relatorio_html(questoes, respostas_usuario, acertos, total, tempo_minutos, arquivo):
    percentual = (acertos / total) * 100
    aprovado = percentual >= 65
    
    # Analise por capitulo
    por_capitulo = {}
    for idx, q in enumerate(questoes, 1):
        cap = identificar_capitulo(q['id'])
        if cap not in por_capitulo:
            por_capitulo[cap] = {'total': 0, 'acertos': 0}
        por_capitulo[cap]['total'] += 1
        if respostas_usuario.get(idx) == q['resposta']:
            por_capitulo[cap]['acertos'] += 1
    
    # Analise por K-level
    por_k = {}
    for idx, q in enumerate(questoes, 1):
        k = q['k_level']
        if k not in por_k:
            por_k[k] = {'total': 0, 'acertos': 0}
        por_k[k]['total'] += 1
        if respostas_usuario.get(idx) == q['resposta']:
            por_k[k]['acertos'] += 1
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatorio Exame ISTQB CTAL-TA</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .resultado {{ background: {'#27ae60' if aprovado else '#e74c3c'}; color: white; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center; }}
        .resultado h2 {{ margin: 0; font-size: 2em; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: #ecf0f1; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-card h3 {{ margin: 0 0 10px 0; color: #34495e; font-size: 0.9em; }}
        .stat-card .value {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #3498db; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .correto {{ color: #27ae60; font-weight: bold; }}
        .errado {{ color: #e74c3c; font-weight: bold; }}
        .questao {{ margin: 20px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #3498db; }}
        .opcoes {{ margin: 10px 0; }}
        .opcao {{ padding: 5px 10px; margin: 5px 0; }}
        .opcao.correta {{ background: #d4edda; border-left: 3px solid #28a745; }}
        .opcao.errada {{ background: #f8d7da; border-left: 3px solid #dc3545; }}
        .justificativa {{ background: #e8f4f8; padding: 10px; margin: 10px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Relatorio de Exame ISTQB CTAL-TA</h1>
        <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        
        <div class="resultado">
            <h2>{'APROVADO' if aprovado else 'REPROVADO'}</h2>
            <p style="font-size: 1.5em; margin: 10px 0;">{acertos}/{total} questoes ({percentual:.1f}%)</p>
            <p>Minimo para aprovacao: 65% (26/40)</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Tempo Total</h3>
                <div class="value">{tempo_minutos} min</div>
            </div>
            <div class="stat-card">
                <h3>Acertos</h3>
                <div class="value">{acertos}</div>
            </div>
            <div class="stat-card">
                <h3>Erros</h3>
                <div class="value">{total - acertos}</div>
            </div>
            <div class="stat-card">
                <h3>Percentual</h3>
                <div class="value">{percentual:.1f}%</div>
            </div>
        </div>
        
        <h2>Desempenho por Capitulo</h2>
        <table>
            <tr><th>Capitulo</th><th>Acertos</th><th>Total</th><th>%</th></tr>
"""
    
    for cap, stats in sorted(por_capitulo.items()):
        perc = (stats['acertos'] / stats['total']) * 100
        html += f"<tr><td>{cap}</td><td>{stats['acertos']}</td><td>{stats['total']}</td><td>{perc:.1f}%</td></tr>\n"
    
    html += """
        </table>
        
        <h2>Desempenho por Nivel K</h2>
        <table>
            <tr><th>Nivel</th><th>Acertos</th><th>Total</th><th>%</th></tr>
"""
    
    for k, stats in sorted(por_k.items()):
        perc = (stats['acertos'] / stats['total']) * 100
        html += f"<tr><td>{k}</td><td>{stats['acertos']}</td><td>{stats['total']}</td><td>{perc:.1f}%</td></tr>\n"
    
    html += """
        </table>
        
        <h2>Revisao Detalhada das Questoes</h2>
"""
    
    for idx, q in enumerate(questoes, 1):
        resposta_user = respostas_usuario.get(idx, 'N/A')
        correto = resposta_user == q['resposta']
        
        html += f"""
        <div class="questao">
            <h3>Questao {idx} ({q['k_level']}) - {'<span class="correto">CORRETO</span>' if correto else '<span class="errado">ERRADO</span>'}</h3>
            <p><strong>{q['pergunta']}</strong></p>
            <div class="opcoes">
"""
        
        for letra, opcao in sorted(q['opcoes'].items()):
            classe = ''
            if letra == q['resposta']:
                classe = 'correta'
            elif letra == resposta_user and not correto:
                classe = 'errada'
            
            html += f'<div class="opcao {classe}">{letra}) {opcao}</div>\n'
        
        html += f"""
            </div>
            <p><strong>Sua resposta:</strong> {resposta_user} | <strong>Resposta correta:</strong> {q['resposta']}</p>
            <div class="justificativa">
                <strong>Justificativa:</strong> {q['justificativa']}
            </div>
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(html)

def identificar_capitulo(id_questao):
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

def analisar_pontos_fracos():
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

def modo_recuperacao():
    print("\n" + "="*70)
    print("MODO RECUPERACAO - FOCO EM PONTOS FRACOS")
    print("="*70)
    
    fracos = analisar_pontos_fracos()
    
    if not fracos:
        print("\nNao foram identificados pontos fracos claros (< 70%) baseados no seu historico")
        print("de simulados por capitulo.")
        print("\nDica: Faca simulados especificos por capitulo para alimentar o historico.")
        return

    print(f"\nCapitulos identificados para reforco (< 70% de aproveitamento):")
    for cap in fracos:
        print(f" - {cap}")
    
    questoes_pool = []
    for cap in fracos:
        questoes_pool.extend(QUESTOES_DB.get(cap, []))
    
    if not questoes_pool:
        print("\nErro: Nenhuma questao encontrada no banco para os capitulos selecionados.")
        return

    print(f"\nTotal de questoes disponiveis nesses topicos: {len(questoes_pool)}")
    num_questoes = input(f"Quantas questoes deseja gerar? (max {len(questoes_pool)}): ").strip()
    
    try:
        num_questoes = int(num_questoes)
        if num_questoes > 0:
            questoes = random.sample(questoes_pool, min(num_questoes, len(questoes_pool)))
            
            executar_quiz_interativo(questoes, "Recuperacao (Foco em Pontos Fracos)", "recuperacao")
    except ValueError:
        print("Digite um numero valido!")

def menu_principal():
    print("\n" + "="*70)
    print("GERADOR DE SIMULADOS ISTQB CTAL-TA v3.0")
    print("="*70)
    
    while True:
        print("\nMENU PRINCIPAL:")
        print("1. MODO EXAME REAL (40 questoes, 120min, cronometrado)")
        print("2. Gerar simulado por capitulo")
        print("3. Gerar simulado completo")
        print("4. Gerar simulado por nivel K")
        print("5. Gerar simulado de RECUPERACAO (Foco em pontos fracos)")
        print("6. Ver estatisticas do banco")
        print("7. Sair")
        
        escolha = input("\nEscolha uma opcao (1-7): ").strip()
        
        if escolha == "1":
            modo_exame_real()
        elif escolha == "2":
            menu_por_capitulo()
        elif escolha == "3":
            menu_completo()
        elif escolha == "4":
            menu_por_k_level()
        elif escolha == "5":
            modo_recuperacao()
        elif escolha == "6":
            estatisticas_banco()
        elif escolha == "7":
            print("\nAte logo! Bons estudos!")
            break
        else:
            print("Opcao invalida!")

def menu_por_capitulo():
    print("\nCAPITULOS DISPONIVEIS:")
    capitulos = {
        "1": ("cap1_risk", "Risk-Based Testing"),
        "2": ("cap2_techniques", "Test Techniques"),
        "3": ("cap3_quality", "Quality Characteristics"),
        "4": ("cap4_reviews", "Reviews"),
        "5": ("cap5_tools", "Test Tools")
    }
    
    for num, (cap_id, cap_nome) in capitulos.items():
        num_questoes = len(QUESTOES_DB.get(cap_id, []))
        print(f"{num}. {cap_nome} ({num_questoes} questoes)")
    
    escolha = input("\nEscolha o capitulo (1-5): ").strip()
    
    if escolha in capitulos:
        cap_id, cap_nome = capitulos[escolha]
        num_max = len(QUESTOES_DB.get(cap_id, []))
        
        num_questoes = input(f"\nQuantas questoes? (max {num_max}): ").strip()
        try:
            num_questoes = int(num_questoes)
            if num_questoes > 0:
                questoes = gerar_simulado(cap_id, num_questoes)
                executar_quiz_interativo(questoes, f"Capitulo: {cap_nome}", cap_id)
        except ValueError:
            print("Digite um numero valido!")

def menu_completo():
    total_questoes = sum(len(q) for q in QUESTOES_DB.values())
    
    print(f"\nSIMULADO COMPLETO (max {total_questoes} questoes)")
    num_questoes = input(f"Quantas questoes? (recomendado: 40): ").strip()
    
    try:
        num_questoes = int(num_questoes)
        if num_questoes > 0:
            questoes = gerar_simulado("todos", num_questoes)
            executar_quiz_interativo(questoes, "Simulado Completo (Mix)", "completo")
    except ValueError:
        print("Digite um numero valido!")

def menu_por_k_level():
    print("\nNIVEIS K DISPONIVEIS:")
    print("1. K2 (Conhecimento)")
    print("2. K3 (Aplicacao)")
    print("3. K4 (Analise)")
    print("4. Mix (K2+K3+K4)")
    
    escolha = input("\nEscolha o nivel (1-4): ").strip()
    
    k_map = {
        "1": ["K2"],
        "2": ["K3"],
        "3": ["K4"],
        "4": ["K2", "K3", "K4"]
    }
    
    if escolha in k_map:
        k_levels = k_map[escolha]
        
        num_questoes = input("\nQuantas questoes? (recomendado: 20): ").strip()
        try:
            num_questoes = int(num_questoes)
            if num_questoes > 0:
                questoes = gerar_simulado("todos", num_questoes, k_levels)
                executar_quiz_interativo(questoes, f"Nivel K: {'+'.join(k_levels)}", "completo")
        except ValueError:
            print("Digite um numero valido!")

def estatisticas_banco():
    total = sum(len(questoes) for questoes in QUESTOES_DB.values())
    
    print("\n" + "="*70)
    print("ESTATISTICAS DO BANCO DE QUESTOES")
    print("="*70)
    print(f"\nTotal de questoes: {total}")
    print("\nPor capitulo:")
    for cap, questoes in QUESTOES_DB.items():
        print(f"  {cap}: {len(questoes)} questoes")
    
    todas_questoes = []
    for questoes in QUESTOES_DB.values():
        todas_questoes.extend(questoes)
    
    k_levels = Counter(q['k_level'] for q in todas_questoes)
    print("\nPor nivel K:")
    for k, count in sorted(k_levels.items()):
        print(f"  {k}: {count} questoes ({count/total*100:.1f}%)")

if __name__ == "__main__":
    menu_principal()
