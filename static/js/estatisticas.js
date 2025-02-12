document.addEventListener('DOMContentLoaded', function () {
    // Gráfico de barras para estatisticas_barras
    if (typeof estatisticas_barras !== "undefined") {
        var labelsBarras = Object.keys(estatisticas_barras);

        // Criar um array de objetos contendo nome, acerto e erro
        var estatisticasOrdenadasBarras = labelsBarras.map(detector => ({
            nome: detector,
            acerto: estatisticas_barras[detector].acerto,
            erro: estatisticas_barras[detector].erro
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
                            label: 'Acerto (%)',
                            data: acertosOrdenadosBarras,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)', // Azul
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                            stack: 'Stack 0'
                        },
                        {
                            label: 'Erro (%)',
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
                    plugins: {
                        legend: { position: 'top' }
                    },
                    scales: {
                        x: { stacked: true },
                        y: { beginAtZero: true, title: { display: true, text: 'Taxa de acerto nas ferramentas de detecção (%)' } }
                    }
                }
            });

        } else {
            console.error("Elemento #barChartBarras não encontrado.");
        }
    } else {
        console.error("Dados estatísticos para o gráfico de barras (barras) não disponíveis.");
    }

    // Gráfico de barras para estatisticas (LLMs)
    if (typeof estatisticas !== "undefined") {
        var labelsLLMs = Object.keys(estatisticas);

        var estatisticasOrdenadasLLMs = labelsLLMs.map(llm => ({
            nome: llm,
            acerto: estatisticas[llm].acerto,
            erro: estatisticas[llm].erro
        })).sort((a, b) => b.acerto - a.acerto); // Ordenar do maior para o menor acerto

        var labelsOrdenadasLLMs = estatisticasOrdenadasLLMs.map(item => item.nome);
        var acertosOrdenadosLLMs = estatisticasOrdenadasLLMs.map(item => item.acerto);
        var errosOrdenadosLLMs = estatisticasOrdenadasLLMs.map(item => item.erro);

        var ctxBarLLMs = document.getElementById('barChartLLMs');
        if (ctxBarLLMs) {
            ctxBarLLMs = ctxBarLLMs.getContext('2d');

            new Chart(ctxBarLLMs, {
                type: 'bar',
                data: {
                    labels: labelsOrdenadasLLMs,
                    datasets: [
                        {
                            label: 'Sucesso (%)',
                            data: acertosOrdenadosLLMs,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)', // Azul
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                            stack: 'Stack 0'
                        },
                        {
                            label: 'Fracasso (%)',
                            data: errosOrdenadosLLMs,
                            backgroundColor: 'rgba(255, 99, 132, 0.8)', // Vermelho
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                            stack: 'Stack 0'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' },
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                                }
                            }
                        }
                    },
                    scales: {
                        x: { stacked: true },
                        y: {
                        beginAtZero: true,
                        title: { display: true,
                            text: 'Sucesso de cada LLM se passando por humano'
                           }
                        }
                    }
                }
            });

        } else {
            console.error("Elemento #barChartLLMs não encontrado.");
        }
    } else {
        console.error("Dados estatísticos para o gráfico de barras (LLMs) não disponíveis.");
    }

    // Gráfico de desempenho por detector
    if (typeof estatisticas_desempenho_detector !== "undefined") {
        var detectores = [...new Set(estatisticas_desempenho_detector.map(item => item.detector))];
        var temas = [...new Set(estatisticas_desempenho_detector.map(item => item.tema))];

        // Organiza os dados para o gráfico
        var estatisticasPorTema = {};

        estatisticas_desempenho_detector.forEach(item => {
            if (!estatisticasPorTema[item.tema]) {
                estatisticasPorTema[item.tema] = {};
            }
            estatisticasPorTema[item.tema][item.detector] = item.media_efetividade || 0;
        });

        // Mapeamento de cores para cada tema
        const coresDisponiveis = [
            'rgba(54, 162, 235, 0.6)',  // Azul
            'rgba(255, 99, 132, 0.6)',  // Rosa
            'rgba(75, 192, 192, 0.6)',  // Verde
            'rgba(255, 206, 86, 0.6)',  // Amarelo
            'rgba(153, 102, 255, 0.6)', // Roxo
            'rgba(255, 159, 64, 0.6)'   // Laranja
        ];

        const corPorTema = {};
        temas.forEach((tema, index) => {
            corPorTema[tema] = coresDisponiveis[index % coresDisponiveis.length];
        });

        var ctxBar = document.getElementById('barChart');
        if (ctxBar) {
            ctxBar = ctxBar.getContext('2d');

            var datasets = temas.map(tema => {
                return {
                    label: tema,
                    data: detectores.map(detector => estatisticasPorTema[tema][detector] || 0),
                    backgroundColor: corPorTema[tema],
                    borderColor: corPorTema[tema].replace('0.6', '1'),
                    borderWidth: 1,
                    barPercentage: 0.5,
                    categoryPercentage: 0.8
                };
            });

            new Chart(ctxBar, {
                type: 'bar',
                data: {
                    labels: detectores,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Detectores',
                                font: { size: 14, weight: 'bold' }
                            }
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Taxa de acerto na detecção por tema(%)',
                                font: { size: 14, weight: 'bold' }
                            }
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

    // Gráfico de LLM por Tema
    if (typeof resultados_llm_tema !== "undefined") {
        // Extrai as LLMs e temas únicos
        var llms = [...new Set(resultados_llm_tema.map(item => item.llm))];
        var temas = [...new Set(resultados_llm_tema.map(item => item.tema))];

        // Organiza os dados para o gráfico
        var estatisticasPorTemaPorLLM = {};

        resultados_llm_tema.forEach(item => {
            if (!estatisticasPorTemaPorLLM[item.llm]) {
                estatisticasPorTemaPorLLM[item.llm] = {};
            }
            estatisticasPorTemaPorLLM[item.llm][item.tema] = item.media_prob_humano || 0;
        });

        // Mapeamento de cores para cada tema
        const coresDisponiveis = [
            'rgba(54, 162, 235, 0.6)',  // Azul
            'rgba(255, 99, 132, 0.6)',  // Rosa
            'rgba(75, 192, 192, 0.6)',  // Verde
            'rgba(255, 206, 86, 0.6)',  // Amarelo
            'rgba(153, 102, 255, 0.6)', // Roxo
            'rgba(255, 159, 64, 0.6)'   // Laranja
        ];

        const corPorTema = {};
        temas.forEach((tema, index) => {
            corPorTema[tema] = coresDisponiveis[index % coresDisponiveis.length];
        });

        var ctxLLM = document.getElementById('barChartLLM');
        if (ctxLLM) {
            ctxLLM = ctxLLM.getContext('2d');

            var datasets = temas.map(tema => {
                return {
                    label: tema,
                    data: llms.map(llm => estatisticasPorTemaPorLLM[llm][tema] || 0),
                    backgroundColor: corPorTema[tema],
                    borderColor: corPorTema[tema].replace('0.6', '1'),
                    borderWidth: 1,
                    barPercentage: 0.5,
                    categoryPercentage: 0.8
                };
            });

            new Chart(ctxLLM, {
                type: 'bar',
                data: {
                    labels: llms,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'LLMs',
                                font: { size: 14, weight: 'bold' }
                            }
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Probabilidade de passar por humano (%)',
                                font: { size: 14, weight: 'bold' }
                            }
                        }
                    }
                }
            });
        } else {
            console.error("Elemento #barChartLLM não encontrado.");
        }
    } else {
        console.error("Dados estatísticos para o gráfico de LLM por tema não disponíveis.");
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
                sSortAscending: ": ativar para ordenar a coluna de forma crescente",
                sSortDescending: ": ativar para ordenar a coluna de forma decrescente"
            }
        }
    });
});
