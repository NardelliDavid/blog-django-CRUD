function eliminarPostConfirmacion(idPost) {
    // Muestra el fondo opaco
    document.getElementById("div-fondo-oscuro").classList.toggle("mostrar-fondo")
    // Muestra el div de confirmacion
  document
    .getElementById("eliminarPostConfirmacion-" + idPost)
    .classList.toggle("mostrar");
    // Modifica el scroll de la pagina
    if (document.body.style.overflow == "hidden") {
        document.body.style.overflow = "auto";
    } else {
        document.body.style.overflow = "hidden";
    }
}

function editarPost(idPost) {
  // Muestra el fondo opaco
  document.getElementById("div-fondo-oscuro").classList.toggle("mostrar-fondo");
  // Muestra el formulario
  document.getElementById("editarPost-" + idPost).classList.toggle("mostrar");
  // Modifica el scroll de la pagina
  if (document.body.style.overflow == "hidden") {
    document.body.style.overflow = "auto";
  } else {
    document.body.style.overflow = "hidden";
  }
}