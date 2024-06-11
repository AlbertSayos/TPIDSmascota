from flask import Flask, jsonify, render_template, Response, request, redirect, ulr_for
import requests  # Se utiliza para hacer consultas a APIs externas
import os  # Se utiliza para interactuar con variables de entorno
from dotenv import load_dotenv  # Se utiliza para cargar variables de entorno desde un archivo .env
from flask_jwt_extended import JWTManager, create_access_token, decode_token
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

@app.route('/registrar', methods=["GET", "POST"])
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

@app.route('/buscadas')
def buscadas():
    return render_template('buscadas.html')

@app.route('/cargarMapa')
def cargarMapa():
    return render_template('mapDeEjemplo.html', api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True, port=PORT)