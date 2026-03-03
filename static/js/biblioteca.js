// Lista única: combina /api/arquivos (metadados do app) + /api/materiais (scan do uploads/)
// Mantém todas as funções existentes:
// - anexos continuam no container #lista-arquivos via arquivos.js
// - biblioteca única é renderizada aqui em #lista-biblioteca

async function renderizarListaUnica() {
    const lista = document.getElementById('lista-biblioteca');
    if (!lista) return;

    const filtroTipo = document.getElementById('filtro-tipo');
    const filtroBusca = document.getElementById('filtro-busca');

    const tipo = (filtroTipo?.value || 'todos').toLowerCase();
    const busca = (filtroBusca?.value || '').trim().toLowerCase();

    try {
        lista.innerHTML = '<p class="empty-state">Carregando...</p>';

        const [respArquivos, respMateriais] = await Promise.all([
            fetch('/api/arquivos').then(r => r.json()).catch(() => ({ success: false })),
            fetch('/api/materiais').then(r => r.json()).catch(() => ({ success: false })),
        ]);

        const anexos = respArquivos?.success && Array.isArray(respArquivos.arquivos) ? respArquivos.arquivos : [];
        const materiais = respMateriais?.success && Array.isArray(respMateriais.materiais) ? respMateriais.materiais : [];

        // Normaliza para um formato único
        // origem: 'anexo' (do app) ou 'uploads' (scan)
        let itens = [];

        anexos.forEach(a => {
            itens.push({
                origem: 'anexo',
                nome: a.nome,
                tipo: (a.tipo || 'outros').toLowerCase(),
                modificado_em: a.data_upload || '-',
                tamanho_bytes: null,
                arquivo_id: a.id,
            });
        });

        materiais.forEach(m => {
            itens.push({
                origem: 'uploads',
                nome: m.nome,
                tipo: (m.tipo || 'outros').toLowerCase(),
                modificado_em: m.modificado_em || '-',
                tamanho_bytes: typeof m.tamanho_bytes === 'number' ? m.tamanho_bytes : null,
                url: m.url,
            });
        });

        // filtros
        if (tipo !== 'todos') {
            itens = itens.filter(i => (i.tipo || 'outros') === tipo);
        }
        if (busca) {
            itens = itens.filter(i => (i.nome || '').toLowerCase().includes(busca));
        }

        // ordena por nome
        itens.sort((a, b) => (a.nome || '').toLowerCase().localeCompare((b.nome || '').toLowerCase()));

        if (!itens.length) {
            lista.innerHTML = '<p class="empty-state">Nenhum item encontrado.</p>';
            return;
        }

        lista.innerHTML = '';
        itens.forEach(item => {
            const div = document.createElement('div');
            div.className = 'arquivo-item';

            const tipoLabel = (item.tipo || 'outros').toUpperCase();
            const origemLabel = item.origem === 'anexo' ? 'ANEXO' : 'UPLOADS';

            const tamanhoKb = typeof item.tamanho_bytes === 'number' ? (item.tamanho_bytes / 1024).toFixed(1) : null;
            const metaParts = [tipoLabel, origemLabel, item.modificado_em || '-'];
            if (tamanhoKb !== null) metaParts.splice(2, 0, `${tamanhoKb} KB`);

            // Verifica se pode gerar questões (apenas PDF/TXT de anexos)
            const podeGerarIA = item.origem === 'anexo' && (item.tipo === 'pdf' || item.tipo === 'txt');
            
            const acoesHtml = item.origem === 'anexo'
                ? podeGerarIA
                    ? `<button onclick="abrirModalGerar(${item.arquivo_id})" class="btn-primary">Examinar e Gerar Questões</button>`
                    : `<button class="btn-secondary" disabled title="Apenas PDF e TXT podem gerar questões">🚫 Não gera questões (${item.tipo.toUpperCase()})</button>`
                : `
                    <button class="btn-primary" onclick="abrirPreview('${item.url}', '${escapeHtml(item.nome)}', '${item.tipo || 'outros'}')">Abrir</button>
                    <a class="btn-secondary" href="${item.url}" target="_blank" rel="noopener">Nova aba</a>
                  `;

            div.innerHTML = `
                <div class="arquivo-info">
                    <h3>📚 ${item.nome}</h3>
                    <p class="arquivo-meta">${metaParts.join(' • ')}</p>
                </div>
                <div class="arquivo-acoes">${acoesHtml}</div>
            `;

            lista.appendChild(div);
        });

    } catch (e) {
        console.error(e);
        lista.innerHTML = `<p class="empty-state">Erro ao renderizar biblioteca: ${e}</p>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const filtroTipo = document.getElementById('filtro-tipo');
    const filtroBusca = document.getElementById('filtro-busca');

    filtroTipo?.addEventListener('change', renderizarListaUnica);
    filtroBusca?.addEventListener('input', () => {
        clearTimeout(window.__bibliotecaBuscaTimer);
        window.__bibliotecaBuscaTimer = setTimeout(renderizarListaUnica, 250);
    });

    // primeira renderização
    renderizarListaUnica();
});
