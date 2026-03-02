let flashcards = [];
let cardAtual = 0;
let avaliacoes = { facil: 0, medio: 0, dificil: 0 };
let deckSelecionado = '';
let capituloSelecionado = { id: 'todos', nome: 'Todos' };

document.addEventListener('DOMContentLoaded', () => {
    // capítulo
    const capSel = document.getElementById('flashcards-capitulo');
    if (capSel) {
        capituloSelecionado = {
            id: capSel.value || 'todos',
            nome: capSel.selectedOptions?.[0]?.getAttribute('data-label') || capSel.selectedOptions?.[0]?.textContent || 'Todos'
        };

        capSel.addEventListener('change', () => {
            capituloSelecionado = {
                id: capSel.value || 'todos',
                nome: capSel.selectedOptions?.[0]?.getAttribute('data-label') || capSel.selectedOptions?.[0]?.textContent || 'Todos'
            };
            carregarDecks();
        });
    }

    carregarDecks();
});

async function carregarDecks() {
    try {
        const response = await fetch('/api/flashcards/decks');
        const data = await response.json();
        
        if (data.success) {
            renderizarDecks(data.decks);

            // Atualiza total no botão "Estudar Todos" (considerando filtro de capítulo)
            const ds = Array.isArray(data.decks) ? data.decks : [];
            const capId = capituloSelecionado?.id || 'todos';

            const total = ds
                .filter(d => {
                    if (capId === 'todos') return true;
                    const deckId = String(d?.deck_id || '').toLowerCase();
                    if (capId === 'cap1') return deckId.startsWith('deck_01');
                    if (capId === 'cap2') return deckId.startsWith('deck_02');
                    if (capId === 'cap3') return deckId.startsWith('deck_03');
                    if (capId === 'cap4') return deckId.startsWith('deck_04');
                    if (capId === 'cap5') return deckId.startsWith('deck_05');
                    return true;
                })
                .reduce((acc, d) => acc + (Number(d?.total) || 0), 0);

            const totalLabel = document.getElementById('total-flashcards-label');
            if (totalLabel) totalLabel.textContent = String(total || 0);
        }
    } catch (error) {
        console.error('Erro ao carregar decks:', error);
        const totalLabel = document.getElementById('total-flashcards-label');
        if (totalLabel) totalLabel.textContent = '-';
    }
}

function _mapDeckParaCapitulo(deckNome) {
    const n = (deckNome || '').toLowerCase();

    // deck_01_risk_based_testing
    if (n.includes('risk')) return { id: 'cap1', nome: 'Cap 1 - Risk-based Testing' };

    // deck_02_* (black box / whitebox)
    if (
        n.includes('test techniques') ||
        n.includes('black box') ||
        n.includes('blackbox') ||
        n.includes('white box') ||
        n.includes('whitebox') ||
        n.includes('experience') ||
        n.includes('techniques') ||
        n.match(/\b02\b/) ||
        n.includes('deck 02') ||
        n.includes('deck_02')
    ) {
        return { id: 'cap2', nome: 'Cap 2 - Test Techniques' };
    }

    // deck_03_quality_characteristics
    if (n.includes('quality') || n.includes('characteristics') || n.includes('deck_03') || n.includes('deck 03') || n.match(/\b03\b/)) {
        return { id: 'cap3', nome: 'Cap 3 - Quality Characteristics' };
    }

    // deck_04_reviews
    if (n.includes('review') || n.includes('reviews') || n.includes('deck_04') || n.includes('deck 04') || n.match(/\b04\b/)) {
        return { id: 'cap4', nome: 'Cap 4 - Reviews' };
    }

    // deck_05_test_tools
    if (n.includes('tool') || n.includes('tools') || n.includes('automation') || n.includes('deck_05') || n.includes('deck 05') || n.match(/\b05\b/)) {
        return { id: 'cap5', nome: 'Cap 5 - Test Tools' };
    }

    return { id: 'importados', nome: 'Importados / Outros' };
}

function renderizarDecks(decks) {
    const listaDecks = document.getElementById('lista-decks');
    listaDecks.innerHTML = '';

    const ds = Array.isArray(decks) ? decks : [];

    // filtra decks pelo capítulo selecionado (preferindo deck_id)
    const decksFiltrados = ds.filter(d => {
        if (!capituloSelecionado || (capituloSelecionado.id || 'todos') === 'todos') return true;

        const deckId = (d?.deck_id || '').toLowerCase();
        if (deckId.startsWith('deck_01')) return capituloSelecionado.id === 'cap1';
        if (deckId.startsWith('deck_02')) return capituloSelecionado.id === 'cap2';
        if (deckId.startsWith('deck_03')) return capituloSelecionado.id === 'cap3';
        if (deckId.startsWith('deck_04')) return capituloSelecionado.id === 'cap4';
        if (deckId.startsWith('deck_05')) return capituloSelecionado.id === 'cap5';

        // fallback: heurística antiga
        const cap = _mapDeckParaCapitulo(d?.nome);
        return cap.id === capituloSelecionado.id;
    });
    
    decksFiltrados.forEach(deck => {
        const deckDiv = document.createElement('div');
        deckDiv.className = 'deck-card';
        deckDiv.onclick = () => iniciarDeck(deck.nome);

        const cap = _mapDeckParaCapitulo(deck.nome);
        const capLinha = capituloSelecionado?.id === 'todos' ? `<p style="opacity:.8">${cap.nome}</p>` : '';
        
        deckDiv.innerHTML = `
            <h3>${deck.nome}</h3>
            <p>${deck.total} cards</p>
            ${capLinha}
        `;
        
        listaDecks.appendChild(deckDiv);
    });

    if (!decksFiltrados.length) {
        listaDecks.innerHTML = '<p class="empty-state">Nenhum deck encontrado para este capítulo.</p>';
    }
}

async function iniciarDeck(deckNome) {
    deckSelecionado = deckNome;
    await carregarFlashcards(deckNome);
}

async function iniciarTodos() {
    deckSelecionado = capituloSelecionado?.id === 'todos'
        ? 'Todos os Decks'
        : `Todos os Decks • ${capituloSelecionado.nome}`;

    await carregarFlashcards('todos');
}

async function carregarFlashcards(deck) {
    try {
        // reset de estado ao iniciar uma sessão
        cardAtual = 0;
        avaliacoes = { facil: 0, medio: 0, dificil: 0 };

        const capId = capituloSelecionado?.id || 'todos';
        const capNome = capituloSelecionado?.nome || (capId === 'todos' ? 'Todos' : capId);

        const qs = new URLSearchParams({ deck });
        if (capId !== 'todos') {
            qs.set('capitulo_id', capId);
            qs.set('capitulo_nome', capNome);
        }

        const response = await fetch(`/api/flashcards?${qs.toString()}`);
        const data = await response.json();
        
        if (data.success) {
            flashcards = Array.isArray(data.flashcards) ? data.flashcards : [];

            if (!flashcards.length) {
                document.getElementById('config-flashcards').style.display = 'none';
                document.getElementById('flashcard-content').style.display = 'none';
                document.getElementById('resultado-flash').style.display = 'block';

                document.getElementById('total-revisados').textContent = '0';
                document.getElementById('total-faceis').textContent = '0';
                document.getElementById('total-medios').textContent = '0';
                document.getElementById('total-dificeis').textContent = '0';
                document.getElementById('recomendacao-texto').textContent = 'Nenhum flashcard encontrado para o filtro selecionado.';

                return;
            }
            
            // Embaralhar
            flashcards.sort(() => Math.random() - 0.5);

            document.getElementById('resultado-flash').style.display = 'none';
            document.getElementById('config-flashcards').style.display = 'none';
            document.getElementById('flashcard-content').style.display = 'block';
            document.getElementById('total-cards').textContent = flashcards.length;
            document.getElementById('deck-atual').textContent = deckSelecionado;
            
            mostrarCard(0);
        }
    } catch (error) {
        alert('Erro ao carregar flashcards: ' + error);
    }
}

function mostrarCard(index) {
    cardAtual = index;
    const card = flashcards[index];

    // guard: pode acontecer se a lista estiver vazia ou index inválido
    if (!card) {
        document.getElementById('card-atual').textContent = '0';
        document.getElementById('pergunta').textContent = '';
        document.getElementById('resposta').innerHTML = '';
        return;
    }
    
    document.getElementById('card-atual').textContent = index + 1;
    document.getElementById('pergunta').textContent = card.pergunta || '';
    document.getElementById('resposta').innerHTML = String(card.resposta || '').replace(/\n/g, '<br>');

    // Resetar flip
    document.getElementById('flashcard').classList.remove('flipped');

    // Atualizar botões
    document.getElementById('btn-voltar-card').style.display = index === 0 ? 'none' : 'inline-block';
    document.getElementById('btn-proximo-card').style.display = index === flashcards.length - 1 ? 'none' : 'inline-block';
    document.getElementById('btn-finalizar-flash').style.display = index === flashcards.length - 1 ? 'inline-block' : 'none';
}

function virarCard() {
    document.getElementById('flashcard').classList.toggle('flipped');
}

function avaliar(nivel) {
    avaliacoes[nivel]++;
    
    // Marcar como avaliado
    flashcards[cardAtual].avaliacao = nivel;
    
    // Avançar automaticamente
    if (cardAtual < flashcards.length - 1) {
        proximoCard();
    }
}

function voltarCard() {
    if (cardAtual > 0) {
        mostrarCard(cardAtual - 1);
    }
}

function proximoCard() {
    if (cardAtual < flashcards.length - 1) {
        mostrarCard(cardAtual + 1);
    }
}

function finalizarFlashcards() {
    document.getElementById('flashcard-content').style.display = 'none';
    document.getElementById('resultado-flash').style.display = 'block';
    
    const totalRevisados = avaliacoes.facil + avaliacoes.medio + avaliacoes.dificil;
    
    document.getElementById('total-revisados').textContent = totalRevisados;
    document.getElementById('total-faceis').textContent = avaliacoes.facil;
    document.getElementById('total-medios').textContent = avaliacoes.medio;
    document.getElementById('total-dificeis').textContent = avaliacoes.dificil;
    
    // Recomendação
    let recomendacao = '';
    const percDificil = (avaliacoes.dificil / totalRevisados) * 100;
    
    if (percDificil > 50) {
        recomendacao = '⚠️ Muitos cards difíceis! Revise este deck novamente amanhã e estude o material relacionado.';
    } else if (percDificil > 30) {
        recomendacao = '📚 Alguns cards precisam de mais atenção. Revise os difíceis em 3 dias.';
    } else if (percDificil > 10) {
        recomendacao = '✅ Bom desempenho! Revise este deck em 7 dias.';
    } else {
        recomendacao = '🏆 Excelente! Você domina este conteúdo. Próxima revisão em 14 dias.';
    }
    
    document.getElementById('recomendacao-texto').textContent = recomendacao;
    
    // Salvar estatísticas
    salvarEstatisticas();
}

function salvarEstatisticas() {
    const stats = {
        data: new Date().toISOString(),
        deck: deckSelecionado,
        total: flashcards.length,
        facil: avaliacoes.facil,
        medio: avaliacoes.medio,
        dificil: avaliacoes.dificil
    };
    
    // Salvar no localStorage
    let historico = JSON.parse(localStorage.getItem('flashcards_historico') || '[]');
    historico.push(stats);
    localStorage.setItem('flashcards_historico', JSON.stringify(historico));
}
