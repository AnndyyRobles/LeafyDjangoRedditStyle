// JavaScript para las tu00e9cnicas de cultivo

document.addEventListener('DOMContentLoaded', function() {
  // Establecer la imagen de fondo para la sección hero de técnicas
  const techniqueHero = document.querySelector('.technique-hero');
  if (techniqueHero) {
    const imageUrl = techniqueHero.getAttribute('data-image-url');
    if (imageUrl) {
      techniqueHero.style.backgroundImage = `url('${imageUrl}')`;
    } else {
      // Si no hay imagen, usar un color de fondo por defecto
      techniqueHero.style.backgroundColor = 'var(--color-dark)';
      // Asegurarse de que el degradado se aplique correctamente
      techniqueHero.classList.add('no-image');
    }
  }
  
  // Manejar las pestañas en la página de detalle de técnica
  const tabItems = document.querySelectorAll('.tab-item');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabItems.forEach(item => {
    item.addEventListener('click', function() {
      // Eliminar la clase active de todas las pestañas
      tabItems.forEach(tab => tab.classList.remove('active'));
      tabContents.forEach(content => content.classList.remove('active'));
      
      // Añadir la clase active a la pestaña seleccionada
      this.classList.add('active');
      const tabId = this.getAttribute('data-tab');
      document.getElementById(tabId).classList.add('active');
    });
  });
});
