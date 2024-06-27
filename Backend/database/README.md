## Conectar la base de datos con la API

Para conectar la API con la base de datos es necesario su URL. Para eso, siga los siguientes pasos...

1.- Entrar a la carpeta 'database':

```
cd database/
```

2.- Iniciar el contenedor con docker-compose:

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