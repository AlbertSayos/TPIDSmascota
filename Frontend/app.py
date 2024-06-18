from flask import Flask, jsonify, render_template, Response,request,redirect,url_for
import requests  # Se utiliza para hacer consultas a APIs externas
import os  # Se utiliza para interactuar con variables de entorno
from dotenv import load_dotenv  # Se utiliza para cargar variables de entorno desde un archivo .env
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from flask_jwt_extended.exceptions import JWTExtendedException, JWTDecodeError


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

"""
redenreriza el home html, pagina de inicio de la web
"""
@app.route('/')
def index():
    global token
    tokenDeUsuario = token
    token = ""
    return render_template('home.html',token=tokenDeUsuario)

"""
registra una publicacion de una mascota encontrada, tiene que tener una secion iniciada
GET: renderiza registrar.html para rellenar un formulario
POST: recibe por request.form, la informacion de del registro, lo envia por requests a la api
"""
@app.route('/registrar', methods=['GET','POST']) 
def registrar():
    if request.method == 'GET':
        return render_template('registrar.html')
    elif request.method == 'POST':

        tokenDeUsuario = request.form.get('ftoken')
        #print("verifico token" + str(tokenDeUsuario))
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
            

            # Realizar la solicitud POST
            response = requests.post(f'{BackendLink}/registrarMascota', json=datos)
            
            # Verificar la respuesta del servidor
            if response.status_code == 201:
                return redirect(url_for('index'))
        return render_template('registrar.html')


"""
Renderiza "perfilmascota.html" . id es el numero de identidad, de una publicacion de mascota y muestra sus datos.
envia un requests a la api del backend para pedir la informacion
"""
@app.route('/PerfilMascota/<id>')
def perfil_mascota(id):
    mascotaid = id
    data = {"mascotaid": mascotaid}
    print(data)
    response=requests.post(f'{BackendLink}/buscarmascotas', json=data)
    
    if response.status_code == 200:
        print(response)
        mascota = response.json()[0]
        return render_template("PerfilMascota.html", mascota=mascota)
    return render_template("404.html")

"""
envia una peticion delete a la api del backend para eliminar una mascota por id
GET: redirecciona al index
POST: toma por request.for el id de la mascota y envia una peticion delete al backend
"""
@app.route('/eliminarMascota',methods=["GET", "POST"])
def eliminarMascota():
    if request.method == "GET":
        return redirect(url_for("index"))
    mascotaid = request.form.get("fmascotaid")
    datos = {
        'mascotaid': mascotaid
        }
    response = requests.delete(f'{BackendLink}/eliminarmascota', json=datos)
    if response.status_code == 202:
        return redirect(url_for("miperfil"))
    else:
        return redirect(url_for("index"))


"""
Registro de usuario
GET: renderiza el "registrarusuario.html"
POST: toma por request.for el nombre de usuario, la contraseña y el contacto, envia una peticion post al backend con esa informacion
"""
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


"""
Pagina web donde esta el registro de las mascotas buscadas
GET: renderiza "buscadas.html" con la tabla completa
POST: toma por request.for el la especie,la raza y el sexo del animal buscado, envia una peticion post al backend con esa informacion
    esta vacio por defecto
"""
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
    if tabla.status_code == 200:
        tabla = tabla.json()
    return render_template('buscadas.html',tablaDeMascotas=tabla)

"""
Devuelve una lista de diccionarios de las tablas de mascotas y centros de mascotas
GET: envia una peticion requests para traer la infomracion de las mascotas y centros para mascotas registrados
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


"""
inicio de secion de usuario
GET: renderiza el "login.html"
POST: toma por request.for el nombre de usuario, la contraseña, envia una peticion post al backend con esa informacion, recibe un token
"""
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
        respuesta = requests.get(f'{BackendLink}/login', json=datos)
        if respuesta.status_code == 200:
            tokenDeUsuario = respuesta.json().get('token')
            token = tokenDeUsuario
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
     return render_template ('login.html')

"""
cierra la secion de usuario
GET: renderiza el "logout.html"
"""
@app.route('/logout', methods=['GET'])
def logout():
    return render_template ('logout.html')

"""
Mi perfil de usuario, necesita tener la sescion iniciada, puede eliminar y revisar informacion de sus mascotas registradas
GET: renderiza el "autorizacion.html" para validar la secion
POST: Valida el token y dependiendo de la informacion del usuario traer la informacion de las mascotas posteadas por el usuario
"""
@app.route('/miperfil', methods=['GET', 'POST'])
def miperfil():
    if request.method == 'POST':
        tokenDeUsuario = request.form.get('token') 
        if tokenDeUsuario:
            try:
                # Intenta decodificar el token
                decodeDeUsuario = decode_token(token).get('sub')
            except (JWTDecodeError, JWTExtendedException, Exception) as e:
                print(f"Ha ocurrido un error al decodificar el token: {e}")
                return redirect(url_for('login'))
            user_id = decodeDeUsuario["user_id"]
            nombreDeUsuario = decodeDeUsuario["username"]
            datos = {"id":user_id}
            respuesta = requests.get(f'{BackendLink}/mascotaDeUsuario', json=datos)
            if respuesta.status_code == 200:
                listaDeMascotas = respuesta.json()
                return render_template('miperfil.html', nombreDeUsuario=nombreDeUsuario,listaDeMascotas=listaDeMascotas)
            else:
                return redirect(url_for('registro'))
        else:
            return redirect(url_for('login'))
    return render_template('autorizacion.html') 

"""
Hace una consulta a la api de google map y recibe un scrip y lo devuelve
"""
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