from flask import Flask, jsonify, Response
import requests  # Se utiliza para hacer consultas a APIs externas
import os  # Se utiliza para interactuar con variables de entorno
from dotenv import load_dotenv  # Se utiliza para cargar variables de entorno desde un archivo .env

PORT = 8080

load_dotenv()  # Carga las variables de entorno desde el archivo .env si existe
app = Flask(__name__)

BackendLink = os.getenv('backend_link')  # Obtiene el valor de la variable de entorno 'backend_link'

@app.route('/')
def index():
    respuesta = requests.get(f'{BackendLink}')  # Realiza una solicitud GET a la URL almacenada en 'BackendLink'

    return jsonify(respuesta.json())  # Devuelve la respuesta JSON de la solicitud realizada
    
@app.route('/registrar')
def registrar():
    if request.method == "POST": # Si se envía el formulario, prepara el JSON con los datos de la misma, y lo devuelve
        mascota = {
            'tipo' : request.form.get('ftipo'),
            'raza' : request.form.get('fraza'),
            'sexo' : request.form.get('fsexo'),
            'detalles' : request.form.get('fdetalles'),
            'zona' : request.form.get('fzona'),
            'calle' : request.form.get('fcalle'),
            'altura' : request.form.get('faltura'),
            
        }
    return jsonify(mascota)
    else:
        return render_template('registrar.html') 
        
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



if __name__ == '__main__':
    app.run(debug=True, port=PORT)
