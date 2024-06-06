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
    if request.method == "POST":
        mascota = {
            'tipo' : request.form.get('ftipo'),
            'raza' : request.form.get('fraza'),
            'sexo' : request.form.get('fsexo'),
            'detalles' : request.form.get('fdetalles') 
        }
            
    else:
        return render_template('registrar.html')
    
    

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
