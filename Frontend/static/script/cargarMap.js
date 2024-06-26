
let map;
const ubicacionDefecto = {lat: -34.61747372535215, lng: -58.367949651070965};
var geocoder;



//*************************************************iniciar mapa*************************************************************** */
async function initMap() {
    var center = { lat: -34.61747372535215, lng: -58.367949651070965 };
    
    // Crear un nuevo mapa
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 17,
        center: center
    });
    
    geocoder = new google.maps.Geocoder(); //obitiene coordenadas

    //buscador
    const placeAutocomplete = new google.maps.places.PlaceAutocompleteElement(); // Autocompletado de lugares
    placeAutocomplete.id = "place-autocomplete-input";
    const card = document.getElementById("place-autocomplete-card");
    card.appendChild(placeAutocomplete);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(card);

    // agrega el evento al seleccionar un lugar
    placeAutocomplete.addEventListener("gmp-placeselect", async ({ place }) => {
        await place.fetchFields({
            fields: ["displayName", "formattedAddress", "location"],
        });

        // posiciona el mapa según el lugar seleccionado
        if (place.viewport) {
            map.fitBounds(place.viewport);
        } else {
            map.setCenter(place.location);
            map.setZoom(17);
        }
    });

    var MarcasDeMascotasYCasas = await moduloDeTablas();
    tablaDeMascotasStr = JSON.stringify(MarcasDeMascotasYCasas[0].tablaDeMascota);
    var tablaDeMascotas = JSON.parse(tablaDeMascotasStr);

    // Iteras sobre cada mascota
    for (let i = 0; i < tablaDeMascotas.length; i++) {
        (function() {
            // Obtiene la mascota actual
            let mascota = tablaDeMascotas[i];
            
            // Define los datos para colocar la marca
            var titulo = mascota.especie;
            var subTitulo = mascota.especie + " " + mascota.raza + " " + mascota.sexo;
            var ubicacionMascota = mascota.calle + " " + mascota.altura + "," + mascota.zona;
            var detalle = mascota.descripcion;
            var boton = `<div><a href="/PerfilMascota/${mascota.mascotaid}"  class="boton" target="_blank">Más información</a></div>`;
            var iconMascotas = {
                url: '/static/icons/imascotas.svg', 
                scaledSize: new google.maps.Size(70, 50) 
            };
            obtenerCoordenadas(geocoder, ubicacionMascota, function(coordenadas) {
                colocarMarca(map, titulo, coordenadas, subTitulo, detalle, boton, ubicacionMascota,iconMascotas); //coloco la marca de las mascotas
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
                var iconoCentros = {
                    url: '/static/icons/Icentros.svg', // Ruta al icono
                    scaledSize: new google.maps.Size(70, 50) // Tamaño del icono
                };
                obtenerCoordenadas(geocoder,ubicaionCentro, function(coordenadas) {
                    colocarMarca(map, titulo, coordenadas, subTitulo, detalle, boton,ubicaionCentro, iconoCentros); //coloco la marca de los refugios
                });
            })(); 
        }

}


    