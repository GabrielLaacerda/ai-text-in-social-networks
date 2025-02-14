window.addEventListener('scroll', function () {

    var icon = document.querySelector('.fa-bars');
    var header = document.querySelector('.header-content-personalizado');
    var header2 = document.querySelector('.header-content');

    // Verifica se o ícone e pelo menos um dos cabeçalhos existem
    if (icon && (header || header2)) {
        var headerRect = header ? header.getBoundingClientRect() : null;
        var header2Rect = header2 ? header2.getBoundingClientRect() : null;

        // Verifica se qualquer um dos cabeçalhos foi rolado para fora da tela
        if ((header && headerRect && headerRect.bottom < 0) || (header2 && header2Rect && header2Rect.bottom < 0)) {
            icon.style.setProperty('color', '#2b3c4f', 'important');
        } else {
            icon.style.setProperty('color', 'white', 'important');
        }
    }
});
