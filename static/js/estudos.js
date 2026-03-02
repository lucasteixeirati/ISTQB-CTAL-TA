async function carregarMateriaisEstudos() {
    const lista = document.getElementById('lista-materiais');
    const filtroTipo = document.getElementById('filtro-tipo');
    const filtroBusca = document.getElementById('filtro-busca');

    const tipo = (filtroTipo?.value || 'todos').toLowerCase();
    const busca = (filtroBusca?.value || '').trim().toLowerCase();

    try {
        if (lista) lista.innerHTML = '<p class="empty-state">Carregando...</p>';

        const resp = await fetch('/api/materiais');
        const data = await resp.json();

        if (!data.success) {
            if (lista) lista.innerHTML = `<p class="empty-state">Erro: ${data.error || 'falha ao carregar materiais'}</p>`;
            return;
        }

        let itens = Array.isArray(data.materiais) ? data.materiais : [];

        if (tipo !== 'todos') {
            itens = itens.filter(i => (i.tipo || 'outros') === tipo);
        }

        if (busca) {
            itens = itens.filter(i => (i.nome || '').toLowerCase().includes(busca));
        }

        if (!itens.length) {
            if (lista) lista.innerHTML = '<p class="empty-state">Nenhum material encontrado.</p>';
            return;
        }

        if (!lista) return;
        lista.innerHTML = '';
        itens.forEach(item => {
            const div = document.createElement('div');
            div.className = 'arquivo-item';

            const tipoLabel = (item.tipo || 'outros').toUpperCase();
            const tamanhoKb = typeof item.tamanho_bytes === 'number' ? (item.tamanho_bytes / 1024).toFixed(1) : '-';

            div.innerHTML = `
                <div class="arquivo-info">
                    <h3>📦 ${item.nome}</h3>
                    <p class="arquivo-meta">
                        ${tipoLabel} • ${tamanhoKb} KB • ${item.modificado_em || '-'}
                    </p>
                </div>
                <div class="arquivo-acoes">
                    <button class="btn-primary" onclick="abrirPreview('${item.url}', '${escapeHtml(item.nome)}', '${item.tipo || 'outros'}')">Abrir</button>
                    <a class="btn-secondary" href="${item.url}" target="_blank" rel="noopener">Nova aba</a>
                </div>
            `;

            lista.appendChild(div);
        });
    } catch (e) {
        console.error(e);
        if (lista) lista.innerHTML = `<p class="empty-state">Erro ao carregar materiais: ${e}</p>`;
    }
}

// compatibilidade: se algo antigo chamar, ainda funciona
async function carregarMateriais() {
    return carregarMateriaisEstudos();
}

function abrirPreview(url, nome, tipo) {
    const modal = document.getElementById('modal-preview');
    const titulo = document.getElementById('modal-preview-titulo');
    const body = document.getElementById('modal-preview-body');

    titulo.textContent = nome;

    if (tipo === 'pdf') {
        body.innerHTML = `
            <iframe src="${url}" style="width: 100%; height: 70vh; border: none; border-radius: 12px;"></iframe>
        `;
    } else if (tipo === 'audio') {
        body.innerHTML = `
            <audio controls style="width: 100%;">
                <source src="${url}">
                Seu navegador não suporta áudio.
            </audio>
        `;
    } else if (tipo === 'video') {
        body.innerHTML = `
            <video controls style="width: 100%; max-height: 70vh; border-radius: 12px;">
                <source src="${url}">
                Seu navegador não suporta vídeo.
            </video>
        `;
    } else {
        body.innerHTML = `
            <p class="help-text">Preview não disponível para este tipo. Use “Nova aba”.</p>
        `;
    }

    modal.style.display = 'flex';
}

function fecharPreview() {
    const modal = document.getElementById('modal-preview');
    const body = document.getElementById('modal-preview-body');
    body.innerHTML = '';
    modal.style.display = 'none';
}

function escapeHtml(str) {
    return String(str)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}

document.addEventListener('DOMContentLoaded', () => {
    const filtroTipo = document.getElementById('filtro-tipo');
    const filtroBusca = document.getElementById('filtro-busca');

    // Se existir lista-materiais (ex.: template antigo), mantém comportamento.
    // Na página unificada, quem renderiza é biblioteca.js.
    if (document.getElementById('lista-materiais')) {
        filtroTipo?.addEventListener('change', carregarMateriaisEstudos);
        filtroBusca?.addEventListener('input', () => {
            clearTimeout(window.__materiaisBuscaTimer);
            window.__materiaisBuscaTimer = setTimeout(carregarMateriaisEstudos, 250);
        });
        carregarMateriaisEstudos();
        return;
    }
});
