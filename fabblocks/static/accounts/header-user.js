$(document).ready(function() {
// Cuando se haga clic en una opción del modal de placas
$('#placasModal').on('click', '.dropdown-item', function() {
    // Obtener el texto de la opción seleccionada
    var placaSeleccionada = $(this).text();
    
    // Actualizar el mensaje de la placa seleccionada
    $('#placaSeleccionadaMensaje').text('Placa seleccionada: ' + placaSeleccionada);
});
});