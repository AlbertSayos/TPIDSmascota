## Instrucciones para controlar la base de datos vía consola MYSQL (no API)

1.- Entrar a la carpeta 'database':

```
cd database/
```

2.- Iniciar el contenedor con docker-compose:

```
sudo docker-compose up -d --build
```

3.- Conectar con la base de datos MYSQL ( contraseña: `tp` ):

```
sudo docker exec -it database mysql -u root -p
```

```
use tp;
```

A partir de aquí, ya se pueden hacer las diversas queries a la base de datos manualmente. Esto es un tanto recomendable ya que, en base a sus resultados, podremos saber exactamente qué queries implementar posteriormente a la API.

4.- Salir de la base de datos y detener el contenedor:

```
exit;
```

```
sudo docker-compose down
```

## Conectar la base de datos con la API

Para conectar la API con la base de datos es necesario su URL. Antes de eso, se tienen que seguir los primeros dos comandos anteriores:

```
cd database/
```

```
sudo docker-compose up -d --build
```

Una vez levantada nuestra base de datos en docker-compose, nos podremos conectar a esta mediante la API con:

```
"mysql+mysqlconnector://root:tp@localhost:3300/tp"
```

Luego, si es necesario, con el siguiente comando se detiene la base de datos.

```
sudo docker-compose down
```