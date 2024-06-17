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

#registra una publicacion de una mascota encontrada  
@app.route('/registrar', methods=['GET','POST']) 
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':

        tokenDeUsuario = request.form.get('ftoken')
        #print("verifico token" + str(tokenDeUsuario))
        if tokenDeUsuario:
            
            decoded_token = decode_token(tokenDeUsuario)
            print("hay error?")
            decode = decoded_token.get('sub')
            print(decode)
            especie = request.form.get('ftipo')
            sexo = request.form.get('fsexo')
            raza = request.form.get('fraza')
            detalles = request.form.get('fdetalles')
            zona = request.form.get('fzona')
            calle = request.form.get('fcalle')
            altura = request.form.get('faltura')

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
            print(f'{BackendLink}/registrarmascota')
            print(datos)

            # Realizar la solicitud POST
            response = requests.post(f'{BackendLink}/registrarMascota', json=datos)
            print(response.status_code)
            # Verificar la respuesta del servidor
            if response.status_code == 201:
                return redirect(url_for('index'))
            else:
                return jsonify({'message': 'algo fallo'}),400
        
@app.route('/PerfilMascota/<id>')
def perfil_mascota(id):
    mascotaid = id
    data = {"mascotaid": mascotaid}
    response=requests.post(f'{BackendLink}/buscarmascotas', json=data)
    if response.status_code == 200:
        print(response)
        mascota = response.json()[0]
        return render_template("PerfilMascota.html", mascota=mascota)
    return render_template("404.html")


@app.route('/eliminarMascota',methods=["GET", "POST"])
def eliminarMascota():
    if request.method == "GET":
        return redirect(url_for("index"))
    mascotaid = request.form.get("fmascotaid")
    datos = {
                'mascotaid': mascotaid
            }
    print(datos)
    response = requests.delete(f'{BackendLink}/eliminarmascota', json=datos)
    if response.status_code == 202:
        print("Datos enviados exitosamente.")
        return redirect(url_for("miperfil"))
    else:
        print(f"Error al enviar los datos: {response.status_code}, {response.text}")
        return redirect(url_for("index"))

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
        response=requests.post(f'{BackendLink}/registrarusuario', json=usuario)
        if response.status_code == 201:
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
    tabla = requests.post(f'{BackendLink}/buscarmascotas', json=datos)
    print(tabla.json())
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
        nombre = request.form.get('fnombre') 
        contraseña = request.form.get('fcontraseña')
        datos = {
            "nombre": nombre,
            "contraseña": contraseña
        }
        print(datos)
        respuesta = requests.get(f'{BackendLink}/login', json=datos)
        print(respuesta)
        if respuesta.status_code == 200:
            tokenDeUsuario = respuesta.json().get('token')
            token = tokenDeUsuario
            print(token)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
     return render_template ('login.html')
     
@app.route('/logout', methods=['GET'])
def logout():
    return render_template ('logout.html')

@app.route('/miperfil', methods=['GET', 'POST'])
def miperfil():
    if request.method == 'POST':
        tokenDeUsuario = request.form.get('token') 
        if tokenDeUsuario:
            
            print("llegue hasta aca")
            decodeDeUsuario = decode_token(tokenDeUsuario).get('sub')

            user_id = decodeDeUsuario["user_id"]
            nombreDeUsuario = decodeDeUsuario["username"]
            datos = {"id":user_id}
            print(datos)
            respuesta = requests.get(f'{BackendLink}/mascotaDeUsuario', json=datos)
            if respuesta.status_code == 200:
                listaDeMascotas = respuesta.json()
                print(listaDeMascotas)
                return render_template('miperfil.html', nombreDeUsuario=nombreDeUsuario,listaDeMascotas=listaDeMascotas)
            else:
                return redirect(url_for('registro'))
        else:
            return redirect(url_for('login'))
    print("********************************************************************************")
    return render_template('autorizacion.html') 


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