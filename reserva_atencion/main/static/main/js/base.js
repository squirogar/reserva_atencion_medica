//boton de scroll automático para que el usuario no tenga que hacer scroll manual
const btnScroll = document.getElementById("btnScroll");

// Mostrar el botón cuando se hace scroll hacia abajo
window.onscroll = function() {
    // pregunta si la página verticalmente se ha movido más de 20 pixeles hacia abajo 
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        btnScroll.style.display = "block";
    } else {
        btnScroll.style.display = "none";
    }
};

// Función para ir al principio de la página
btnScroll.onclick = function() {
    window.scrollTo({
        top: 0,
        behavior: "smooth" // Hace que el scroll sea suave
    });
};
