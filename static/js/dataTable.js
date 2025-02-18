$(document).ready(function () {
    $('#dataTable').DataTable({
        responsive: true,  // Torna a tabela responsiva
        autoWidth: false,
        paging: false,         // Desativa paginação
        searching: false,      // Remove a barra de pesquisa
        ordering: false,       // Remove ordenação das colunas
        info: false,           // Remove o texto "Mostrando X de Y registros"
        lengthChange: false,   // Remove a opção de alterar a quantidade de linhas exibidas
        language: {
            emptyTable: "Nenhum dado disponível na tabela"
        }
    });
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