from flask import Flask, jsonify, render_template, Response
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

@app.route('/cargarMapa')
def cargarMapa():
    return render_template('mapDeEjemplo.html', api_key=api_key)

if __name__ == '__main__':
    app.run(debug=True, port=PORT)