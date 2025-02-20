document.addEventListener("DOMContentLoaded", function () {
    let labelElement = document.getElementById("labelTitulo");

    if (labelElement) {
        document.getElementById("labelTitulo").innerHTML =
        "Escolha o LLM que irá gerar o comentário ou <b>deixe desmarcado para gerar com todos de uma vez</b>:";

    }
});


