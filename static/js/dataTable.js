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
