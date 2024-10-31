function getCSRFToken() { // Obtiene el CSRF-TOKEN
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
}
function guardarPublicacion(event) {
  const boton = event.currentTarget;
  const publicacionId = boton.getAttribute("data-id"); // Obtiene el atributo data-id
  const icono = document.getElementById(`guardar-icono-${publicacionId}`); // Obtiene el id de la imagen adentro del boton de guardar
  const urlGuardado = "/static/icons/guardado.png"; // Ruta absoluta
  const urlNoGuardado = "/static/icons/no-guardado.png"; // Ruta absoluta

  fetch(`/guardar_publicacion/${publicacionId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(),
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      // Redirige si el codigo de error es 401
      if (response.status === 401) {
        window.location.href = "/login_vista";
        return 0; // Evita que se ejecute el resto de la función
      }
      return response.json();
    })
    .then((data) => {
      if (data.estado === "guardado") {
        icono.src = urlGuardado; // Si el estado es guardado pone la imagen de guardado
      } else if (data.estado === "eliminado") {
        icono.src = urlNoGuardado; // Si el estado es no guardado pone la imagen de no guardado
      } else if (data.error) {
        alert("Error: " + data.error);
      } 
    })
    .catch((error) => console.error("Error al guardar:", error));
}
