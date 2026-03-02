"""
Script de Importação de Questões dos Simulados Markdown
Extrai questões dos arquivos .md e gera estrutura Python
"""

import re
import json

def extrair_questoes_markdown(arquivo_md, capitulo):
    """Extrai questões de arquivo Markdown"""
    with open(arquivo_md, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    questoes = []
    # Regex para capturar questões
    pattern = r'## Questão \d+ \(([K234])\)(.*?)(?=## Questão|\## Gabarito|$)'
    matches = re.findall(pattern, conteudo, re.DOTALL)
    
    for k_level, bloco in matches:
        # Extrair pergunta
        pergunta_match = re.search(r'\n(.*?)\n\n[A-D]\)', bloco, re.DOTALL)
        if not pergunta_match:
            continue
        pergunta = pergunta_match.group(1).strip()
        
        # Extrair opções
        opcoes = {}
        for letra in ['A', 'B', 'C', 'D']:
            opcao_match = re.search(rf'{letra}\)(.*?)(?:\n[A-D]\)|\n\*\*Resposta)', bloco, re.DOTALL)
            if opcao_match:
                opcoes[letra] = opcao_match.group(1).strip()
        
        # Extrair resposta
        resposta_match = re.search(r'\*\*Resposta:\*\* ([A-D])', bloco)
        resposta = resposta_match.group(1) if resposta_match else "A"
        
        # Extrair justificativa
        just_match = re.search(r'\*\*Justificativa:\*\*(.*?)(?:\n---|$)', bloco, re.DOTALL)
        justificativa = just_match.group(1).strip() if just_match else ""
        
        questoes.append({
            "k_level": f"K{k_level}",
            "pergunta": pergunta,
            "opcoes": opcoes,
            "resposta": resposta,
            "justificativa": justificativa
        })
    
    return questoes

# Processar todos os simulados
simulados = [
    ("simulados/simulado_01_risk_based_testing.md", "cap1_risk"),
    ("simulados/simulado_02_test_techniques.md", "cap2_techniques"),
    ("simulados/simulado_03_quality_characteristics.md", "cap3_quality"),
    ("simulados/simulado_04_reviews_tools.md", "cap4_reviews"),
    ("simulados/simulado_05_completo_final.md", "completo")
]

banco_completo = {}

for arquivo, cap in simulados:
    try:
        questoes = extrair_questoes_markdown(arquivo, cap)
        print(f"OK {arquivo}: {len(questoes)} questoes extraidas")
        
        if cap == "completo":
            # Distribuir questões do simulado completo
            for i, q in enumerate(questoes):
                if i < 6:
                    banco_completo.setdefault("cap1_risk", []).append(q)
                elif i < 26:
                    banco_completo.setdefault("cap2_techniques", []).append(q)
                elif i < 34:
                    banco_completo.setdefault("cap3_quality", []).append(q)
                elif i < 38:
                    banco_completo.setdefault("cap4_reviews", []).append(q)
                else:
                    banco_completo.setdefault("cap5_tools", []).append(q)
        else:
            banco_completo[cap] = questoes
    except Exception as e:
        print(f"ERRO em {arquivo}: {e}")

# Salvar em JSON
with open("banco_questoes.json", "w", encoding="utf-8") as f:
    json.dump(banco_completo, f, indent=2, ensure_ascii=False)

print(f"\nRESUMO:")
for cap, questoes in banco_completo.items():
    print(f"  {cap}: {len(questoes)} questões")
print(f"\nTotal: {sum(len(q) for q in banco_completo.values())} questoes")
print(f"Banco salvo em: banco_questoes.json")
