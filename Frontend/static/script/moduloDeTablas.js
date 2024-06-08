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
