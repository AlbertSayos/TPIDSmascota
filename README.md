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

