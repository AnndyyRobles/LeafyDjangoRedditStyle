// Script para aplicar estilos específicos a la vista de sala
document.addEventListener('DOMContentLoaded', function() {
  // Verificar si estamos en la página de sala
  if (document.querySelector('.room-container')) {
    // Aplicar estilos directamente para asegurar que se muestren correctamente
    const roomContainer = document.querySelector('.room-container');
    roomContainer.style.display = 'grid';
    roomContainer.style.gridTemplateColumns = '3fr 1fr';
    roomContainer.style.gap = '30px';
    roomContainer.style.maxWidth = '1300px';
    roomContainer.style.margin = '0 auto';
    roomContainer.style.width = '95%';
    
    // Aplicar estilos a la sala principal
    const room = document.querySelector('.room');
    if (room) {
      room.style.position = 'relative';
      room.style.display = 'flex';
      room.style.flexDirection = 'column';
      room.style.width = '100%';
      room.style.borderRadius = '0.7rem';
      room.style.overflow = 'hidden';
      room.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
    }
    
    // Aplicar estilos a los participantes
    const participants = document.querySelector('.participants');
    if (participants) {
      participants.style.width = '100%';
      participants.style.borderRadius = '0.7rem';
      participants.style.overflow = 'hidden';
      participants.style.display = 'flex';
      participants.style.flexDirection = 'column';
      participants.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
    }
    
    // Aplicar estilos a los hilos de conversación
    const threads = document.querySelector('.threads');
    if (threads) {
      threads.style.width = '100%';
      threads.style.display = 'flex';
      threads.style.flexDirection = 'column';
      threads.style.alignItems = 'stretch';
    }
    
    // Aplicar estilos a cada hilo individual
    const threadElements = document.querySelectorAll('.thread');
    threadElements.forEach(thread => {
      thread.style.width = '100%';
      thread.style.margin = '1rem 0';
      thread.style.padding = '2rem';
      thread.style.borderRadius = '0.7rem';
      thread.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
    });
  }
});
