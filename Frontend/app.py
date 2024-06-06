from flask import Flask, jsonify, render_template, Response
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

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/cargarMapa')
def cargarMapa():
    api_key = os.getenv('APIKEY') #api de google cloud
    print("lo pase")
    return render_template('mapDeEjemplo.html', api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True, port=PORT)