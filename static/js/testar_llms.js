// Função para mostrar a mensagem de sucesso no canto superior direito
function showPopup(message) {
    const popup = document.getElementById('popupSucesso');
    popup.textContent = message;
    popup.style.display = 'block';

    // Oculta o pop-up após 3 segundos
    setTimeout(function () {
        popup.style.display = 'none';
    }, 3000);
}

// Função chamada ao enviar o formulário
function sendFormData(event) {
    event.preventDefault();

    // Exibe o pop-up de espera
    document.getElementById('modal').style.display = 'block';

    // Cria o FormData com os dados do formulário
    const formData = new FormData(document.getElementById('llm-form'));

    // Realiza a requisição POST
    fetch('/testar_llms', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Exibe a mensagem de sucesso
            showPopup("Arquivo gerado com sucesso!");
        }

        // Oculta o pop-up de espera
        document.getElementById('modal').style.display = 'none';
    })
    .catch(error => {
        console.error('Erro:', error);
        // Oculta o pop-up de espera
        document.getElementById('modal').style.display = 'none';
    });
}


// Quando o DOM estiver pronto, configura o DataTables
$(document).ready(function () {
    $('#myTable').DataTable({
        paging: false, // Desativa paginação
        searching: false, // Remove o campo de busca
        info: false, // Remove informações de exibição (ex.: "Mostrando X de Y")
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.5/i18n/pt-BR.json"
        }
    });
});
