var MarcasDeMascotasYCasas = await moduloDeTablas();

tablaDeMascotasStr = JSON.stringify(MarcasDeMascotasYCasas[0].tablaDeMascota);
tablaDeMascotas = JSON.parse(tablaDeMascotasStr);

function cargarTabla(){
    
}