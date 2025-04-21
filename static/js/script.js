// // Actions:

// const closeButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>remove</title>
// <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
// </svg>
// `;
// const menuButton = `<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
// <title>ellipsis-horizontal</title>
// <path d="M16 7.843c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 1.98c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 19.908c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 14.046c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// <path d="M16 31.974c-2.156 0-3.908-1.753-3.908-3.908s1.753-3.908 3.908-3.908c2.156 0 3.908 1.753 3.908 3.908s-1.753 3.908-3.908 3.908zM16 26.111c-1.077 0-1.954 0.877-1.954 1.954s0.877 1.954 1.954 1.954c1.077 0 1.954-0.877 1.954-1.954s-0.877-1.954-1.954-1.954z"></path>
// </svg>
// `;

// const actionButtons = document.querySelectorAll('.action-button');

// if (actionButtons) {
//   actionButtons.forEach(button => {
//     button.addEventListener('click', () => {
//       const buttonId = button.dataset.id;
//       let popup = document.querySelector(`.popup-${buttonId}`);
//       console.log(popup);
//       if (popup) {
//         button.innerHTML = menuButton;
//         return popup.remove();
//       }

//       const deleteUrl = button.dataset.deleteUrl;
//       const editUrl = button.dataset.editUrl;
//       button.innerHTML = closeButton;

//       popup = document.createElement('div');
//       popup.classList.add('popup');
//       popup.classList.add(`popup-${buttonId}`);
//       popup.innerHTML = `<a href="${editUrl}">Edit</a>
//       <form action="${deleteUrl}" method="delete">
//         <button type="submit">Delete</button>
//       </form>`;
//       button.insertAdjacentElement('afterend', popup);
//     });
//   });
// }

// Menu

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

// Solución simple para likes
function handleLikes() {
  // Buscar todos los botones de like
  const likeButtons = document.querySelectorAll('.btn-like');
  console.log('Encontrados botones de like:', likeButtons.length);
  
  // Añadir evento click a cada botón
  for (let i = 0; i < likeButtons.length; i++) {
    likeButtons[i].onclick = function(e) {
      e.preventDefault();
      
      // Verificar si el usuario está autenticado
      if (!this.hasAttribute('data-user-authenticated')) {
        alert('Debes iniciar sesión para dar like');
        return false;
      }
      
      // Obtener URL del botón
      const url = this.getAttribute('data-url');
      console.log('Click en like, URL:', url);
      
      // Crear elemento iframe oculto para hacer la petición sin recargar la página
      const iframe = document.createElement('iframe');
      iframe.style.display = 'none';
      document.body.appendChild(iframe);
      
      // Obtener estado actual del like
      const isLiked = this.classList.contains('liked');
      const iconElement = this.querySelector('.leaf-icon');
      const countElement = this.querySelector('.like-count');
      
      // Actualizar contador y apariencia inmediatamente
      if (countElement) {
        const currentCount = parseInt(countElement.textContent) || 0;
        // Si ya está dado like, restar 1; si no, sumar 1
        countElement.textContent = isLiked ? currentCount - 1 : currentCount + 1;
      }
      
      // Cambiar apariencia del botón
      this.classList.toggle('liked');
      
      // Cargar la URL en el iframe
      iframe.src = url;
      
      // Eliminar el iframe después de un tiempo
      setTimeout(function() {
        document.body.removeChild(iframe);
      }, 1000);
      
      return false;
    };
  }
}

// Ejecutar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', handleLikes);
// También ejecutar ahora por si el DOM ya está cargado
handleLikes();
