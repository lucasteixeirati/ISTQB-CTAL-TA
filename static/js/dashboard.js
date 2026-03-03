document.addEventListener('DOMContentLoaded', () => {
    inicializarModalRevisao();
    carregarEstatisticas();
});

function inicializarModalRevisao() {
    const modal = document.getElementById('modal-revisao-simulado');
    const btnFechar = document.getElementById('btn-fechar-revisao');

    if (!modal || !btnFechar) {
        return;
    }

    btnFechar.addEventListener('click', fecharModalRevisao);
    modal.addEventListener('click', (event) => {
        if (event.target === modal) {
            fecharModalRevisao();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && modal.style.display !== 'none') {
            fecharModalRevisao();
        }
    });
}

function escapeHtml(texto) {
    return String(texto ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function abrirModalRevisao(simulado, resultados) {
    const modal = document.getElementById('modal-revisao-simulado');
    const titulo = document.getElementById('modal-revisao-titulo');
    const corpo = document.getElementById('modal-revisao-corpo');

    if (!modal || !titulo || !corpo) {
        return;
    }

    const capitulo = escapeHtml(simulado.capitulo_nome || simulado.capitulo || 'N/A');
    titulo.textContent = `Revisão do Simulado - ${capitulo}`;

    const linhas = resultados.map((item, idx) => {
        const correto = item.correto;
        const statusIcon = correto ? '✅' : '❌';
        const statusTexto = correto ? 'Acertou' : 'Errou';
        const statusClasse = correto ? 'correta' : 'errada';
        const pergunta = escapeHtml(item.pergunta || `Questão ${idx + 1}`);
        const respostaUsuario = escapeHtml(item.resposta_usuario || '—');
        const respostaCorreta = escapeHtml(item.resposta_correta || '—');
        const justificativa = escapeHtml(item.justificativa || '');

        return `
            <div class="questao-revisao ${statusClasse}">
                <p style="margin-bottom: 10px;"><strong>${idx + 1}. ${pergunta}</strong></p>
                <p style="margin: 8px 0;"><strong>${statusIcon} ${statusTexto}</strong></p>
                <p style="margin: 8px 0;"><strong>Sua resposta:</strong> ${respostaUsuario}</p>
                <p style="margin: 8px 0;"><strong>Resposta correta:</strong> ${respostaCorreta}</p>
                ${justificativa ? `<p style="margin: 8px 0; margin-top: 12px;"><strong>Justificativa:</strong> ${justificativa}</p>` : ''}
            </div>
        `;
    }).join('');

    corpo.innerHTML = linhas;
    modal.style.display = 'flex';
    modal.setAttribute('aria-hidden', 'false');
}

function fecharModalRevisao() {
    const modal = document.getElementById('modal-revisao-simulado');
    const corpo = document.getElementById('modal-revisao-corpo');

    if (!modal || !corpo) {
        return;
    }

    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
    corpo.innerHTML = '';
}

async function carregarEstatisticas() {
    try {
        const response = await fetch('/api/estatisticas');
        const data = await response.json();
        
        if (data.success) {
            renderizarEstatisticas(data);
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

function renderizarEstatisticas(data) {
    // Stats gerais
    document.getElementById('total-simulados').textContent = data.total_simulados;
    document.getElementById('media-geral').textContent = `${data.media_geral}%`;
    
    // Status
    let status = 'Iniciante';
    let statusColor = '#7f8c8d';
    
    if (data.media_geral >= 80) {
        status = 'EXCELENTE';
        statusColor = '#27ae60';
    } else if (data.media_geral >= 65) {
        status = 'BOM';
        statusColor = '#f39c12';
    } else if (data.media_geral > 0) {
        status = 'ATENÇÃO';
        statusColor = '#e74c3c';
    }
    
    const statusEl = document.getElementById('status-geral');
    statusEl.textContent = status;
    statusEl.style.color = statusColor;
    
    // Gráfico de evolução
    renderizarGrafico(data.simulados);
    
    // Histórico
    renderizarHistorico(data.simulados);
    
    // Recomendações
    renderizarRecomendacoes(data.media_geral, data.total_simulados);
}

function renderizarGrafico(simulados) {
    const graficoDiv = document.getElementById('grafico-evolucao');
    
    if (simulados.length === 0) {
        graficoDiv.innerHTML = '<p class="empty-state">Nenhum simulado realizado ainda</p>';
        return;
    }
    
    graficoDiv.innerHTML = '';
    
    simulados.forEach((sim, index) => {
        const barraDiv = document.createElement('div');
        barraDiv.className = 'barra-grafico';
        
        const data = sim.data.split(' ')[0];
        
        barraDiv.innerHTML = `
            <div class="barra-label">${data}</div>
            <div class="barra-fill">
                <div class="barra-progress" style="width: ${sim.percentual}%">
                    ${sim.percentual}%
                </div>
            </div>
        `;
        
        graficoDiv.appendChild(barraDiv);
    });
}

function renderizarHistorico(simulados) {
    const tabelaDiv = document.getElementById('tabela-historico');
    
    if (simulados.length === 0) {
        tabelaDiv.innerHTML = '<p class="empty-state">Nenhum simulado realizado ainda</p>';
        return;
    }
    
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Data</th>
                    <th>Capítulo</th>
                    <th>Resultado</th>
                    <th>%</th>
                    <th>Status</th>
                    <th>Revisão</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    simulados.forEach(sim => {
        const statusText = sim.aprovado ? '✅ APROVADO' : '❌ REPROVADO';
        const statusColor = sim.aprovado ? '#27ae60' : '#e74c3c';
        
        html += `
            <tr>
                <td>${sim.data}</td>
                <td>${sim.capitulo}</td>
                <td>${sim.acertos}/${sim.total_questoes}</td>
                <td>${sim.percentual}%</td>
                <td style="color: ${statusColor}; font-weight: bold;">${statusText}</td>
                <td>
                    ${sim.tem_revisao && sim.id
                        ? `<button class="btn-secondary" onclick="abrirRevisaoSimulado('${sim.id}')">Ver revisão</button>`
                        : '<span>-</span>'}
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    tabelaDiv.innerHTML = html;
}

async function abrirRevisaoSimulado(simuladoId) {
    try {
        const response = await fetch(`/api/simulados/historico/${simuladoId}`);
        const data = await response.json();

        if (!data.success || !data.simulado) {
            throw new Error(data.error || 'Não foi possível carregar a revisão');
        }

        const simulado = data.simulado;
        const resultados = Array.isArray(simulado.resultados) ? simulado.resultados : [];

        if (resultados.length === 0) {
            const modal = document.getElementById('modal-revisao-simulado');
            const titulo = document.getElementById('modal-revisao-titulo');
            const corpo = document.getElementById('modal-revisao-corpo');
            
            if (modal && titulo && corpo) {
                titulo.textContent = 'Revisão do Simulado';
                corpo.innerHTML = '<div style="padding: 40px; text-align: center; color: #b8c1ec;"><p>Este simulado não possui revisão detalhada.</p><p style="margin-top: 10px; font-size: 0.9em;">Simulados antigos podem não conter o histórico completo de respostas.</p></div>';
                modal.style.display = 'flex';
                modal.setAttribute('aria-hidden', 'false');
            }
            return;
        }

        abrirModalRevisao(simulado, resultados);
    } catch (error) {
        console.error('Erro ao abrir revisão:', error);
        alert('Erro ao carregar revisão detalhada.');
    }
}

function renderizarRecomendacoes(media, totalSimulados) {
    const recomendacoesDiv = document.getElementById('recomendacoes');
    
    let recomendacoes = [];
    
    if (totalSimulados === 0) {
        recomendacoes.push({
            titulo: 'Comece Agora!',
            texto: 'Faça seu primeiro simulado para começar a acompanhar seu progresso.'
        });
    } else if (media >= 80) {
        recomendacoes.push({
            titulo: '🏆 Excelente Desempenho!',
            texto: 'Você está pronto para o exame! Continue praticando para manter o nível.'
        });
        recomendacoes.push({
            titulo: 'Próximos Passos',
            texto: 'Faça mais 2-3 simulados completos e agende seu exame.'
        });
    } else if (media >= 65) {
        recomendacoes.push({
            titulo: '⚠️ Bom Desempenho',
            texto: 'Você está no caminho certo! Mais 2 semanas de estudo recomendadas.'
        });
        recomendacoes.push({
            titulo: 'Foque em',
            texto: 'Revise os capítulos com menor pontuação e refaça os simulados.'
        });
    } else {
        recomendacoes.push({
            titulo: '❌ Atenção Necessária',
            texto: 'Estudo intensivo necessário. Revise todo o material antes de continuar.'
        });
        recomendacoes.push({
            titulo: 'Recomendação',
            texto: 'Estude os flashcards diariamente e refaça todos os simulados.'
        });
    }
    
    recomendacoesDiv.innerHTML = '';
    
    recomendacoes.forEach(rec => {
        const div = document.createElement('div');
        div.className = 'recomendacao';
        div.innerHTML = `
            <h4>${rec.titulo}</h4>
            <p>${rec.texto}</p>
        `;
        recomendacoesDiv.appendChild(div);
    });
}
