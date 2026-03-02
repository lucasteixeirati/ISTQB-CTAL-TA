let questoes = [];
let questaoAtual = 0;
let respostas = {};
let tempoInicio = null;
let timerInterval = null;
let tempoTotal = 0;
let capituloSelecionado = { id: 'todos', nome: 'Todos' };

async function iniciarSimulado() {
    const numQuestoes = document.getElementById('num-questoes').value;

    const capSel = document.getElementById('simulado-capitulo');
    capituloSelecionado = {
        id: capSel?.value || 'todos',
        nome: capSel?.selectedOptions?.[0]?.getAttribute('data-label') || capSel?.selectedOptions?.[0]?.textContent || 'Todos'
    };
    
    try {
        const response = await fetch('/api/iniciar-simulado', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                num_questoes: parseInt(numQuestoes),
                capitulo_id: capituloSelecionado.id,
                capitulo_nome: capituloSelecionado.nome,
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            questoes = data.questoes;
            tempoTotal = data.tempo_total * 60; // converter para segundos
            
            document.getElementById('config-simulado').style.display = 'none';
            document.getElementById('simulado-content').style.display = 'block';
            document.getElementById('total-questoes').textContent = questoes.length;
            
            tempoInicio = Date.now();
            iniciarTimer();
            mostrarQuestao(0);
        }
    } catch (error) {
        alert('Erro ao iniciar simulado: ' + error);
    }
}

function iniciarTimer() {
    timerInterval = setInterval(() => {
        const tempoDecorrido = Math.floor((Date.now() - tempoInicio) / 1000);
        const tempoRestante = Math.max(0, tempoTotal - tempoDecorrido);
        
        const minutos = Math.floor(tempoRestante / 60);
        const segundos = tempoRestante % 60;
        
        document.getElementById('timer').textContent = 
            `${String(minutos).padStart(2, '0')}:${String(segundos).padStart(2, '0')}`;
        
        if (tempoRestante === 0) {
            clearInterval(timerInterval);
            alert('Tempo esgotado!');
            finalizarSimulado();
        }
    }, 1000);
}

function mostrarQuestao(index) {
    questaoAtual = index;
    const questao = questoes[index];
    
    document.getElementById('questao-atual').textContent = index + 1;
    document.getElementById('k-level').textContent = questao.k_level;
    document.getElementById('num-questao').textContent = index + 1;
    document.getElementById('questao-texto').textContent = questao.pergunta;
    
    // Renderizar opções
    const opcoesDiv = document.getElementById('opcoes');
    opcoesDiv.innerHTML = '';
    
    Object.entries(questao.opcoes).forEach(([letra, texto]) => {
        const opcaoDiv = document.createElement('div');
        opcaoDiv.className = 'opcao';
        if (respostas[questao.id] === letra) {
            opcaoDiv.classList.add('selecionada');
        }
        opcaoDiv.textContent = `${letra}) ${texto}`;
        opcaoDiv.onclick = () => selecionarResposta(questao.id, letra);
        opcoesDiv.appendChild(opcaoDiv);
    });
    
    // Atualizar botões de navegação
    document.getElementById('btn-voltar').style.display = index === 0 ? 'none' : 'inline-block';
    document.getElementById('btn-avancar').style.display = index === questoes.length - 1 ? 'none' : 'inline-block';
    document.getElementById('btn-finalizar').style.display = index === questoes.length - 1 ? 'inline-block' : 'none';
}

function selecionarResposta(questaoId, letra) {
    respostas[questaoId] = letra;
    
    // Atualizar visual
    document.querySelectorAll('.opcao').forEach(opcao => {
        opcao.classList.remove('selecionada');
    });
    event.target.classList.add('selecionada');
}

function voltarQuestao() {
    if (questaoAtual > 0) {
        mostrarQuestao(questaoAtual - 1);
    }
}

function avancarQuestao() {
    if (questaoAtual < questoes.length - 1) {
        mostrarQuestao(questaoAtual + 1);
    }
}

async function finalizarSimulado() {
    if (!confirm('Tem certeza que deseja finalizar o simulado?')) {
        return;
    }
    
    clearInterval(timerInterval);
    
    const tempoGasto = Math.floor((Date.now() - tempoInicio) / 60000); // minutos
    
    try {
        const response = await fetch('/api/finalizar-simulado', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                respostas: respostas,
                tempo_gasto: tempoGasto
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            mostrarResultado(data);
        }
    } catch (error) {
        alert('Erro ao finalizar simulado: ' + error);
    }
}

function mostrarResultado(data) {
    document.getElementById('simulado-content').style.display = 'none';
    document.getElementById('resultado').style.display = 'block';
    
    document.getElementById('resultado-titulo').textContent = 
        data.aprovado ? '✅ APROVADO!' : '❌ REPROVADO';
    document.getElementById('resultado-titulo').style.color = 
        data.aprovado ? '#27ae60' : '#e74c3c';
    
    document.getElementById('acertos').textContent = `${data.acertos}/${data.total}`;
    document.getElementById('percentual').textContent = `${data.percentual}%`;
    document.getElementById('status').textContent = data.aprovado ? 'APROVADO' : 'REPROVADO';
    document.getElementById('status').style.color = data.aprovado ? '#27ae60' : '#e74c3c';
    
    // Mostrar revisão das questões
    const revisaoDiv = document.getElementById('revisao-questoes');
    revisaoDiv.innerHTML = '<h3>Revisão das Questões</h3>';
    
    data.resultados.forEach((q, index) => {
        const questaoDiv = document.createElement('div');
        questaoDiv.className = `questao-revisao ${q.correto ? 'correta' : 'errada'}`;
        
        questaoDiv.innerHTML = `
            <h4>Questão ${index + 1} - ${q.correto ? '✅ Correto' : '❌ Errado'}</h4>
            <p><strong>${q.pergunta}</strong></p>
            <p>Sua resposta: <strong>${q.resposta_usuario || 'Não respondida'}</strong></p>
            <p>Resposta correta: <strong>${q.resposta_correta}</strong></p>
            <p><em>${q.justificativa}</em></p>
        `;
        
        revisaoDiv.appendChild(questaoDiv);
    });
}
