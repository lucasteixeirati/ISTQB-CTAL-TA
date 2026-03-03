let geracoes = [];
let jobSelecionado = null;

document.addEventListener('DOMContentLoaded', () => {
    carregarGeracoes();
    setInterval(carregarGeracoes, 10000); // 10 segundos
});

function _parseJobDate(job) {
    const raw = (job && (job.atualizado_em || job.criado_em)) || '';
    if (!raw) return 0;

    // tenta ISO e "YYYY-MM-DD HH:MM:SS"
    const normalized = raw.includes('T') ? raw : raw.replace(' ', 'T');
    const ms = Date.parse(normalized);
    return Number.isNaN(ms) ? 0 : ms;
}

async function carregarGeracoes() {
    try {
        const resp = await fetch('/api/geracoes');
        const data = await resp.json();
        if (!data.success) return;
        geracoes = data.jobs || [];

        // Ordenação invertida: mais recentes primeiro (topo), mais antigos por último (final)
        geracoes.sort((a, b) => {
            const da = _parseJobDate(a);
            const db = _parseJobDate(b);
            if (da !== db) return db - da; // DESC
            return String(b.id || '').localeCompare(String(a.id || '')); // fallback DESC
        });

        renderizarGeracoes();
    } catch (e) {
        console.error('Erro ao carregar gerações:', e);
    }
}

function renderizarGeracoes() {
    const container = document.getElementById('lista-geracoes');

    // Atualiza contadores
    const elTotal = document.getElementById('total-jobs');
    const elProcessando = document.getElementById('total-processando');
    const elConcluidos = document.getElementById('total-concluidos');

    const total = geracoes.length;
    const processando = geracoes.filter(j => ['pendente', 'processando'].includes((j.status || '').toLowerCase())).length;
    const concluidos = geracoes.filter(j => ['concluido', 'concluido_salvo'].includes((j.status || '').toLowerCase())).length;

    if (elTotal) elTotal.textContent = String(total);
    if (elProcessando) elProcessando.textContent = String(processando);
    if (elConcluidos) elConcluidos.textContent = String(concluidos);

    if (!geracoes.length) {
        container.innerHTML = '<p class="empty-state">Nenhuma geração iniciada ainda.</p>';
        return;
    }
    container.innerHTML = '';
    geracoes.forEach(job => {
        const div = document.createElement('div');
        div.className = 'geracao-item';
        const statusLabel = job.status || 'desconhecido';
        div.innerHTML = `
            <div class="geracao-info">
                <h3>Job ${job.id}</h3>
                <p class="geracao-meta">
                    Arquivo: ${job.arquivo_nome || '-'} · LLM: ${job.provider || '-'} · Qtd: ${job.num_questoes || '-'}
                </p>
                <p class="geracao-meta">
                    Status: <span class="status-badge status-${statusLabel}">${statusLabel}</span>
                    · Criado em: ${job.criado_em || '-'}
                    · Atualizado em: ${job.atualizado_em || '-'}
                </p>
            </div>
            <div class="geracao-acoes">
                <button class="btn-primary" onclick="abrirDetalheJob('${job.id}')" ${statusLabel === 'concluido' || statusLabel === 'concluido_salvo' ? '' : 'disabled'}>
                    Ver Questões
                </button>
            </div>
        `;
        container.appendChild(div);
    });
}

async function abrirDetalheJob(jobId) {
    jobSelecionado = jobId;
    try {
        const resp = await fetch(`/api/geracoes/${jobId}`);
        const data = await resp.json();
        if (!data.success) {
            alert(data.error || 'Erro ao carregar job');
            return;
        }
        const job = data.job;
        const lista = document.getElementById('questoes-geradas-job-lista');
        lista.innerHTML = '';
        const questoes = job.questoes || [];
        if (!questoes.length) {
            lista.innerHTML = '<p class="empty-state">Nenhuma questão disponível para este job.</p>';
        } else {
            questoes.forEach((q, idx) => {
                const opcoes = q.opcoes || {};
                const alternativas = ['A','B','C','D'].map(l => opcoes[l] || '').filter(a => a);
                const resposta = (q.resposta || '').toString().trim();
                lista.innerHTML += `
                    <div class="questao-edit-block">
                        <label>Pergunta ${idx + 1}:</label>
                        <textarea name="pergunta_${idx}" rows="3">${q.pergunta || ''}</textarea>
                        <label>Alternativas (uma por linha):</label>
                        <textarea name="alternativas_${idx}" rows="6">${alternativas.join('\n')}</textarea>
                        <label>Resposta Correta (A/B/C/D):</label>
                        <input type="text" name="resposta_${idx}" value="${resposta}">
                        <hr>
                    </div>
                `;
            });
        }
        document.getElementById('modal-geracao-detalhe').style.display = 'flex';
    } catch (e) {
        alert('Erro ao carregar detalhes do job: ' + e);
    }
}

function fecharModalJob() {
    document.getElementById('modal-geracao-detalhe').style.display = 'none';
    jobSelecionado = null;
}

async function salvarQuestoesJob() {
    if (!jobSelecionado) return;
    const form = document.getElementById('form-questoes-geradas-job');
    const blocks = form.querySelectorAll('.questao-edit-block');
    const questoes = [];
    const incompletas = [];

    blocks.forEach((block, idx) => {
        const pergunta = block.querySelector(`textarea[name='pergunta_${idx}']`).value.trim();
        const alternativas = block.querySelector(`textarea[name='alternativas_${idx}']`).value
            .split('\n')
            .map(a => a.trim())
            .filter(a => a);
        const resposta = block.querySelector(`input[name='resposta_${idx}']`).value.trim().toUpperCase();

        const completa = !!pergunta && alternativas.length === 4 && ['A','B','C','D'].includes(resposta);
        if (completa) {
            questoes.push({ pergunta, alternativas, resposta });
        } else {
            incompletas.push({ idx: idx + 1, perguntaOk: !!pergunta, alternativas: alternativas.length, resposta });
        }
    });

    if (!questoes.length) {
        alert('Nenhuma questão completa para salvar. Verifique pergunta, 4 alternativas e resposta A/B/C/D.');
        return;
    }

    // Exibe mensagem de carregamento
    const btnSalvar = document.querySelector('#modal-job button[onclick="salvarQuestoesJob()"]');
    if (btnSalvar) {
        btnSalvar.disabled = true;
        btnSalvar.textContent = 'Analisando duplicidade...';
    }

    try {
        const resp = await fetch(`/api/geracoes/${jobSelecionado}/salvar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ questoes })
        });
        const data = await resp.json();
        
        if (data.success) {
            let mensagem = data.msg || 'Questões salvas com sucesso!';
            
            // Adiciona detalhes de estatísticas se disponível
            if (data.estatisticas) {
                const stats = data.estatisticas;
                mensagem += `\n\n📊 Estatísticas:`;
                mensagem += `\n✅ Salvas: ${stats.salvas}`;
                if (stats.duplicadas > 0) {
                    mensagem += `\n⚠️ Duplicadas (ignoradas): ${stats.duplicadas}`;
                }
                if (stats.invalidas > 0) {
                    mensagem += `\n❌ Inválidas (descartadas): ${stats.invalidas}`;
                }
                mensagem += `\n📝 Total analisadas: ${stats.total_analisadas}`;
            }
            
            alert(mensagem);
            fecharModalJob();
            carregarGeracoes();
        } else {
            alert('Erro ao salvar questões: ' + (data.error || data.msg || 'erro desconhecido'));
        }
    } catch (e) {
        alert('Erro ao salvar questões: ' + e);
    } finally {
        // Restaura o botão
        if (btnSalvar) {
            btnSalvar.disabled = false;
            btnSalvar.textContent = 'Salvar Questões';
        }
    }
}
