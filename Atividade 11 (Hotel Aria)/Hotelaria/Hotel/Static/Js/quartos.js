function toggleExpand(element) {
    element.classList.toggle('expanded');
}

let quartoSelecionado = null;
let novoStatusSelecionado = null;

function mudarStatus(quartoId, novoStatus) {
    quartoSelecionado = quartoId;
    novoStatusSelecionado = novoStatus;

    if (novoStatus === '0') {
        document.getElementById('reservaDate').value = '';
        abrirModalComData();
    } else {
        abrirModal();
    }
}

function confirmarMudanca() {
    const csrftoken = getCookie('csrftoken');

    let dataReserva = null;
    if (novoStatusSelecionado === '0') {
        dataReserva = document.getElementById('reservaDate').value;
        if (!dataReserva) {
            exibirErro("Informe uma data para reservar o quarto.");
            return; // Não fecha a modal
        }
    }

    const bodyData = `id=${quartoSelecionado}&status=${novoStatusSelecionado}${dataReserva ? `&data_reserva=${dataReserva}` : ''}`;

    fetch("/alterar-status-quarto/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: bodyData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            fecharModal();
            fecharModalComData();
            exibirMensagem("Status alterado com sucesso!");
            setTimeout(() => location.reload(), 1500);
        } else {
            fecharModal();
            fecharModalComData();
            exibirErro("Erro ao alterar status: " + data.error);
        }
    })
    .catch(() => {
        fecharModal();
        fecharModalComData();
        exibirErro("Erro na requisição.");
    });
}

function abrirModal() {
    document.getElementById('confirmModal').classList.add('show');
}

function fecharModal() {
    document.getElementById('confirmModal').classList.remove('show');
    quartoSelecionado = null;
    novoStatusSelecionado = null;
}

function abrirModalComData() {
    document.getElementById('confirmModalData').classList.add('show');
}

function fecharModalComData() {
    document.getElementById('confirmModalData').classList.remove('show');
    quartoSelecionado = null;
    novoStatusSelecionado = null;
}

function exibirMensagem(texto) {
    const modal = document.getElementById('messageModal');
    document.getElementById('messageText').textContent = texto;
    modal.classList.add('show');
}

function fecharMensagem() {
    document.getElementById('messageModal').classList.remove('show');
}

function exibirErro(texto) {
    const modal = document.getElementById('errorModal');
    document.getElementById('errorText').textContent = texto;
    modal.classList.add('show');
}

function fecharErro() {
    document.getElementById('errorModal').classList.remove('show');
}

function confirmarExclusaoComModal(form) {
    const modal = document.getElementById('confirmExclusaoModal');
    modal.classList.add('show');
    document.getElementById('confirmarExclusaoBtn').onclick = () => {
        modal.classList.remove('show');
        form.submit();
    };
    document.getElementById('cancelarExclusaoBtn').onclick = () => {
        modal.classList.remove('show');
    };
    return false;
}

function reservarQuarto(quartoId) {
    const dataInput = document.getElementById(`dataReserva-${quartoId}`);
    const dataReserva = dataInput.value;
    const csrftoken = getCookie('csrftoken');

    if (!dataReserva) {
        exibirErro("Informe uma data para reservar o quarto.");
        return;
    }

    fetch("/reservar-quarto/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: `quarto_id=${quartoId}&data_reserva=${dataReserva}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            exibirMensagem("Reserva realizada com sucesso!");
            setTimeout(() => location.reload(), 1500);
        } else {
            exibirErro("Erro: " + data.error);
        }
    })
    .catch(() => {
        exibirErro("Erro na requisição.");
    });
}

function cancelarReservaComModal(form) {
    const modal = document.getElementById('confirmExclusaoModal');
    modal.classList.add('show');

    document.getElementById('confirmarExclusaoBtn').onclick = () => {
        modal.classList.remove('show');
        form.submit();
    };

    document.getElementById('cancelarExclusaoBtn').onclick = () => {
        modal.classList.remove('show');
    };

    return false;
}

function confirmarExclusaoAutomaticaComModal(form) {
    const modal = document.getElementById('confirmExclusaoModal');
    document.getElementById('confirmarExclusaoBtn').onclick = () => {
        modal.classList.remove('show');
        form.submit();
    };
    document.getElementById('cancelarExclusaoBtn').onclick = () => {
        modal.classList.remove('show');
    };
    modal.classList.add('show');
    return false;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}