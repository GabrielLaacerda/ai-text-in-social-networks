document.addEventListener('DOMContentLoaded', function() {
    var ctxBar = document.getElementById('barChart');
    if (ctxBar) {
        ctxBar = ctxBar.getContext('2d');
        var barChart = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ['Cohere', 'ChatGPT', 'Gemini', 'Llama','MaritacaIA','MistralAI'],
                datasets: [{
                    label: 'Índice de acertos',
                    data: [50, 100, 75, 99, 40, 83],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            }
        });
    } else {
        console.error("Elemento #barChart não encontrado.");
    }

    var ctxPie = document.getElementById('pieChart');
    if (ctxPie) {
        ctxPie = ctxPie.getContext('2d');
        var pieChart = new Chart(ctxPie, {
            type: 'pie',
            data: {
                labels: ['Cohere', 'ChatGPT', 'Gemini', 'Llama','MaritacaIA','MistralAI'],
                datasets: [{
                    label: 'Índice de acertos',
                    data: [50, 100, 75, 120,45],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(75, 192, 192, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: {
                        position: 'right' // Coloca a legenda à direita
                    }
                }
            }
        });
    } else {
        console.error("Elemento #pieChart não encontrado.");
    }


});


$(document).ready(function () {
    $('#dataTable').DataTable({
        language: {
            sEmptyTable: "Nenhum dado disponível na tabela",
            sInfo: "Mostrando _START_ até _END_ de _TOTAL_ registros",
            sInfoEmpty: "Mostrando 0 até 0 de 0 registros",
            sInfoFiltered: "(filtrado de _MAX_ registros no total)",
            sInfoPostFix: "",

            sLoadingRecords: "Carregando...",
            sProcessing: "Processando...",
            sSearch: "Pesquisar:",
            sZeroRecords: "Nenhum registro encontrado",
            sLengthMenu: "Exibir _MENU_ Itens por página",
            oPaginate: {
                sFirst: "",
                sPrevious: "",
                sNext: "",
                sLast: ""
            },
            oAria: {
                sSortAscending: ": ativar para ordenar a coluna de forma ascendente",
                sSortDescending: ": ativar para ordenar a coluna de forma descendente"
            }
        }
    });
});
