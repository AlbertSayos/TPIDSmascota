from flask import Flask, jsonify, render_template, Response,request
import requests  # Se utiliza para hacer consultas a APIs externas
import os  # Se utiliza para interactuar con variables de entorno
from dotenv import load_dotenv  # Se utiliza para cargar variables de entorno desde un archivo .env
api_key = os.getenv('APIKEY') #api de google cloud
PORT = 8080

load_dotenv()  # Carga las variables de entorno desde el archivo .env si existe
app = Flask(__name__)

BackendLink = os.getenv('backend_link')  # Obtiene el valor de la variable de entorno 'backend_link'


@app.route('/')
def index():
    #respuesta = requests.get(f'{BackendLink}')  # Realiza una solicitud GET a la URL almacenada en 'BackendLink'
    
    return render_template('home.html',api_key=api_key)

@app.route('/map')
def map():
    return render_template('mapDeEjemplo.html',api_key=api_key)

@app.route('/home')
def home():
    return render_template('home.html',api_key=api_key)

@app.route('/registrar')
def registrar():
    
    return render_template('registrar.html')

tablademascotas = [
    {
        "id": 1,
        "especie": "perro",
        "raza": "Labrador Retriever",
        "zona": "Palermo",
        "calle": "Av. Santa Fe",
        "altura": 3000,
        "sexo": "macho"
    },
    {   
        "id": 2,
        "especie": "gato",
        "raza": "Siamés",
        "zona": "Recoleta",
        "calle": "Av. Callao",
        "altura": 1200,
        "sexo": "hembra"
    },
    {
        "id": 3,
        "especie": "perro",
        "raza": "Golden Retriever",
        "zona": "Belgrano",
        "calle": "Av. Cabildo",
        "altura": 2000,
        "sexo": "macho"
    },
    {
        "id": 4,
        "especie": "gato",
        "raza": "Persa",
        "zona": "San Telmo",
        "calle": "Av. Independencia",
        "altura": 1500,
        "sexo": "hembra"
    },
    {
        "id": 5,
        "especie": "perro",
        "raza": "Bulldog Francés",
        "zona": "Villa Crespo",
        "calle": "Av. Corrientes",
        "altura": 5800,
        "sexo": "macho"
    }
]
tablaDePerros = [
    {
        "id": 1,
        "especie": "perro",
        "raza": "Labrador Retriever",
        "zona": "Palermo",
        "calle": "Av. Santa Fe",
        "altura": 3000,
        "sexo": "macho"
    },
    {
        "id": 3,
        "especie": "perro",
        "raza": "Golden Retriever",
        "zona": "Belgrano",
        "calle": "Av. Cabildo",
        "altura": 2000,
        "sexo": "macho"
    },
    {
        "id": 5,
        "especie": "perro",
        "raza": "Bulldog Francés",
        "zona": "Villa Crespo",
        "calle": "Av. Corrientes",
        "altura": 5800,
        "sexo": "macho"
    }
]


@app.route('/buscadas')
def buscadas():
    #llamas a la tabla de mascota con requests.get(f'{BackendLink}/buscarMascota') #tabla de perros es lo que espero recibir por ejemplo
    tabla = tablademascotas #se puede poner tablaDePerros
    tipo = request.args.get('tipo') #tambien estan raza y sexo
    #en caso de que no haya ningun filtro llamas a tablademascotas
    return render_template('buscadas.html',api_key=api_key, tablaDeMascota=tabla)

@app.route('/cargarMapa')
def cargarMapa():
    return render_template('mapDeEjemplo.html', api_key=api_key)

#EJEMPLO DE COMO DEVOLVER CARGAR TAMBLAS
resultados = [
    {
        "tablaDeMascota": [
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
    },
    {
        "tablaDeCasas": [
            {
                "nombre": "Casa 1",
                "descripcion": "Casa grande con jardín",
                "zona": "Palermo",
                "calle": "Av. Santa Fe",
                "altura": 100
            },
            {
                "nombre": "Casa 2",
                "descripcion": "Departamento moderno",
                "zona": "Recoleta",
                "calle": "Av. Callao",
                "altura": 100
            },
            {
                "nombre": "Casa 3",
                "descripcion": "Casa antigua con estilo",
                "zona": "Belgrano",
                "calle": "Av. Cabildo",
                "altura": 100
            },
            {
                "nombre": "Casa 4",
                "descripcion": "Departamento luminoso",
                "zona": "San Telmo",
                "calle": "Av. Independencia",
                "altura": 600
            },
            {
                "nombre": "Casa 5",
                "descripcion": "Loft amplio",
                "zona": "Villa Crespo",
                "calle": "Av. Corrientes",
                "altura": 900
            }
        ]
    }
]


@app.route('/cargarTablas')
def cargarTablas():
    #llamas a dos tablas con requests.get(f'{BackendLink}/tablaDeMascotas') y el de tablas de las casas
    #las juntas y las devolves
    #tiene que quedar asi 
    # mascotasPerdidas = ["tablaDeMascota": {....}
    #                      "tablaDeCasas": {....}] 
    return jsonify(resultados)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)