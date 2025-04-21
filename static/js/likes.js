// Script para manejar likes sin recargar la página
document.addEventListener('DOMContentLoaded', function() {
  // Seleccionar todos los botones de like
  const likeButtons = document.querySelectorAll('.btn-like');
  console.log('Encontrados botones de like:', likeButtons.length);
  
  // Añadir evento click a cada botón
  likeButtons.forEach(function(button) {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Obtener URL del botón
      const url = this.getAttribute('data-url');
      console.log('Click en like, URL:', url);
      
      // Hacer petición AJAX con fetch
      fetch(url)
        .then(function(response) {
          console.log('Respuesta recibida, status:', response.status);
          return response.json();
        })
        .then(function(data) {
          console.log('Datos JSON:', data);
          // Actualizar contador
          const countElement = button.querySelector('.like-count');
          if (countElement) {
            countElement.textContent = data.count;
            console.log('Contador actualizado a:', data.count);
          }
        })
        .catch(function(error) {
          console.error('Error en la petición:', error);
        });
    });
  });
});
