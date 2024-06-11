# Instrucciones para usar el Proyecto

Para utilizar este proyecto, sigue los siguientes pasos:

## Configuración del archivo .env

Antes de ejecutar el proyecto, es necesario crear un archivo `.env` en la raíz del proyecto y configurar la dirección del backend. Si estás ejecutando el proyecto de forma local, puedes configurar la variable `BACKEND_LINK` de la siguiente manera:

```
BACKEND_LINK=http://localhost:8081
```

Asegúrate de que el enlace sea el adecuado para tu entorno de desarrollo.

## Instalación de dependencias

Este proyecto utiliza algunas dependencias específicas que necesitas instalar antes de ejecutarlo. Puedes instalarlas utilizando pip, el gestor de paquetes de Python:

```
pip install python-dotenv
pip install requests
```

- **python-dotenv**: Esta librería se utiliza para manejar las variables de entorno desde el archivo .env.
- **requests**: Esta librería se utiliza para realizar solicitudes HTTP a servidores externos y manejar las respuestas.

## Clonar y actualizar el repositorio

Si aún no has clonado este repositorio, puedes hacerlo utilizando el siguiente comando:

```
git clone https://github.com/AlbertSayos/TPIDSmascota.git
```

Una vez clonado el repositorio, puedes actualizarlo desde una rama con tu nombre utilizando los siguientes comandos:

```
#cambiar de rama
git checkout main   # Cambia a la rama principal
git pull            # Actualiza el repositorio local con los cambios remotos
git checkout -b <nombre-de-tu-rama>   # Crea una nueva rama con tu nombre
git push -u <nombre-de-tu-rama> #esto crea la rama en github

#subir cambios
git add .           # Agrega los cambios realizados
git commit -m "agrego commit"
git push origin <nombre-de-tu-rama>   # Sube tus cambios a tu rama en el repositorio remoto
```


Recuerda reemplazar `<nombre-de-tu-rama>` con el nombre que quieras darle a tu rama.



Para usar el mapa
poner estos script

```
<script src="{{ url_for('static', filename='/script/cargarMap.js') }}" defer></script>

```

```
<script>
        (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})({
          key: '{{api_key}}',
          v: "beta",
          // Use the 'v' parameter to indicate the version to use (weekly, beta, alpha, etc.).
          // Add other bootstrap parameters as needed, using camel case.
        });
      </script>
```
Y este html
```
<h3>Mi primer mapa de Google</h3>
    <div class="place-autocomplete-card" id="place-autocomplete-card">
        <p>Search for a place here:</p>
      </div>
      <div id="map"></div>
```
hacer una cuenta en google cloud
agregar la api de:
Maps JavaScript API (para el mapa)
Places API (New) (para el buscador)
y Geocoding API (y para que te devuelva las coordenadas de una calle)
poner su api key en su archivo .env y estaria

Por ultimo deje un mapa de ejemplo donde se muestra como se usa