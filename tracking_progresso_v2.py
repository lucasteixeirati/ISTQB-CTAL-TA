"""\
ISTQB CTAL-TA - Tracking utilities (CLI / legacy)

This module contains utilities used by the CLI dashboard scripts.
The web app uses its own endpoints and service-layer logging.

Note:
    There is overlapping functionality with app/services/simulado_service.py.
    Prefer keeping the web-facing tracking logic centralized in the service layer.
"""

"""
ISTQB CTAL-TA - Sistema de Tracking v2.0
- Dashboard visual com graficos
- Analise por tecnica de teste
- Recomendacoes inteligentes
- Exportar relatorios PDF
"""

import json
import os
from datetime import datetime
from collections import defaultdict

TRACKING_FILE = "progresso_simulados.json"


def carregar_progresso():
    """Load the tracking JSON file from disk."""
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"simulados": []}


def salvar_progresso(dados):
    """Persist tracking data to disk (JSON)."""
    with open(TRACKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def registrar_simulado(capitulo, total_questoes, acertos, tempo_minutos=None):
    """Register a completed simulation attempt into the tracking dataset."""
    dados = carregar_progresso()
    
    resultado = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "capitulo": capitulo,
        "total_questoes": total_questoes,
        "acertos": acertos,
        "percentual": round((acertos / total_questoes) * 100, 1),
        "tempo_minutos": tempo_minutos,
        "aprovado": acertos >= (total_questoes * 0.65)
    }
    
    dados["simulados"].append(resultado)
    salvar_progresso(dados)
    
    print(f"\nResultado registrado!")
    print(f"Pontuacao: {acertos}/{total_questoes} ({resultado['percentual']}%)")
    print(f"{'APROVADO' if resultado['aprovado'] else 'REPROVADO'} (minimo 65%)")


def calcular_xp_simulado(sim):
    """Compute XP based on effort (questions) and performance (correct answers)."""
    xp = sim['total_questoes'] * 10  # 10 XP por questao (esforco)
    xp += sim['acertos'] * 20        # 20 XP por acerto (precisao)
    if sim['aprovado']:
        xp += 100                    # 100 XP bonus aprovacao
    if sim['percentual'] == 100 and sim['total_questoes'] >= 5:
        xp += 300                    # 300 XP bonus gabarito (apenas simulados > 5 questoes)
    return xp


def get_gamification_status(simulados):
    """Aggregate XP and return current/next level thresholds."""
    xp_total = sum(calcular_xp_simulado(s) for s in simulados)
    
    niveis = [
        (0, "Junior Tester"),
        (1000, "Test Analyst"),
        (3000, "Senior Analyst"),
        (6000, "Test Manager"),
        (12000, "ISTQB Master"),
        (25000, "Legendary Tester")
    ]
    
    atual = niveis[0]
    proximo = niveis[-1]
    
    for i, (req, titulo) in enumerate(niveis):
        if xp_total >= req:
            atual = (req, titulo)
            if i + 1 < len(niveis):
                proximo = niveis[i+1]
            else:
                proximo = (xp_total, "Max Level")
        else:
            break
            
    return xp_total, atual, proximo


def dashboard_visual():
    """Render an ASCII dashboard view for the tracking data (CLI)."""
    dados = carregar_progresso()
    simulados = dados.get("simulados", [])
    
    if not simulados:
        print("\nNenhum simulado registrado ainda.")
        return
    
    print("\n" + "="*80)
    print("DASHBOARD DE PROGRESSO")
    print("="*80)
    
    # Gamification Header
    xp_total, nivel_atual, nivel_proximo = get_gamification_status(simulados)
    req_atual = nivel_atual[0]
    req_prox = nivel_proximo[0]
    
    if req_prox != "Max Level":
        progresso_nivel = min(1.0, (xp_total - req_atual) / (req_prox - req_atual)) if req_prox > req_atual else 1.0
        barra_xp = '#' * int(progresso_nivel * 40)
        vazio_xp = '-' * (40 - len(barra_xp))
        print(f"\n🏆 NIVEL: {nivel_atual[1].upper()}")
        print(f"⭐ XP: {xp_total} / {req_prox}")
        print(f"   [{barra_xp}{vazio_xp}] {int(progresso_nivel*100)}%")
    else:
        print(f"\n🏆 NIVEL: {nivel_atual[1].upper()} (MAX)")
        print(f"⭐ XP: {xp_total}")

    # Estatisticas gerais
    total_simulados = len(simulados)
    total_questoes = sum(s['total_questoes'] for s in simulados)
    total_acertos = sum(s['acertos'] for s in simulados)
    media_geral = round((total_acertos / total_questoes) * 100, 1)
    aprovados = sum(1 for s in simulados if s['aprovado'])
    
    print(f"\nRESUMO GERAL:")
    print(f"  Total de simulados: {total_simulados}")
    print(f"  Total de questoes: {total_questoes}")
    print(f"  Media geral: {media_geral}%")
    print(f"  Taxa de aprovacao: {aprovados}/{total_simulados} ({round(aprovados/total_simulados*100, 1)}%)")
    
    # Grafico ASCII de evolucao
    print(f"\nEVOLUCAO (ultimos 10 simulados):")
    ultimos = simulados[-10:]
    max_perc = max(s['percentual'] for s in ultimos)
    
    for s in ultimos:
        data_curta = s['data'].split()[0]
        barra = '#' * int((s['percentual'] / 100) * 50)
        print(f"  {data_curta} [{s['percentual']:5.1f}%] {barra}")
    
    # Analise por capitulo
    por_capitulo = defaultdict(lambda: {"total": 0, "acertos": 0, "simulados": 0})
    
    for sim in simulados:
        cap = sim['capitulo']
        por_capitulo[cap]['total'] += sim['total_questoes']
        por_capitulo[cap]['acertos'] += sim['acertos']
        por_capitulo[cap]['simulados'] += 1
    
    print(f"\nDESEMPENHO POR CAPITULO:")
    for cap, stats in sorted(por_capitulo.items()):
        media = round((stats['acertos'] / stats['total']) * 100, 1)
        barra = '#' * int((media / 100) * 30)
        status = "OK" if media >= 70 else "REVISAR"
        print(f"  {cap:30s} [{media:5.1f}%] {barra} ({status})")
    
    # Identificar pontos fracos
    pontos_fracos = [(cap, stats) for cap, stats in por_capitulo.items() 
                     if (stats['acertos'] / stats['total']) < 0.70]
    
    if pontos_fracos:
        print(f"\nPONTOS FRACOS (< 70%):")
        for cap, stats in pontos_fracos:
            media = round((stats['acertos'] / stats['total']) * 100, 1)
            print(f"  - {cap} ({media}%)")
    
    # Recomendacoes inteligentes
    print(f"\nRECOMENDACOES INTELIGENTES:")
    
    if media_geral >= 80:
        print("  EXCELENTE! Voce esta pronto para o exame.")
        print("  - Faca mais 2-3 simulados completos para manter o ritmo")
        print("  - Revise apenas os topicos que errou")
        print("  - Agende o exame!")
    elif media_geral >= 65:
        print("  BOM! Mais 2 semanas de estudo recomendadas.")
        print("  - Foque nos capitulos com < 70%")
        print("  - Refaca simulados ate atingir 80%+")
        print("  - Revise flashcards dos topicos fracos")
    else:
        print("  ATENCAO! Estudo intensivo necessario.")
        print("  - Releia o syllabus completo")
        print("  - Estude todos os flashcards (189 cards)")
        print("  - Refaca todos os simulados")
        print("  - Nao agende o exame ainda")
    
    # Analise de tendencia
    if len(simulados) >= 3:
        ultimos_3 = [s['percentual'] for s in simulados[-3:]]
        if ultimos_3[-1] > ultimos_3[0]:
            print(f"\n  TENDENCIA: Melhorando! (+{ultimos_3[-1] - ultimos_3[0]:.1f}%)")
        elif ultimos_3[-1] < ultimos_3[0]:
            print(f"\n  TENDENCIA: Piorando! ({ultimos_3[-1] - ultimos_3[0]:.1f}%)")
        else:
            print(f"\n  TENDENCIA: Estavel")


def analise_por_tecnica():
    print("\n" + "="*80)
    print("ANALISE POR TECNICA DE TESTE")
    print("="*80)
    
    print("\nEsta funcionalidade requer dados detalhados de cada questao.")
    print("Baseado nos capitulos testados:\n")
    
    tecnicas = {
        "cap2_techniques": [
            "Equivalence Partitioning (EP)",
            "Boundary Value Analysis (BVA)",
            "Decision Tables",
            "State Transition Testing",
            "Use Case Testing",
            "Classification Trees",
            "Statement Coverage",
            "Branch Coverage",
            "Error Guessing",
            "Exploratory Testing"
        ]
    }
    
    dados = carregar_progresso()
    simulados = dados.get("simulados", [])
    
    cap2_simulados = [s for s in simulados if 'cap2' in s['capitulo'].lower() or 'technique' in s['capitulo'].lower()]
    
    if cap2_simulados:
        total = sum(s['total_questoes'] for s in cap2_simulados)
        acertos = sum(s['acertos'] for s in cap2_simulados)
        media = round((acertos / total) * 100, 1)
        
        print(f"Cap 2 (Test Techniques): {acertos}/{total} ({media}%)")
        print("\nTecnicas cobertas:")
        for tec in tecnicas["cap2_techniques"]:
            print(f"  - {tec}")
        
        if media < 70:
            print(f"\nRECOMENDACOES:")
            print("  - Revise flashcards do Cap 2 (104 cards)")
            print("  - Pratique exemplos de cada tecnica")
            print("  - Refaca Simulado 02 (Test Techniques)")
    else:
        print("Nenhum simulado de Test Techniques registrado ainda.")
        print("\nDICA: Cap 2 e 50% do exame! Priorize este capitulo.")


def exportar_relatorio_html():
    dados = carregar_progresso()
    simulados = dados.get("simulados", [])
    
    if not simulados:
        print("\nNenhum simulado para exportar.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo = f"relatorio_progresso_{timestamp}.html"
    
    # Calcular estatisticas
    total_simulados = len(simulados)
    total_questoes = sum(s['total_questoes'] for s in simulados)
    total_acertos = sum(s['acertos'] for s in simulados)
    media_geral = round((total_acertos / total_questoes) * 100, 1)
    aprovados = sum(1 for s in simulados if s['aprovado'])
    
    por_capitulo = defaultdict(lambda: {"total": 0, "acertos": 0})
    for sim in simulados:
        cap = sim['capitulo']
        por_capitulo[cap]['total'] += sim['total_questoes']
        por_capitulo[cap]['acertos'] += sim['acertos']
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relatorio de Progresso ISTQB CTAL-TA</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: #ecf0f1; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-card h3 {{ margin: 0 0 10px 0; color: #34495e; font-size: 0.9em; }}
        .stat-card .value {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #3498db; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .progress-bar {{ background: #ecf0f1; height: 30px; border-radius: 5px; overflow: hidden; margin: 10px 0; }}
        .progress-fill {{ background: #3498db; height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }}
        .recomendacao {{ background: #e8f4f8; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Relatorio de Progresso ISTQB CTAL-TA</h1>
        <p><strong>Gerado em:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        
        <h2>Resumo Geral</h2>
        <div class="stats">
            <div class="stat-card">
                <h3>Total de Simulados</h3>
                <div class="value">{total_simulados}</div>
            </div>
            <div class="stat-card">
                <h3>Total de Questoes</h3>
                <div class="value">{total_questoes}</div>
            </div>
            <div class="stat-card">
                <h3>Media Geral</h3>
                <div class="value">{media_geral}%</div>
            </div>
            <div class="stat-card">
                <h3>Taxa de Aprovacao</h3>
                <div class="value">{round(aprovados/total_simulados*100, 1)}%</div>
            </div>
        </div>
        
        <h2>Desempenho por Capitulo</h2>
        <table>
            <tr><th>Capitulo</th><th>Acertos</th><th>Total</th><th>%</th><th>Progresso</th></tr>
"""
    
    for cap, stats in sorted(por_capitulo.items()):
        perc = round((stats['acertos'] / stats['total']) * 100, 1)
        html += f"""
            <tr>
                <td>{cap}</td>
                <td>{stats['acertos']}</td>
                <td>{stats['total']}</td>
                <td>{perc}%</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {perc}%">{perc}%</div>
                    </div>
                </td>
            </tr>
"""
    
    html += """
        </table>
        
        <h2>Historico de Simulados</h2>
        <table>
            <tr><th>Data</th><th>Capitulo</th><th>Resultado</th><th>%</th><th>Status</th></tr>
"""
    
    for sim in simulados:
        html += f"""
            <tr>
                <td>{sim['data']}</td>
                <td>{sim['capitulo']}</td>
                <td>{sim['acertos']}/{sim['total_questoes']}</td>
                <td>{sim['percentual']}%</td>
                <td>{'APROVADO' if sim['aprovado'] else 'REPROVADO'}</td>
            </tr>
"""
    
    html += f"""
        </table>
        
        <div class="recomendacao">
            <h3>Recomendacoes</h3>
"""
    
    if media_geral >= 80:
        html += "<p><strong>EXCELENTE!</strong> Voce esta pronto para o exame.</p>"
    elif media_geral >= 65:
        html += "<p><strong>BOM!</strong> Mais 2 semanas de estudo recomendadas.</p>"
    else:
        html += "<p><strong>ATENCAO!</strong> Estudo intensivo necessario.</p>"
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\nRelatorio HTML exportado: {arquivo}")


def ver_historico():
    dados = carregar_progresso()
    simulados = dados.get("simulados", [])
    
    if not simulados:
        print("\nNenhum simulado registrado ainda.")
        return
    
    print("\n" + "="*80)
    print("HISTORICO DE SIMULADOS")
    print("="*80)
    
    for idx, sim in enumerate(simulados, 1):
        print(f"\n{idx}. {sim['data']}")
        print(f"   Capitulo: {sim['capitulo']}")
        print(f"   Resultado: {sim['acertos']}/{sim['total_questoes']} ({sim['percentual']}%)")
        if sim.get('tempo_minutos'):
            print(f"   Tempo: {sim['tempo_minutos']} minutos")
        print(f"   Status: {'APROVADO' if sim['aprovado'] else 'REPROVADO'}")


def limpar_historico():
    confirmacao = input("\nTem certeza que deseja limpar TODO o historico? (sim/nao): ").strip().lower()
    
    if confirmacao == "sim":
        dados = {"simulados": []}
        salvar_progresso(dados)
        print("Historico limpo com sucesso!")
    else:
        print("Operacao cancelada.")


def menu_tracking():
    while True:
        print("\n" + "="*80)
        print("SISTEMA DE TRACKING DE PROGRESSO v2.0")
        print("="*80)
        print("\n1. Dashboard visual")
        print("2. Registrar resultado de simulado")
        print("3. Ver historico completo")
        print("4. Analise por tecnica de teste")
        print("5. Exportar relatorio HTML")
        print("6. Limpar historico")
        print("7. Voltar")
        
        escolha = input("\nEscolha uma opcao (1-7): ").strip()
        
        if escolha == "1":
            dashboard_visual()
        elif escolha == "2":
            menu_registrar()
        elif escolha == "3":
            ver_historico()
        elif escolha == "4":
            analise_por_tecnica()
        elif escolha == "5":
            exportar_relatorio_html()
        elif escolha == "6":
            limpar_historico()
        elif escolha == "7":
            break
        else:
            print("Opcao invalida!")


def menu_registrar():
    print("\nREGISTRAR RESULTADO DE SIMULADO")
    
    print("\nCapitulos disponiveis:")
    print("1. cap1_risk")
    print("2. cap2_techniques")
    print("3. cap3_quality")
    print("4. cap4_reviews")
    print("5. cap5_tools")
    print("6. completo")
    
    capitulos = {
        "1": "cap1_risk",
        "2": "cap2_techniques",
        "3": "cap3_quality",
        "4": "cap4_reviews",
        "5": "cap5_tools",
        "6": "completo"
    }
    
    escolha_cap = input("\nEscolha o capitulo (1-6): ").strip()
    
    if escolha_cap not in capitulos:
        print("Opcao invalida!")
        return
    
    capitulo = capitulos[escolha_cap]
    
    try:
        total = int(input("Total de questoes: ").strip())
        acertos = int(input("Numero de acertos: ").strip())
        
        if acertos > total or acertos < 0 or total <= 0:
            print("Valores invalidos!")
            return
        
        tempo = input("Tempo gasto em minutos (opcional, Enter para pular): ").strip()
        tempo_minutos = int(tempo) if tempo else None
        
        registrar_simulado(capitulo, total, acertos, tempo_minutos)
        
    except ValueError:
        print("Digite numeros validos!")


if __name__ == "__main__":
    menu_tracking()
