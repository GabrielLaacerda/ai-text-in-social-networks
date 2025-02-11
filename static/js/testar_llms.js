function abrirModal() {
    var modal = document.getElementById("modal");
    modal.style.display = "block";
}


function fecharModal() {
    var modal = document.getElementById("modal");
    modal.style.display = "none";
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