function iniciarDownload(file_path) {
    const novaJanela = window.open("", "_blank");
    novaJanela.document.write("<h1>Download em andamento...</h1>");
    const link = novaJanela.document.createElement("a");
    link.href = "/download?file_path=" + file_path;  // Passa o caminho do arquivo gerado
    link.download = file_path;  // Nome do arquivo ao fazer o download
    link.click();  // Inicia o download automaticamente
    novaJanela.document.close();
}