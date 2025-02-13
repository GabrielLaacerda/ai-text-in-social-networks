function abrirModal() {
    var modal = document.getElementById("modal");
    modal.style.display = "block";
}

function fecharModal() {
    var modal = document.getElementById("modal");
    modal.style.display = "none";
}

function iniciarDownload(file_path) {
    const novaJanela = window.open("", "_blank");
    novaJanela.document.write("<h1>Download em andamento...</h1>");
    const link = novaJanela.document.createElement("a");
    link.href = "/download?file_path=" + file_path;  // Passa o caminho do arquivo gerado
    link.download = "comentarios_gerados.txt";  // Nome do arquivo ao fazer o download
    link.click();  // Inicia o download automaticamente
    novaJanela.document.close();
}

document.addEventListener("DOMContentLoaded", () => {

    const selectElement = document.getElementById('themes');

    selectElement.addEventListener('change', () => {
        const defaultOption = selectElement.querySelector('option[value=""]');
        if (defaultOption) {
            defaultOption.style.display = 'none'; // Oculta a opção padrão
        }
    });
});

function handleThemeSelection(selectElement) {
    const selectedValue = selectElement.value;
    if (selectedValue) {
        fetch(`/load_json?file=${selectedValue}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erro ao carregar o arquivo JSON");
                }
                return response.json();
            })
            .then(data => {
                console.log("Conteúdo do JSON carregado:", data);
                showPopup("JSON carregado com sucesso!", "success");
            })
            .catch(error => {
                console.error("Erro ao carregar o JSON:", error);
                showPopup("Não foi possível carregar o arquivo JSON.", "error");
            });
    }
}

function showPopup(message, type) {
    // Criação do pop-up
    const popup = document.createElement("div");
    popup.className = `popup ${type}`;
    popup.textContent = message;

    // Adicionando o pop-up ao corpo do documento
    document.body.appendChild(popup);

    // Estilos para posicionar o pop-up no canto superior direito
    popup.style.position = 'fixed';
    popup.style.top = '20px'; // Distância de 20px do topo
    popup.style.right = '20px'; // Distância de 20px da direita
    popup.style.backgroundColor = 'green'; // Fundo verde
    popup.style.color = 'white'; // Cor do texto
    popup.style.padding = '10px'; // Espaçamento interno
    popup.style.borderRadius = '8px'; // Borda arredondada
    popup.style.zIndex = '9999'; // Fica acima de outros elementos
    popup.style.opacity = '1'; // Começa com visibilidade total

    // Fazendo o pop-up desaparecer após 3 segundos
    setTimeout(() => {
        popup.style.opacity = 0;
        setTimeout(() => popup.remove(), 1000); // Remove após desaparecer
    }, 3000); // Desaparece após 3 segundos
}

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