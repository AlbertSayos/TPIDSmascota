from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

PORT = 8081

app = Flask(__name__)
engine = create_engine('mysql+mysqlconnector://user:pass@host/DBname') 
#reemplazar 'user', 'pass', 'host' y 'DBname' con los datos correspondientes

@app.route('/tablademascotas', methods=["GET"])
def mostrar_tabla_de_mascotas():
    conexion = engine.connect() #establezco la conexion con la base de datos
    query = 'SELECT * FROM mascotas;'

    try: 
       resultado=conexion.excute(text(query))
       conexion.close()
    except SQLAlchemyError as error:
       return jsonify({'error': str(error.__cause__)})
    
    mascotas = []
    for fila in resultado:
       mascota = {}
       mascota['id'] = fila.id
       mascota['especie'] = fila.especie
       mascota['sexo'] = fila.sexo
       mascota['raza'] = fila.raza
       mascota['detalles'] = fila.detalles
       mascota['contacto'] = fila.contacto
       mascota['EnBusqueda'] = fila.EnBusqueda
       mascota['IDusuario'] = fila.IDusuario
       mascotas.append(mascota)
    return jsonify(mascotas)


if __name__ == '__main__':
  app.run(debug=True, port=PORT)
