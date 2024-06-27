from flask import Flask, jsonify, render_template, Response,request,redirect,url_for
import requests  # Se utiliza para hacer consultas a APIs externas
import os  # Se utiliza para interactuar con variables de entorno
from dotenv import load_dotenv  # type: ignore # Se utiliza para cargar variables de entorno desde un archivo .env

load_dotenv()  # Carga las variables de entorno desde el archivo .env si existe
BACKEND_LINK = 'http://127.0.0.1:5000'  # Obtiene el valor de la variable de entorno 'backend_link'
API_KEY = 'AIzaSyD7gp-t7RRuboSEbhyK3kGBOAGaDjUBOsg' #api de google cloud
BASE_URL = "https://maps.googleapis.com/maps/api/js"
PORT = 8080

app = Flask(__name__)


"""
redenreriza el home html, pagina de inicio de la web
"""
@app.route('/')
def index():
    return render_template('home.html')

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

        usuarioid = request.form.get('fusuarioid')
        imagen_mascota=request.files.get("fimagen")
       
        #print("verifico token" + str(tokenDeUsuario))
        if usuarioid:
            especie = request.form.get('ftipo')
            sexo = request.form.get('fsexo')
            raza = request.form.get('fraza')
            detalles = request.form.get('fdetalles')
            zona = request.form.get('fzona')
            calle = request.form.get('fcalle')
            altura = request.form.get('faltura')

            datos= {
                'usuarioid': usuarioid,
                'especie': especie,
                'sexo': sexo,
                'raza': raza,
                'detalles': detalles,
                'zona': zona,
                'calle': calle,
                'altura': altura
            }

            # Imprimir la URL y los datos para depuración
            print(f'{BACKEND_LINK}/registrarmascota')
            print(datos)
            print(imagen_mascota)
            #if imagen_mascota:
                #response = requests.post(f'{BACKEND_LINK}/registrarMascota', json=datos)
            #    response = requests.post(f'{BACKEND_LINK}/registrarMascota', json=datos, files={'fimagen': imagen_mascota})
            #else:
                # Realizar la solicitud POST
            response = requests.post(f'{BACKEND_LINK}/registrarMascota', json=datos)
            mascota_id = response.json().get("mascota_id")
            
            if imagen_mascota and response.status_code == 201:
                nombreArchivo = f"{mascota_id}_mascota.jpg"
                imagen_mascota.save(os.path.join("static","image/mascotas", nombreArchivo))
            
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
    response=requests.post(f'{BACKEND_LINK}/buscarmascotas', json=data)
    
    if response.status_code == 200:
        mascota = response.json()[0]
        print(mascota)
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
    response = requests.delete(f'{BACKEND_LINK}/eliminarmascota', json=datos)
    if response.status_code == 202:
        return redirect(url_for("mi_perfil"))
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
        response=requests.post(f'{BACKEND_LINK}/registrarusuario', json=usuario)
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
        "sexo": "",
        "estado": ""
    }
    if request.method == "POST":
        especie = request.form.get("mespecie")
        raza = request.form.get("mraza")
        sexo = request.form.get("msexo")
        estado = request.form.get("mestado")

        datos = {
            "especie": especie,
            "raza": raza,
            "sexo": sexo,
            "estado":estado
        }
    tabla = requests.post(f'{BACKEND_LINK}/buscarmascotas', json=datos)
    if tabla.status_code == 200:
        tabla = tabla.json()
        return render_template('buscadas.html',listaDeMascotas=tabla)
    tabla = []
    return render_template('buscadas.html',listaDeMascotas=tabla)

"""
Devuelve una lista de diccionarios de las tablas de mascotas y centros de mascotas
GET: envia una peticion requests para traer la infomracion de las mascotas y centros para mascotas registrados
"""
@app.route('/cargarTablas')
def cargar_tablas():
    tabla_de_mascota = {}
    tabla_de_casas = {}
    try:
        res_mascotas = requests.get(f'{BACKEND_LINK}/tablademascotas')
        res_casas = requests.get(f'{BACKEND_LINK}/tabladecentros')
        
        # Comprobamos si las peticiones fueron exitosas
        if res_mascotas.status_code == 200 and res_casas.status_code == 200:
            tabla_de_mascota = res_mascotas.json()
            tabla_de_casas = res_casas.json()
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    tablas_de_mascotas_y_casas = [
        {
            "tablaDeMascota": tabla_de_mascota,
        },
        {
            "tablaDeCasas": tabla_de_casas
        }
    ]
    return jsonify(tablas_de_mascotas_y_casas)


"""
inicio de secion de usuario
GET: renderiza el "login.html"
POST: toma por request.for el nombre de usuario, la contraseña, envia una peticion post al backend con esa informacion, recibe un token
"""
@app.route('/login', methods=['GET','POST'])
def login():
    usuarioid = ""
    if request.method == 'POST':
        nombre = request.form.get('fnombre') 
        contraseña = request.form.get('fcontraseña')
        datos = {
            "nombre": nombre,
            "contraseña": contraseña
        }
        respuesta = requests.get(f'{BACKEND_LINK}/login', json=datos)
        if respuesta.status_code == 200:
            usuarioid = respuesta.json().get('usuarioid')
    return render_template ('login.html', usuarioid = usuarioid)

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
def mi_perfil():
    if request.method == 'POST':
        user_id = request.form.get('usuarioid') 
        if user_id:
            datos = {"usuarioid":user_id}
            respuesta_mascotas = requests.get(f'{BACKEND_LINK}/mascotaDeUsuario', json=datos)
            respuesta_usuario = requests.get(f'{BACKEND_LINK}/datosDeUsuario', json=datos)
        user_id = request.form.get('usuarioid') 
        if user_id:
            datos = {"usuarioid":user_id}
            respuesta_mascotas = requests.get(f'{BACKEND_LINK}/mascotaDeUsuario', json=datos)
            respuesta_usuario = requests.get(f'{BACKEND_LINK}/datosDeUsuario', json=datos)
            print(respuesta_mascotas)
            print(respuesta_usuario)
            if respuesta_mascotas.status_code == 200:
                lista_de_mascotas = respuesta_mascotas.json()
                info_usuario = respuesta_usuario.json()
                print(lista_de_mascotas)
                
                return render_template('miperfil.html', infoUsuario=info_usuario ,tablaDeMascotas=lista_de_mascotas)

            else:
                lista_de_mascotas = []
                info_usuario = respuesta_usuario.json()
                return render_template('miperfil.html', infoUsuario=info_usuario ,tablaDeMascotas=lista_de_mascotas)
        else:
            return redirect(url_for('login'))
    return render_template('autorizacion.html') 

"""
Hace una consulta a la api de google map y recibe un scrip y lo devuelve
"""
@app.route('/script')
def conseguir_script():
    base_url = BASE_URL
    params = {
        "key": API_KEY,
        "v": "beta",
        "callback": "initMap"  # llama la funcion cuando carga la pagina
    }
    libraries = ["marker", "places", "geocoding"]  # Lista de bibliotecas a importar
    params["libraries"] = ",".join(libraries)
    script_de_mapa= requests.get(base_url, params=params)


    if script_de_mapa.status_code == 200:
        return script_de_mapa.text

@app.route('/preguntasfrecuentes', methods=['GET'])
def faq():
    respuesta = requests.get(f'{BACKEND_LINK}/tabla_faq')
    print(respuesta)
    if(respuesta.status_code == 200):
        tabla_faq= respuesta.json()
        print(tabla_faq)
        return render_template ('faq.html', tabla_faq=tabla_faq)
    return render_template("404.html")
    


@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=PORT)