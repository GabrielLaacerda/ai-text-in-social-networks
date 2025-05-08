document.addEventListener('DOMContentLoaded', function () {
    // Gráfico de barras para estatisticas_barras
    if (typeof estatisticas_barras !== "undefined") {
    var labelsBarras = Object.keys(estatisticas_barras);

    var estatisticasOrdenadasBarras = labelsBarras.map(detector => ({
        nome: detector,
        acerto: estatisticas_barras[detector].acerto,
        erro: estatisticas_barras[detector].erro
    })).sort((a, b) => b.acerto - a.acerto);

    var labelsOrdenadasBarras = estatisticasOrdenadasBarras.map(item => item.nome);
    var acertosOrdenadosBarras = estatisticasOrdenadasBarras.map(item => item.acerto);
    var errosOrdenadosBarras = estatisticasOrdenadasBarras.map(item => item.erro);

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
                        backgroundColor: 'rgba(76, 175, 80, 0.9)',    // Verde vibrante
                        borderColor: 'rgba(56, 142, 60, 1)',
                        borderWidth: 1,
                        stack: 'Stack 0'
                    },
                    {
                        label: 'Erro (%)',
                        data: errosOrdenadosBarras,
                        backgroundColor: 'rgba(244, 67, 54, 0.9)',    // Vermelho vibrante
                        borderColor: 'rgba(211, 47, 47, 1)',
                        borderWidth: 1,
                        stack: 'Stack 0'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    },
                    datalabels: {
                        anchor: 'center',
                        align: 'center',
                        color: 'white',
                        font: {
                            weight: 'bold',
                            size: 14
                        },
                        formatter: function(value, context) {
                            if (context.dataset.label === 'Acerto (%)') {
                                return value.toFixed(1) + '%';
                            }
                            return '';
                        }
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Detectores',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        ticks: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Taxa de Sucesso na Detecção (%)',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        ticks: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    }
                }
            },
            plugins: [ChartDataLabels]
        });
    } else {
        console.error("Elemento #barChartBarras não encontrado.");
    }
} else {
    console.error("Dados estatísticos para o gráfico de barras não disponíveis.");
}

    // Gráfico de barras para estatisticas (LLMs)
    if (typeof estatisticas !== "undefined") {
    var labelsLLMs = Object.keys(estatisticas);

    var estatisticasOrdenadasLLMs = labelsLLMs.map(llm => ({
        nome: llm,
        acerto: estatisticas[llm].acerto,
        erro: estatisticas[llm].erro
    })).sort((a, b) => b.acerto - a.acerto);

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
                        backgroundColor: 'rgba(76, 175, 80, 0.9)',    // Verde vibrante
                        borderColor: 'rgba(56, 142, 60, 1)',
                        borderWidth: 1,
                        stack: 'Stack 0'
                    },
                    {
                        label: 'Fracasso (%)',
                        data: errosOrdenadosLLMs,
                        backgroundColor: 'rgba(244, 67, 54, 0.9)',    // Vermelho vibrante
                        borderColor: 'rgba(211, 47, 47, 1)',
                        borderWidth: 1,
                        stack: 'Stack 0'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (tooltipItem) {
                                return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                            }
                        }
                    },
                    datalabels: {
                        anchor: 'center',
                        align: 'center',
                        color: 'white',
                        font: {
                            weight: 'bold',
                            size: 14
                        },
                        formatter: function (value, context) {
                            if (context.dataset.label === 'Sucesso (%)') {
                                return value.toFixed(1) + '%';
                            }
                            return '';
                        }
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Modelos de Geração',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        ticks: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Sucesso de cada LLM se passando por humano (%)',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        ticks: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    }
                }
            },
            plugins: [ChartDataLabels]
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

    var estatisticasPorTema = {};
    estatisticas_desempenho_detector.forEach(item => {
        if (!estatisticasPorTema[item.tema]) {
            estatisticasPorTema[item.tema] = {};
        }
        estatisticasPorTema[item.tema][item.detector] = item.media_efetividade || 0;
    });

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
                    legend: {
                        position: 'top',
                        labels: {
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (tooltipItem) {
                                return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Detectores',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        ticks: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Taxa de acerto na detecção por tema (%)',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        ticks: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            },
                            color: '#333'
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

        const corPorTema2 = {};
        temas.forEach((tema, index) => {
            corPorTema2[tema] = coresDisponiveis[index % coresDisponiveis.length];
        });


    // Ordenação em blocos de 5
    function ordenarEmBlocos(llms, estatisticas, bloco = 5) {
        let ordenado = [];
        let novosLabels = [];

        for (let i = 0; i < llms.length; i += bloco) {
            let subArray = llms.slice(i, i + bloco).map(llm => ({
                llm: llm,
                valores: temas.map(tema => estatisticas[llm][tema] || 0)
            }));

            subArray.sort((a, b) => b.valores.reduce((x, y) => x + y, 0) - a.valores.reduce((x, y) => x + y, 0));

            ordenado.push(...subArray);
            novosLabels.push(...subArray.map(item => item.llm));
        }

        return { ordenado, novosLabels };
    }

    // Ordena os LLMs em blocos de 5
    let { ordenado, novosLabels } = ordenarEmBlocos(llms, estatisticasPorTemaPorLLM);

    // Criar datasets ordenados
    var datasets = temas.map((tema, index) => ({
        label: tema,
        data: ordenado.map(item => item.valores[index]),
        backgroundColor: corPorTema2[tema],
        borderColor: corPorTema2[tema].replace('0.6', '1'),
        borderWidth: 1,
        barPercentage: 0.5,
        categoryPercentage: 0.8
    }));

    // Criar gráfico apenas se o elemento existir
    var ctxLLM = document.getElementById('barChartLLM');
    if (ctxLLM) {
        ctxLLM = ctxLLM.getContext('2d');

        new Chart(ctxLLM, {
            type: 'bar',
            data: {
                labels: novosLabels,
                datasets: datasets
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (tooltipItem) {
                                return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toFixed(2) + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'LLMs',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        ticks: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            },
                            color: '#333'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Taxa de acerto ao se passar por humano (%)',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#333'
                        },
                        ticks: {
                            font: {
                                size: 14,
                                weight: 'bold'
                            },
                            color: '#333'
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

