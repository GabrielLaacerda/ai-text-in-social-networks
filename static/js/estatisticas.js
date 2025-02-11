document.addEventListener('DOMContentLoaded', function () {

    if (typeof estatisticas_barras !== "undefined") {
        var labels = Object.keys(estatisticas_barras); // Extrai os nomes dos detectores

        // Arrays de acertos e erros de cada detector
        var acertos = labels.map(detector => estatisticas_barras[detector].acerto);
        var erros = labels.map(detector => estatisticas_barras[detector].erro);

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
                            data: acertos,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        },
                        {
                            label: 'Erro (%)',
                            data: erros,
                            backgroundColor: 'rgba(255, 99, 132, 0.6)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top'
                        }
                    },
                    scales: {
                        x: {
                            stacked: false
                        },
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        } else {
            console.error("Elemento #barChart não encontrado.");
        }
    } else {
        console.error("Dados estatísticos para o gráfico de barras não disponíveis.");
    }

    if (typeof estatisticas !== "undefined") {
        var labelsPie = Object.keys(estatisticas);
        var acertosPie = labelsPie.map(detector => estatisticas[detector].acerto);

        var ctxPie = document.getElementById('pieChart');
        if (ctxPie) {
            ctxPie = ctxPie.getContext('2d');
            new Chart(ctxPie, {
                type: 'pie',
                data: {
                    labels: labelsPie,
                    datasets: [{
                        label: 'Acertos por Detector',
                        data: acertosPie,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.6)',
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(75, 192, 192, 0.6)',
                            'rgba(153, 102, 255, 0.6)',
                            'rgba(255, 159, 64, 0.6)',
                            'rgba(255, 205, 86, 0.6)',
                            'rgba(201, 203, 207, 0.6)'
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
                            position: 'top'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(tooltipItem) {
                                    return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                                }
                            }
                        }
                    }
                }
            });
        } else {
            console.error("Elemento #pieChart não encontrado.");
        }
    } else {
        console.error("Dados estatísticos para o gráfico de pizza não disponíveis.");
    }
});



function detectores() {
    window.location.href = '/detectores';
}

$(document).ready(function () {
    var table = $('#dataTable').DataTable({
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
