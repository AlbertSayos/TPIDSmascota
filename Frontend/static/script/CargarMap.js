// Initialize and add the map
let map;
const ubicacionDefecto = {lat: -34.61747372535215, lng: -58.367949651070965};
/*
const mascotasPerdidas = [
    {
        "especie": "perro",
        "raza": "Labrador Retriever",
        "zona": "Palermo",
        "calle": "Av. Santa Fe",
        "altura": 3000
    },
    {
        "especie": "gato",
        "raza": "Siamés",
        "zona": "Recoleta",
        "calle": "Av. Callao",
        "altura": 1200
    },
    {
        "especie": "perro",
        "raza": "Golden Retriever",
        "zona": "Belgrano",
        "calle": "Av. Cabildo",
        "altura": 2000
    },
    {
        "especie": "gato",
        "raza": "Persa",
        "zona": "San Telmo",
        "calle": "Av. Independencia",
        "altura": 1500
    },
    {
        "especie": "perro",
        "raza": "Bulldog Francés",
        "zona": "Villa Crespo",
        "calle": "Av. Corrientes",
        "altura": 5800
    }
]
*/
var MarcasDeMascotasYCasas = []; 

function traerDatosDeMarcas(){
    fetch('/cargarTablas')
        .then(respuesta => {
            if (!respuesta.ok){
                throw new Error('Network response was not ok');
            }
            return respuesta.json();
        })
        .then(sigRespuesta => {
            
            MarcasDeMascotasYCasas = sigRespuesta;
        })
        .catch(error => {
            console.error('Hubo un problema con la petición fetch:', error);
        });
}

//var mascotasPerdidas = 
//var casasRegistradas = 


updateInfoWindow
//let geocoder;
async function initMap() {
     // The location of Uluru
     //const position = { lat: -25.344, lng: 131.031 };
    // Request needed libraries.
    //@ts-ignore
    const [{ Map }, { AdvancedMarkerElement }, {Geocoder}] = await Promise.all([
        google.maps.importLibrary("marker"),
        google.maps.importLibrary("places"),
        google.maps.importLibrary("geocoding"),
      ]);
    const geocoder = new google.maps.Geocoder();
    //*****************************************creo mapa y lo centro en la fiuba****************************************/
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 17,
        center: ubicacionDefecto,
        mapId: "Mapa de mascotas",
    });
    /***************************************buscador*********************************************************************/
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

    /***************************************agregar marcas***************************************************************/
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
    function cargarMascota(titulo,coordenadas){
        const priceTag = document.createElement("div");

        priceTag.className = "price-tag";
        priceTag.textContent = titulo;
        const marker = new google.maps.marker.AdvancedMarkerElement({
            map: map,
            position: coordenadas,
            title: titulo,
            content: priceTag,
          });
        }
    
        //console.log(JSON.stringify(MarcasDeMascotasYCasas[0].tablaDeMascota))
        tablaDeMascotasStr = JSON.stringify(MarcasDeMascotasYCasas[0].tablaDeMascota);
        tablaDeMascotas = JSON.parse(tablaDeMascotasStr);
        for (let i = 0; i < tablaDeMascotas.length; i++) {
            (function() {
                let mascota = tablaDeMascotas[i];
                
                var titulo = mascota.especie + " " + mascota.raza;
                var ubicaionMascota = mascota.calle + " " + mascota.altura + "," + mascota.zona ;
                //console.log(tablaDeMascotas.length);
                obtenerCoordenadas(geocoder,ubicaionMascota, function(coordenadas) {
                    cargarMascota(titulo,coordenadas);
                });
            })();
        }
        
        casasRegistradasStr = JSON.stringify(MarcasDeMascotasYCasas[1].tablaDeCasas);
        casasRegistradas = JSON.parse(casasRegistradasStr);
        for (let i = 0; i < casasRegistradas.length; i++) {
            (function() {
                let mascota = casasRegistradas[i];
                
                var titulo = mascota.nombre;
                var ubicaionMascota = mascota.calle + " " + mascota.altura + "," + mascota.zona ;
                //console.log(tablaDeMascotas.length);
                obtenerCoordenadas(geocoder,ubicaionMascota, function(coordenadas) {
                    cargarMascota(titulo,coordenadas);
                });
            })();
        }
    
}

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

traerDatosDeMarcas()
initMap();