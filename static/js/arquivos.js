let arquivoSelecionado = null;
let llmOpcoes = [];
let llmSelecionada = 'auto';

document.addEventListener('DOMContentLoaded', () => {
    carregarArquivos();
    carregarLLMOpcoes();
    
    // Upload de arquivo
    const fileInput = document.getElementById('file-input');
    fileInput.addEventListener('change', uploadArquivo);
    
    // Drag and drop
    const uploadArea = document.getElementById('upload-area');
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#3498db';
    });
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#ecf0f1';
    });
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#ecf0f1';
        fileInput.files = e.dataTransfer.files;
        uploadArquivo();
    });
});

async function carregarArquivos() {
    try {
        const response = await fetch('/api/arquivos');
        const data = await response.json();
        
        if (data.success) {
            renderizarArquivos(data.arquivos);
        }
    } catch (error) {
        console.error('Erro ao carregar arquivos:', error);
    }
}

function renderizarArquivos(arquivos) {
    const lista = document.getElementById('lista-arquivos');
    
    if (arquivos.length === 0) {
        lista.innerHTML = '<p class="empty-state">Nenhum arquivo anexado ainda</p>';
        return;
    }
    
    lista.innerHTML = '';
    
    arquivos.forEach(arquivo => {
        const div = document.createElement('div');
        div.className = 'arquivo-item';
        
        div.innerHTML = `
            <div class="arquivo-info">
                <h3>📄 ${arquivo.nome}</h3>
                <p class="arquivo-meta">
                    ${arquivo.tipo.toUpperCase()} • 
                    ${arquivo.data_upload} • 
                    ${arquivo.questoes_geradas} questões geradas
                </p>
            </div>
            <div class="arquivo-acoes">
                <button onclick="abrirModalGerar(${arquivo.id})" class="btn-primary">
                    Examinar e Gerar Questões
                </button>
                <button onclick="abrirModalDeletar(${arquivo.id})" class="btn-danger">
                    Deletar
                </button>
            </div>
        `;
        
        lista.appendChild(div);
    });
}

async function uploadArquivo() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Arquivo enviado com sucesso!');
            fileInput.value = '';
            carregarArquivos();
        } else {
            alert('Erro: ' + data.error);
        }
    } catch (error) {
        alert('Erro ao enviar arquivo: ' + error);
    }
}

async function carregarLLMOpcoes() {
    const select = document.getElementById('llm-provider');
    if (!select) return;
    try {
        const resp = await fetch('/api/llm-opcoes');
        const data = await resp.json();
        if (!data.success || !Array.isArray(data.opcoes)) return;
        llmOpcoes = data.opcoes;
        select.innerHTML = '';
        data.opcoes.forEach(op => {
            const opt = document.createElement('option');
            opt.value = op.id;
            opt.textContent = op.label;
            select.appendChild(opt);
        });
        llmSelecionada = 'auto';
        select.value = 'auto';
        select.addEventListener('change', () => {
            llmSelecionada = select.value;
        });
    } catch (e) {
        console.error('Falha ao carregar opções de LLM:', e);
    }
}

function abrirModalGerar(arquivoId) {
    arquivoSelecionado = arquivoId;
    document.getElementById('modal-gerar').style.display = 'flex';
}

function abrirModalDeletar(arquivoId) {
    arquivoSelecionado = arquivoId;
    document.getElementById('modal-deletar').style.display = 'flex';
}

function fecharModal() {
    document.getElementById('modal-gerar').style.display = 'none';
    document.getElementById('modal-deletar').style.display = 'none';
    // não limpar arquivoSelecionado aqui: ele é necessário para salvar questões no modal de revisão
}

function fecharModalRevisao() {
    document.getElementById('modal-revisao-questoes').style.display = 'none';
    esconderDebugLLM();
    // agora sim podemos limpar o selecionado
    arquivoSelecionado = null;
}

function setLoadingGeracao(loading) {
    const overlay = document.getElementById('loading-geracao');
    const btnGerar = document.getElementById('btn-gerar');
    const btnCancelar = document.getElementById('btn-cancelar-gerar');
    if (!overlay) return;

    overlay.style.display = loading ? 'flex' : 'none';
    if (btnGerar) btnGerar.disabled = loading;
    if (btnCancelar) btnCancelar.disabled = loading;
}

function mostrarDebugLLM(payload) {
    const details = document.getElementById('debug-llm-details');
    const pre = document.getElementById('debug-llm-json');
    if (!details || !pre) return;

    try {
        pre.textContent = JSON.stringify(payload, null, 2);
    } catch {
        pre.textContent = String(payload);
    }
    details.style.display = 'block';
}

function esconderDebugLLM() {
    const details = document.getElementById('debug-llm-details');
    const pre = document.getElementById('debug-llm-json');
    if (details) details.style.display = 'none';
    if (pre) pre.textContent = '';
}

async function confirmarGerar() {
    if (!arquivoSelecionado) {
        alert('Selecione um arquivo para gerar questões.');
        return;
    }

    const numQuestoes = parseInt(document.getElementById('num-questoes-gerar')?.value || '5', 10);
    const provider = document.getElementById('llm-provider')?.value || 'auto';

    const capSelect = document.getElementById('syllabus-capitulo');
    const capitulo_id = capSelect?.value || 'importados';
    const capitulo_nome = capSelect?.selectedOptions?.[0]?.getAttribute('data-label') || capSelect?.selectedOptions?.[0]?.textContent || 'Importados / Outros';

    setLoadingGeracao(true);

    fetch('/api/geracoes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            arquivo_id: arquivoSelecionado,
            num_questoes: numQuestoes,
            provider,
            capitulo_id,
            capitulo_nome
        })
    })
    .then(r => r.json().then(data => ({ ok: r.ok, status: r.status, data })))
    .then(({ ok, data }) => {
        if (!ok) {
            throw new Error(data?.erro || 'Falha ao criar job de geração');
        }

        fecharModal();
        setLoadingGeracao(false);

        // Redireciona para a tela de Gerações para acompanhar o job
        window.location.href = '/geracoes';
    })
    .catch(err => {
        console.error(err);
        setLoadingGeracao(false);
        alert(err?.message || 'Erro ao iniciar geração');
    });
}

function exibirQuestoesGeradas(questoes) {
    const modal = document.getElementById('modal-revisao-questoes');
    const lista = document.getElementById('questoes-geradas-lista');
    lista.innerHTML = '';

    if (!Array.isArray(questoes) || questoes.length === 0) {
        lista.innerHTML = `
            <div class="empty-state" style="margin: 8px 0 16px;">
                Nenhuma questão foi renderizada. Abra <b>Debug: retorno da IA (JSON)</b> acima para ver o que a API devolveu.
            </div>
        `;
        modal.style.display = 'flex';
        return;
    }

    questoes.forEach((q, idx) => {
        // Backend (app.py) retorna: { pergunta, opcoes: {A,B,C,D}, resposta }
        // IA pode retornar: { alternativas: [] }. Aceita ambos.
        let alternativas = [];
        const opcoes = q.opcoes && typeof q.opcoes === 'object' ? q.opcoes : (q.opcoes_map && typeof q.opcoes_map === 'object' ? q.opcoes_map : null);

        if (Array.isArray(q.alternativas) && q.alternativas.length) {
            alternativas = q.alternativas;
        } else if (Array.isArray(q.options) && q.options.length) {
            alternativas = q.options;
        } else if (opcoes) {
            alternativas = ['A', 'B', 'C', 'D'].map(l => opcoes[l]).filter(v => v);
        }

        const resposta = (q.resposta || q.resposta_correta || q.answer || '').toString().trim();

        lista.innerHTML += `
        <div class="questao-edit-block">
            <label>Pergunta ${idx + 1}:</label>
            <textarea name="pergunta_${idx}" rows="3">${q.pergunta || q.question || ''}</textarea>
            <label>Alternativas (uma por linha):</label>
            <textarea name="alternativas_${idx}" rows="6">${alternativas.join('\n')}</textarea>
            <label>Resposta Correta (A/B/C/D ou texto):</label>
            <input type="text" name="resposta_${idx}" value="${resposta}">
            <hr>
        </div>
        `;
    });
    modal.style.display = 'flex';
}

async function salvarQuestoesGeradas() {
    const form = document.getElementById('form-questoes-geradas');
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
            incompletas.push({
                idx: idx + 1,
                perguntaOk: !!pergunta,
                alternativas: alternativas.length,
                resposta
            });
        }
    });

    if (questoes.length === 0) {
        alert(
            'Nenhuma questão completa para salvar.\n\n' +
            'Requisitos: pergunta preenchida + 4 alternativas (uma por linha) + resposta A/B/C/D.\n\n' +
            'Itens incompletos (debug): ' + JSON.stringify(incompletas.slice(0, 5))
        );
        return;
    }

    // Mantém o capítulo selecionado no modal de geração (se existir) ao salvar.
    const capSelect = document.getElementById('syllabus-capitulo');
    const capitulo_id = capSelect?.value || 'importados';
    const capitulo_nome = capSelect?.selectedOptions?.[0]?.getAttribute('data-label') || capSelect?.selectedOptions?.[0]?.textContent || 'Importados / Outros';

    try {
        const response = await fetch(`/api/arquivos/salvar-questoes/${arquivoSelecionado}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ questoes, capitulo_id, capitulo_nome })
        });
        const data = await response.json();
        if (data.success) {
            alert('Questões salvas com sucesso!');
            fecharModalRevisao();
            carregarArquivos();
        } else {
            const details = data.details ? `\n\nDetalhes: ${JSON.stringify(data.details)}` : '';
            alert('Erro ao salvar questões: ' + (data.error || data.msg || 'erro desconhecido') + details);
        }
    } catch (error) {
        alert('Erro ao salvar questões: ' + error);
    }
}

async function confirmarDeletar() {
    try {
        const response = await fetch(`/api/deletar-arquivo/${arquivoSelecionado}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Arquivo deletado com sucesso!');
            fecharModal();
            carregarArquivos();
        } else {
            alert('Erro: ' + data.error);
        }
    } catch (error) {
        alert('Erro ao deletar arquivo: ' + error);
    }
}
