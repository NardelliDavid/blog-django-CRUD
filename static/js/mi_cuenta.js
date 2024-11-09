function formNombre() {
  document.getElementById("div-fondo-opaco").classList.toggle("mostrar-div");
  document.getElementById("formNombre").classList.toggle("mostrarForm");
}
function formPassword() {
  document.getElementById("div-fondo-opaco").classList.toggle("mostrar-div");
  document.getElementById("formPassword").classList.toggle("mostrarForm");
}
// Formulario de borrar cuenta
function formBorrarCuenta() {
  document.getElementById("div-fondo-opaco").classList.toggle("mostrar-div");
  document.getElementById("formBorrarCuenta").classList.toggle("mostrarForm");
}
// Mostrar confirmacion
function mostrarConfirmacion() {
  const pass1 = document.getElementById("input-password1").value.trim();
  const pass2 = document.getElementById("input-password2").value.trim();
  if (pass1 == "" || pass2 == "") { // Si 1 de los campos esta vacio no muestra la confirmacion
    alert("Complete los datos faltantes!")
  } else { // Si ambos campos tienen contenido se muestra la confirmacion
    document.getElementById("div-form").classList.toggle("ocultar-div-form");
    document
      .getElementById("div-confirmacion")
      .classList.toggle("mostrar-confirmacion");
  }
  
}
// Boton de cancelacion
function cancelarBoton() {
  formBorrarCuenta();
  // Espera medio segundo para ejecutar la funcion
  setTimeout(() => {
    mostrarConfirmacion();
  }, 150)
}
