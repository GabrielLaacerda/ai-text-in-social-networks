document.addEventListener('DOMContentLoaded', function () {
    if (typeof probabilidades !== "undefined") {
        var labelsBarras = Object.keys(probabilidades);

        // Criar um array de objetos contendo nome, acerto e erro
        var estatisticasOrdenadasBarras = labelsBarras.map(detector => ({
            nome: detector,
            acerto: probabilidades[detector].acerto,
            erro: probabilidades[detector].erro
        })).sort((a, b) => b.acerto - a.acerto); // Ordenar do maior para o menor acerto

        // Extrair as informações já ordenadas
        var labelsOrdenadasBarras = estatisticasOrdenadasBarras.map(item => item.nome);
        var acertosOrdenadosBarras = estatisticasOrdenadasBarras.map(item => item.acerto);
        var errosOrdenadosBarras = estatisticasOrdenadasBarras.map(item => item.erro);

        // Selecionar o canvas do gráfico
        var ctxBarBarras = document.getElementById('barChartBarras');
        if (ctxBarBarras) {
            ctxBarBarras = ctxBarBarras.getContext('2d');

            new Chart(ctxBarBarras, {
                type: 'bar',
                data: {
                    labels: labelsOrdenadasBarras,
                    datasets: [
                        {
                            label: 'Humano (%)',
                            data: acertosOrdenadosBarras,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)', // Azul
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                            stack: 'Stack 0'
                        },
                        {
                            label: 'IA (%)',
                            data: errosOrdenadosBarras,
                            backgroundColor: 'rgba(255, 99, 132, 0.8)', // Vermelho
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                            stack: 'Stack 0' // Empilhar erro dentro da mesma barra
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'top' }
                    },
                    scales: {
                            x: { stacked: true },
                            y: { beginAtZero: true, title: { display: true, text: 'Taxa de detecção dos comentários por cada detector(%)' } }
                   }
                }
            });

        } else {
            console.error("Elemento #barChartBarras não encontrado.");
        }
    } else {
        console.error("Dados estatísticos para o gráfico de barras (barras) não disponíveis.");
    }

})

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

function abrirModal() {
    var modal = document.getElementById("modal");
    modal.style.display = "block";
}