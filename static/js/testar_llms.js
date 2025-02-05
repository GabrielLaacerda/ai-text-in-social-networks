document.addEventListener('DOMContentLoaded', function () {
    if (typeof estatisticas !== "undefined") {
        var labels = Object.keys(estatisticas);

        // Sumarizando os acertos e erros de todos os detectores
        var totalAcertos = 0;
        var totalErros = 0;

        labels.forEach(detector => {
            totalAcertos += estatisticas[detector].acerto;
            totalErros += estatisticas[detector].erro;
        });

        // Array com os acertos de cada detector
        var acertos = labels.map(detector => estatisticas[detector].acerto);
        var erros = labels.map(detector => estatisticas[detector].erro);

    } else {
        console.error("Dados estatísticos não disponíveis.");
        return;
    }

    // Gráfico de barras
    var ctxBar = document.getElementById('barChart');
    if (ctxBar) {
        ctxBar = ctxBar.getContext('2d');
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Acerto (%)',
                        data: acertos, // Usando os acertos de cada detector
                        backgroundColor: 'rgba(54, 162, 235, 0.6)', // Azul
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Erro (%)',
                        data: erros, // Usando os erros de cada detector
                        backgroundColor: 'rgba(255, 99, 132, 0.6)', // Vermelho
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top' // Posiciona a legenda no topo
                    }
                },
                scales: {
                    x: {
                        stacked: false // Mantém as barras lado a lado
                    },
                    y: {
                        beginAtZero: true // Garante que os valores comecem do zero
                    }
                }
            }
        });
    } else {
        console.error("Elemento #barChart não encontrado.");
    }

    // Gráfico de pizza para mostrar os acertos de cada detector
    var ctxPie = document.getElementById('pieChart');
    if (ctxPie) {
        ctxPie = ctxPie.getContext('2d');
        new Chart(ctxPie, {
            type: 'pie',
            data: {
                labels: labels, // Detectors as labels
                datasets: [{
                    label: 'Acertos por Detector',
                    data: acertos, // Dados de acertos de cada detector
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.6)', // Azul
                        'rgba(255, 99, 132, 0.6)', // Vermelho
                        'rgba(75, 192, 192, 0.6)', // Verde
                        'rgba(153, 102, 255, 0.6)', // Roxo
                        'rgba(255, 159, 64, 0.6)', // Laranja
                        'rgba(255, 205, 86, 0.6)', // Amarelo
                        'rgba(201, 203, 207, 0.6)'  // Cinza
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(201, 203, 207, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top' // Legenda no topo
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2) + '%'; // Mostrar a porcentagem com 2 casas decimais
                            }
                        }
                    }
                }
            }
        });
    } else {
        console.error("Elemento #pieChart não encontrado.");
    }
});

function testar_llms() {
    window.location.href = '/testar_llms';
}

$(document).ready(function () {

    // Inicializa o DataTable
    $('#dataTable').DataTable({
        language: {
            sEmptyTable: "Nenhum dado disponível na tabela",
            sInfo: "Mostrando _START_ até _END_ de _TOTAL_ registros",
            sInfoEmpty: "Mostrando 0 até 0 de 0 registros",
            sInfoFiltered: "(filtrado de _MAX_ registros no total)",
            sLoadingRecords: "Carregando...",
            sProcessing: "Processando...",
            sZeroRecords: "Nenhum registro encontrado",
            sLengthMenu: "Exibir _MENU_ Itens por página",
            sSearch: "Buscar",
            oPaginate: {
                sFirst: "Primeira",
                sPrevious: "Anterior",
                sNext: "Próxima",
                sLast: "Última"
            },
            oAria: {
                sSortAscending: ": ativar para ordenar a coluna de forma ascendente",
                sSortDescending: ": ativar para ordenar a coluna de forma descendente"
            }
        },
        searching: true,
        autoWidth: true,
        paging: true,
        order: [[1, 'asc']],
    });

});