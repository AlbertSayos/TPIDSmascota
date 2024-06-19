async function moduloDeTablas() {
    var MarcasDeMascotasYCasas = {};

    async function traerDatosDeMarcas() {
        try {
            let respuesta = await fetch('/cargarTablas');
            if (!respuesta.ok) {
                throw new Error('Network response was not ok');
            }
            let sigRespuesta = await respuesta.json();
            // Asumiendo que sigRespuesta es un array con dos objetos: uno para tablaDeMascota y otro para tablaDeCasas
            MarcasDeMascotasYCasas = [
                { tablaDeMascota: sigRespuesta[0].tablaDeMascota || [] },
                { tablaDeCasas: sigRespuesta[1].tablaDeCasas || [] }
            ];
        } catch (error) {
            console.error('Hubo un problema con la petición fetch:', error);
        }
    }

    await traerDatosDeMarcas();
    console.log(MarcasDeMascotasYCasas);
    return MarcasDeMascotasYCasas;
}

function colocarMarca(map,titulo, coordenadas, subTitulo, detalle, boton, ubicaionMascota,icono) {

    const contenido = `
        <div class="mascota resaltar">
            <div class="detalles">  
                <div class="especie">${ubicaionMascota}</div>  
                <div class="raza">${subTitulo}</div>
                <div class="info">
                    <div>${detalle}</div>
                    ${boton}
                </div>
            </div>
        </div>
    `;
    
    var marker = new google.maps.Marker({
        position: coordenadas,
        map: map,
        title: titulo,
        animation: google.maps.Animation.DROP,
        icon: icono
    });

    var infowindow = new google.maps.InfoWindow({
        content: contenido
    });

    // Ejemplo de evento de clic para los marcadores
    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
}


function obtenerCoordenadas(geocoder, calle, callback) {
    function procesarResultados(resultado, estado) {
        if (estado === 'OK') {
            // Obtener las coordenadas de la primera coincidencia encontrada
            var latitud = resultado[0].geometry.location.lat();
            var longitud = resultado[0].geometry.location.lng();
            var coordenadas = { 'lat': latitud, 'lng': longitud };
            // Llamar al callback con las coordenadas obtenidas
            callback(coordenadas);
        }
    }

    // Hacer una solicitud al geocoder y pasar la función de devolución de llamada
    geocoder.geocode({ 'address': calle }, procesarResultados);
}
function posicionar(coordenadas) {
    if (map && map instanceof google.maps.Map) {
        map.setCenter(coordenadas);
    } else {
        console.error('El mapa no está definido o no es una instancia válida de google.maps.Map.');
    }
}
function irADireccion(data){
    obtenerCoordenadas(geocoder,data, function(coordenadas) {
        posicionar(coordenadas);
    });
}

