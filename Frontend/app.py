from flask import Flask, jsonify, render_template, Response,request,redirect,url_for
import requests  # Se utiliza para hacer consultas a APIs externas
import os  # Se utiliza para interactuar con variables de entorno
from dotenv import load_dotenv  # Se utiliza para cargar variables de entorno desde un archivo .env
from flask_jwt_extended import JWTManager, create_access_token, decode_token



BackendLink = os.getenv('backend_link')  # Obtiene el valor de la variable de entorno 'backend_link'
api_key = os.getenv('APIKEY') #api de google cloud
PORT = 8080

load_dotenv()  # Carga las variables de entorno desde el archivo .env si existe
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('contraseña')
app.config['SECRET_KEY'] = os.getenv('contraseña')
jwt = JWTManager(app)
token = ""

@app.route('/')
def index():
    global token
    tokenDeUsuario = token
    token = ""
    return render_template('home.html',api_key=api_key,token=tokenDeUsuario)

@app.route('/map')
def map():
    return render_template('mapDeEjemplo.html',api_key=api_key)

@app.route('/home')
def home():
    return render_template('home.html',api_key=api_key)

    
@app.route('/registrar', methods=['GET','POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':

        tokenDeUsuario = request.headers.get('autorizacion')
        if tokenDeUsuario:
            decoded_token = decode_token(tokenDeUsuario)
            decode = decoded_token.get('sub')

            especie = request.form.get('ftipo')
            sexo = request.form.get('fsexo')
            raza = request.form.get('fraza')
            detalles = request.form.get('fdetalles')
            zona = request.form.get('fzona')
            calle = request.form.get('fcalle')
            altura = request.form.get('faltura')
            requests.get(f'{BackendLink}/registrar?usuarioid={decode.user_id}&especie={especie}&raza={raza}&sexo={sexo}&detalles={detalles}&zona={zona}&calle={calle}&altura={altura}')
            
            return redirect(ulr_for('index'))

@app.route('/PerfilMascota') # Planee una demo con ese estilo de parametros acorde a lo que se recibirá en la base de datos
def perfil_mascota():
    mascota = {
        "id": 1,
        "especie": "perro",
        "raza": "Labrador Retriever",
        "zona": "Palermo",
        "calle": "Av. Santa Fe",
        "altura": 3000,
        "sexo": "macho",
        "estado": "buscado",
        "detalles": "Este es mi comentario",
        "contacto": "Este es mi número"}
    return render_template("PerfilMascota.html", mascota=mascota)

@app.route("/RegistrarUsuario")
def registrar_usuario():
    if request.method == "POST": # Cuando el usuario haya sido ingresado, envia un JSON para la verificacion
        usuario = {
            'nombre' : request.form.get('fusuario'),
            "contraseña" : request.form.get('fcontraseña')
        }
        return jsonify(usuario)
        
    else:
        return render_template("registrarusuario.html")



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


@app.route('/buscadas', methods=['GET', 'POST'])
def buscadas():
    if request.method == "POST":
        especie = request.form["mespecie"]
        raza = request.form["mraza"]
        sexo = request.form["msexo"]
        filtro = requests.get(f'{BackendLink}/buscarmascotas?especie = {especie}&raza = {raza}&sexo = {sexo}')
        if filtro.status_code == 200:
            tablaDeMascotas = filtro.json()
            return render_template('buscadas.html',api_key=api_key, tablaDeMascota=tablaDeMascotas)
    tabla = requests.get(f'{BackendLink}/buscarmascotas')
    if tabla.status_code == 200:
        tabla = tabla.json()
        return render_template('buscadas.html', api_key=api_key, tablaDeMascotas=tabla)


@app.route('/cargarMapa')
def cargarMapa():
    return render_template('mapDeEjemplo.html', api_key=api_key)
"""
#EJEMPLO DE COMO DEVOLVER CARGAR TAMBLAS
resultados = [
    {
        "tablaDeMascota": [
    {
        "id": 1,
        "especie": "perro",
        "raza": "Labrador Retriever",
        "zona": "Palermo",
        "calle": "Av. Santa Fe",
        "altura": 3000,
        "sexo": "macho",
        "detalles": "Perro amigable y enérgico, encontrado cerca del parque."
    },
    {   
        "id": 2,
        "especie": "gato",
        "raza": "Siamés",
        "zona": "Recoleta",
        "calle": "Av. Callao",
        "altura": 1200,
        "sexo": "hembra",
        "detalles": "Gata tímida, encontrada cerca de un restaurante."
    },
    {
        "id": 3,
        "especie": "perro",
        "raza": "Golden Retriever",
        "zona": "Belgrano",
        "calle": "Av. Cabildo",
        "altura": 2000,
        "sexo": "macho",
        "detalles": "Perro juguetón, le encanta correr y jugar con pelotas."
    },
    {
        "id": 4,
        "especie": "gato",
        "raza": "Persa",
        "zona": "San Telmo",
        "calle": "Av. Independencia",
        "altura": 1500,
        "sexo": "hembra",
        "detalles": "Gata de pelaje largo y sedoso, muy cariñosa."
    },
    {
        "id": 5,
        "especie": "perro",
        "raza": "Bulldog Francés",
        "zona": "Villa Crespo",
        "calle": "Av. Corrientes",
        "altura": 5800,
        "sexo": "macho",
        "detalles": "Perro pequeño pero fuerte, le encanta pasear."
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
"""

@app.route('/cargarTablas')
def cargarTablas():
    tablaDeMascota = {}
    tablaDeCasas = {}
    try:
        res_mascotas = requests.get(f'{BackendLink}/tablademascotas')
        res_casas = requests.get(f'{BackendLink}/tabladecentros')
        
        # Comprobamos si las peticiones fueron exitosas
        if res_mascotas.status_code == 200 and res_casas.status_code == 200:
            tablaDeMascota = res_mascotas.json()
            tablaDeCasas = res_casas.json()
        else:
            return jsonify({"error": "Error al obtener datos de las tablas"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    tablasDeMascotasYCasas = [
        {
            "tablaDeMascota": tablaDeMascota,
        },
        {
            "tablaDeCasas": tablaDeCasas
        }
    ]
    return jsonify(tablasDeMascotasYCasas)

@app.route('/login', methods=['GET','POST'])
def login():
     global token
     if request.method == 'POST':
        nombre = request.form.get('nombre') 
        contraseña = request.form.get('contraseña')
        respuesta = requests.get(f'{BackendLink}/login?usuario={nombre}&contraseña={contraseña}')
        if respuesta.status_code == 200:
            tokenDeUsuario = respuesta.json().get('token')
            token = tokenDeUsuario
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
     return render_template ('login.html')
     
@app.route('/logout', methods=['GET'])
def logout():
    return render_template ('logout.html')

@app.route('/perfil', methods=['GET'])
def perfil():
    return render_template('perfil.html') #y aca ponemos un script que pase un token al POST de mi perfil

decode = {}
@app.route('/decodificar', methods=['GET'])
def decodificar():
    global decode
    tokenDeUsuario = request.headers.get('autorizacion')
    print(tokenDeUsuario)
    if tokenDeUsuario:
        decoded_token = decode_token(tokenDeUsuario)
        decode = decoded_token.get('sub')
        return '', 204
    else:
        return redirect(url_for('login'))
    
@app.route('/miperfil', methods=['GET'])
def miperfil():
    global decode
    if not decode:
        return  redirect(url_for('perfil'))
    decodeDeUsuario = decode
    decode = {}
    return render_template('miperfil.html', decode=decodeDeUsuario)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
