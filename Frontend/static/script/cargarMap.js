


// Initialize and add the map
let map;
const ubicacionDefecto = {lat: -34.61747372535215, lng: -58.367949651070965};
var geocoder;

async function initMap() {
    var center = { lat: -34.61747372535215, lng: -58.367949651070965 };
    
    // Crear un nuevo mapa
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 17,
        center: center
    });

    // Autocompletado de lugares, etc.
    geocoder = new google.maps.Geocoder();
    const placeAutocomplete = new google.maps.places.PlaceAutocompleteElement();
    placeAutocomplete.id = "place-autocomplete-input";
    const card = document.getElementById("place-autocomplete-card");
    card.appendChild(placeAutocomplete);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(card);

    // Listener para seleccionar un lugar
    placeAutocomplete.addEventListener("gmp-placeselect", async ({ place }) => {
        await place.fetchFields({
            fields: ["displayName", "formattedAddress", "location"],
        });

        // Ajustar el mapa según el lugar seleccionado
        if (place.viewport) {
            map.fitBounds(place.viewport);
        } else {
            map.setCenter(place.location);
            map.setZoom(17);
        }
    });

    var MarcasDeMascotasYCasas = await moduloDeTablas();
    tablaDeMascotasStr = JSON.stringify(MarcasDeMascotasYCasas[0].tablaDeMascota);
    tablaDeMascotas = JSON.parse(tablaDeMascotasStr);
    //console.log(tablaDeMascotas)
    for (let i = 0; i < tablaDeMascotas.length; i++) {
        (function() {
            let mascota = tablaDeMascotas[i];
            //console.log(mascota.especie + i)
            var titulo = mascota.especie;
            var subTitulo = mascota.especie + " " + mascota.raza + " " + mascota.sexo;
            var ubicaionMascota = mascota.calle + " " + mascota.altura + "," + mascota.zona;
            var detalle = mascota.descripcion;
            var icono = `<i aria-hidden="true" class="fa fa-paw" title="${subTitulo}"></i>`
            var boton = `<div><a href="/PerfilMascota/${mascota.mascotaid}"  class="boton" target="_blank">Más información</a></div>`;
            obtenerCoordenadas(geocoder,ubicaionMascota, function(coordenadas) {
                //cargarMascota(map,titulo,coordenadas,subTitulo,detalle,boton,ubicaionMascota,icono);
                console.log(coordenadas)
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
            const iconMascotas = {
                url: '/static/icons/imascotas.svg', // Ruta al icono
                scaledSize: new google.maps.Size(50, 35) // Tamaño del icono
            };
            var marker = new google.maps.Marker({
                position: coordenadas,
                map: map,
                title: subTitulo,
                animation: google.maps.Animation.DROP,
                icon: iconMascotas
            });
        
            var infowindow = new google.maps.InfoWindow({
                content: contenido
            });
        
            // Ejemplo de evento de clic para los marcadores
            marker.addListener('click', function() {
                infowindow.open(map, marker);
            });
            });
        })();
    }

    casasRegistradasStr = JSON.stringify(MarcasDeMascotasYCasas[1].tablaDeCasas);
    casasRegistradas = JSON.parse(casasRegistradasStr);
    for (let i = 0; i < casasRegistradas.length; i++) {
        (function() {
            let casa = casasRegistradas[i];
                
            var titulo = casa.nombre;
            var subTitulo = "casa o centro de mascota"
            var ubicaionCentro = casa.calle + " " + casa.altura + "," + casa.zona ;
            var detalle = casa.descripcion;
            var boton = `<div><a href="#" target="_blank" class="boton">Más información</a></div>`;
            var icono = `<i aria-hidden="true" class="fa-solid fa-house" title="${subTitulo}"></i>`
            //console.log(tablaDeMascotas.length);
            obtenerCoordenadas(geocoder,ubicaionCentro, function(coordenadas) {
                const contenido = `
                <div class="mascota resaltar">
                    <div class="detalles">  
                        <div class="especie">${ubicaionCentro}</div>  
                        <div class="raza">${subTitulo}</div>
                        <div class="info">
                            <div>${detalle}</div>
                            ${boton}
                        </div>
                    </div>
                </div>
            `;
            const iconoCentros = {
                url: '/static/icons/Icentros.svg', // Ruta al icono
                scaledSize: new google.maps.Size(50, 35) // Tamaño del icono
            };

            var marker = new google.maps.Marker({
                position: coordenadas,
                map: map,
                title: subTitulo,
                icon: iconoCentros,
                animation: google.maps.Animation.DROP
            });
        
            var infowindow = new google.maps.InfoWindow({
                content: contenido
            });
        
            // Ejemplo de evento de clic para los marcadores
            marker.addListener('click', function() {
                infowindow.open(map, marker);
            });
            });
            })();
        }

}


function obtenerCoordenadas(geocoder, calle, callback) {
    // Definir la función de devolución de llamada
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



/*
updateInfoWindow
//let geocoder;
async function initMap() {

    //@ts-ignore
    const [{ Map }, { AdvancedMarkerElement }, {Geocoder}] = await Promise.all([
        //google.maps.importLibrary("marker"),
        //google.maps.importLibrary("places"),
        //google.maps.importLibrary("geocoding"),
      ]);
    //geocoder = new google.maps.Geocoder();
    //*****************************************creo mapa y lo centro en la fiuba****************************************
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 17,
        center: ubicacionDefecto,
        mapId: "Mapa de mascotas",
    });
    /***************************************buscador*********************************************************************
    //@ts-ignore
    const placeAutocomplete = new google.maps.places.PlaceAutocompleteElement();

    //@ts-ignore
    placeAutocomplete.id = "place-autocomplete-input";

    const card = document.getElementById("place-autocomplete-card");

    //@ts-ignore
    card.appendChild(placeAutocomplete);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(card);
    // Create the marker and infowindow
    marker = new google.maps.marker.AdvancedMarkerElement({
        map,
    });
    infoWindow = new google.maps.InfoWindow({});
    // Add the gmp-placeselect listener, and display the results on the map.
    //@ts-ignore
    placeAutocomplete.addEventListener("gmp-placeselect", async ({ place }) => {
        await place.fetchFields({
        fields: ["displayName", "formattedAddress", "location"],
        });
        // If the place has a geometry, then present it on a map.
        if (place.viewport) {
        map.fitBounds(place.viewport);
        } else {
        map.setCenter(place.location);
        map.setZoom(17);
        }

        let content =
        '<div id="infowindow-content">' +
        '<span id="place-displayname" class="title">' +
        place.displayName +
        "</span><br />" +
        '<span id="place-address">' +
        place.formattedAddress +
        "</span>" +
        "</div>";

        updateInfoWindow(content, place.location);
        marker.position = place.location;
    });
    */
    /***************************************agregar marcas***************************************************************
    
    function construirContenido(mascota) {
        const contenido = document.createElement("div"); 
    
        contenido.classList.add("mascota");
        contenido.innerHTML = `
        <div class="icono">
            <i aria-hidden="true" class="fa fa-paw" title="${mascota.especie}"></i>
            <span class="fa-sr-only">${mascota.especie}</span>
        </div>
        <div class="detalles">  
            <div class="especie">${mascota.especie}</div>  
            <div class="raza">${mascota.raza}</div>  
            <div class="info">
                <div>${mascota.sexo}</div>  
                <div>${mascota.detalles}</div> 
                <div>${mascota.contacto}</div> 
                <div><a href="#" target="_blank">Más información</a></div>
            </div>
        </div>
        `;
        return contenido;
    }
    function alternarResaltar(marcadorVista) {
        if (marcadorVista.content.classList.contains("resaltar")) {
        marcadorVista.content.classList.remove("resaltar");
        marcadorVista.zIndex = null;
        } else {
        marcadorVista.content.classList.add("resaltar");
        marcadorVista.zIndex = 1;
        }
    }

    function cargarMascota(titulo,coordenadas,subTitulo,detalle,boton,ubicaion,icono){
        console.log(titulo)
        const contenido = document.createElement("div"); 
        contenido.classList.add("mascota");
        contenido.innerHTML = `
        <div class="icono">
            ${icono}
            <span class="fa-sr-only">${titulo}</span>
        </div>
        <div class="detalles">  
            <div class="especie">${ubicaion}</div>  
            <div class="raza">${subTitulo}</div>
            <div class="info">
                <div>${detalle}</div>
                ${boton}
            </div>
        </div>
        `;
        const marker = new google.maps.marker.AdvancedMarkerElement({
            map: map,
            position: coordenadas,
            title: subTitulo,
            content: contenido,
          });
        marker.addListener("click", () => {
            alternarResaltar(marker);
        });

        }

        var MarcasDeMascotasYCasas = await moduloDeTablas();
        tablaDeMascotasStr = JSON.stringify(MarcasDeMascotasYCasas[0].tablaDeMascota);
        tablaDeMascotas = JSON.parse(tablaDeMascotasStr);
        for (let i = 0; i < tablaDeMascotas.length; i++) {
            (function() {
                let mascota = tablaDeMascotas[i];
                console.log(mascota.especie + i)
                var titulo = mascota.especie;
                var subTitulo = mascota.especie + " " + mascota.raza + " " + mascota.sexo;
                var ubicaionMascota = mascota.calle + " " + mascota.altura + "," + mascota.zona;
                var detalle = mascota.descripcion;
                var icono = `<i aria-hidden="true" class="fa fa-paw" title="${subTitulo}"></i>`
                var boton = `<div><a href="/PerfilMascota/${mascota.mascotaid}"  class="boton" target="_blank">Más información</a></div>`;
                obtenerCoordenadas(geocoder,ubicaionMascota, function(coordenadas) {
                    cargarMascota(titulo,coordenadas,subTitulo,detalle,boton,ubicaionMascota,icono);
                });
            })();
        }
        
        casasRegistradasStr = JSON.stringify(MarcasDeMascotasYCasas[1].tablaDeCasas);
        casasRegistradas = JSON.parse(casasRegistradasStr);
        for (let i = 0; i < casasRegistradas.length; i++) {
            (function() {
                let casa = casasRegistradas[i];
                
                var titulo = casa.nombre;
                var subTitulo = "casa o centro de mascota"
                var ubicaionCentro = casa.calle + " " + casa.altura + "," + casa.zona ;
                var detalle = casa.descripcion;
                var boton = `<div><a href="#" target="_blank" class="boton">Más información</a></div>`;
                var icono = `<i aria-hidden="true" class="fa-solid fa-house" title="${subTitulo}"></i>`
                //console.log(tablaDeMascotas.length);
                obtenerCoordenadas(geocoder,ubicaionCentro, function(coordenadas) {
                    cargarMascota(titulo,coordenadas,subTitulo,detalle,boton,ubicaionCentro,icono);
                });
            })();
        }*/
    
//}
/*
// Helper function to create an info window.
function updateInfoWindow(content, center) {
    infoWindow.setContent(content);
    infoWindow.setPosition(center);
    infoWindow.open({
      map,
      anchor: marker,
      shouldFocus: false,
    });
  }
*/



//**************************************iniciar funciones******************************************************* */
//traerDatosDeMarcas()
//MarcasDeMascotasYCasas = moduloDeTablas()
//initMap();