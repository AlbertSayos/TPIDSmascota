
window.addEventListener('DOMContentLoaded', function() {
    var currentPage = window.location.pathname;
    // Verificar si estamos en la página específica
    if (currentPage.includes('/login')) {
      var boton = document.getElementById('petbutton');
      boton.style.display = 'none'; 
    }
});