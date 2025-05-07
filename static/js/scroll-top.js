// Función para manejar el botón de volver arriba
document.addEventListener('DOMContentLoaded', function() {
    // Crear el botón
    const scrollTopButton = document.createElement('button');
    scrollTopButton.id = 'scroll-top-btn';
    
    // Crear la flecha hacia arriba usando un span
    const arrow = document.createElement('span');
    arrow.className = 'arrow';
    scrollTopButton.appendChild(arrow);
    
    // Añadir el botón al body
    document.body.appendChild(scrollTopButton);
    
    // Mostrar/ocultar el botón según la posición de scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopButton.classList.add('show');
        } else {
            scrollTopButton.classList.remove('show');
        }
    });
    
    // Añadir funcionalidad de scroll al hacer clic
    scrollTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});