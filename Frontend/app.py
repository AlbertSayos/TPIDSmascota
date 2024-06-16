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
decode = ""

@app.route('/')
def index():
    global token
    tokenDeUsuario = token
    token = ""
    return render_template('home.html',token=tokenDeUsuario)

@app.route('/map')
def map():
    
    return render_template('mapbasic.html')

@app.route('/home')
def home():
    return render_template('home.html',api_key=api_key)

    
@app.route('/registrar', methods=['GET','POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':

        tokenDeUsuario = request.headers.get('autorizacion')
        #print("verifico token" + str(tokenDeUsuario))
        if tokenDeUsuario:
            
            decoded_token = decode_token(tokenDeUsuario)
            print("hay error?")
            decode = decoded_token.get('sub')
            print(decode)
            especie = request.headers.get('ftipo')
            sexo = request.headers.get('fsexo')
            raza = request.headers.get('fraza')
            detalles = request.headers.get('fdetalles')
            zona = request.headers.get('fzona')
            calle = request.headers.get('fcalle')
            altura = request.headers.get('faltura')

            datos= {
                'usuarioid': decode["user_id"],
                'especie': especie,
                'sexo': sexo,
                'raza': raza,
                'detalles': detalles,
                'zona': zona,
                'calle': calle,
                'altura': altura
            }

            # Imprimir la URL y los datos para depuración
            print(f'{BackendLink}/registrar')
            print(datos)

            # Realizar la solicitud POST
            response = requests.post(f'{BackendLink}/registrar', json=datos)
            print(response.status_code)
            # Verificar la respuesta del servidor
            if response.status_code == 200:
                return jsonify({'message': 'se ha agregado correctamente'}),200
            else:
                return jsonify({'message': 'algo fallo'}),400
        
@app.route('/PerfilMascota/<int:id>')
def perfil_mascota(id):
    response=requests.get(f'{BackendLink}//buscarmascotas?mascotaid={id}')
    if response.status_code == 200:
        mascota = response.json()[0]
        return render_template("PerfilMascota.html", mascota=mascota)
    return render_template("404.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST": # Cuando el usuario haya sido ingresado, envia un JSON para la verificacion
        nombre= request.form.get('fusuario')
        contraseña= request.form.get('fpassword')
        contacto= request.form.get('fcontact')
        usuario = {
            'nombre' : nombre,
            "contraseña" : contraseña,
            "contacto" : contacto
        }
        response=requests.post(f'{BackendLink}/registrarUsuario?nombre={nombre}&contraseña={contraseña}&contacto={contacto}', json=usuario)
        if response.status_code == 200:
            return redirect(url_for('login'))
        else:
            return render_template("registrarusuario.html")
    return render_template("registrarusuario.html")


@app.route('/buscadas', methods=['GET', 'POST'])
def buscadas():
    datos = {
        "id": "",
        "especie": "",
        "raza": "",
        "sexo": ""
    }
    if request.method == "POST":
        especie = request.form.get("mespecie")
        raza = request.form.get("mraza")
        sexo = request.form.get("msexo")

        datos = {
            "especie": especie,
            "raza": raza,
            "sexo": sexo
        }
        #filtro = requests.get(f'{BackendLink}/buscarmascotas', json=datos)
        #if filtro.status_code == 200:
        #    tablaDeMascotas = filtro.json()
        #    return render_template('buscadas.html',scriptDeMapa=scriptDeMapa, tablaDeMascotas=tablaDeMascotas)
    tabla = requests.get(f'{BackendLink}/buscarmascotas', json=datos)
    if tabla.status_code == 200:
        tabla = tabla.json()
    return render_template('buscadas.html',tablaDeMascotas=tabla)


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
        datos = {
            "nombre": nombre,
            "contraseña": contraseña
        }
        respuesta = requests.get(f'{BackendLink}', json=datos)
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

@app.route('/decodificar', methods=['GET'])
def decodificar():
    global decode
    tokenDeUsuario = request.headers.get('autorizacion')
    
    if tokenDeUsuario:
        print(tokenDeUsuario)
        decoded_token = decode_token(tokenDeUsuario)
        print(decoded_token)
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
    user_id = decodeDeUsuario["user_id"]
    nombreDeUsuario = decodeDeUsuario["username"]
    datos = {"user_id":user_id}
    respuesta = requests.get(f'{BackendLink}/mascotaDeUsuario', json=datos)
    if respuesta.status_code == 200:
        listaDeMascotas = respuesta.json()
        print(listaDeMascotas)
        return render_template('miperfil.html', nombreDeUsuario=nombreDeUsuario,listaDeMascotas=listaDeMascotas)
    else:
        return redirect(url_for('login'))


@app.route('/script')
def conseguirScript():
    base_url = "https://maps.googleapis.com/maps/api/js"
    params = {
        "key": api_key,
        "v": "beta",
        "callback": "initMap"  # llama la funcion cuando carga la pagina
    }
    libraries = ["marker", "places", "geocoding"]  # Lista de bibliotecas a importar
    params["libraries"] = ",".join(libraries)
    scriptDeMapa= requests.get(base_url, params=params)


    if scriptDeMapa.status_code == 200:
        return scriptDeMapa.text

if __name__ == '__main__':
    app.run(debug=True, port=PORT)