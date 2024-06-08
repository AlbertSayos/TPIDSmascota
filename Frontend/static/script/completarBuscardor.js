var razaDePerros = [
    "Labrador Retriever",
    "Golden Retriever",
    "Bulldog",
    "Boxer",
    "Caniche",
    "Dóberman",
    "Chihuahua",
    "Pug",
    "Yorkshire Terrier",
    "Bichón Frisé",
    "Nose/Mestizo",
];
var razaDeGatos = ["Siamés",
    "Persa",
    "Maine Coon",
    "Bengalí",
    "Ragdoll",
    "British Shorthair",
    "Abisinio",
    "Sphynx",
    "Scottish Fold",
    "Munchkin",
     "nose/mestizo"
    ];

var tipoHTML = document.getElementById("tipo");
tipoHTML.addEventListener('change', function () {
    var tipo = tipoHTML.value;
    var razas = document.getElementById('razas');

    // Eliminar opciones anteriores
    razas.innerHTML = '<option value="">Selecciona la raza</option>';

    // Recorrido de las opciones
    function agregarOpciones(opciones) {
        for (let i = 0; i < opciones.length; i++) {
            var raza = opciones[i];
            var option = document.createElement('option');
            option.value = raza;
            option.text = raza;
            razas.appendChild(option);
        }
    }

    // Agrego nuevas opciones
    if (tipo === 'perro') {
        agregarOpciones(razaDePerros);
    } else if (tipo === 'gato') {
        agregarOpciones(razaDeGatos);
    } else {
        // Si el tipo no es ni "perro" ni "gato", agregar opciones personalizadas
        var option = document.createElement('option');
        option.value = tipo; // Usamos el valor del tipo como la raza personalizada
        option.text = tipo; // Usamos el valor del tipo como el texto de la opción
        razas.appendChild(option);
    }
});
