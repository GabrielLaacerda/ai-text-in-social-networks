console.log("O JavaScript externo foi carregado corretamente!");

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

    // Estilo do pop-up
    setTimeout(() => {
        popup.style.opacity = 0;
        setTimeout(() => popup.remove(), 1000); // Remove o pop-up após ele desaparecer
    }, 3000); // O pop-up desaparecerá após 3 segundos
}
