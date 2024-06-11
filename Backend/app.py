from flask import Flask, jsonify, request
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
      resultado=conexion.execute(text(query))
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
      mascota['zona'] =fila.zona
      mascota['calle']=fila.calle
      mascota['altura']=fila.altura
      mascota['contacto'] = fila.contacto
      mascota['estado'] = fila.estado
      mascota['IDusuario'] = fila.IDusuario
      mascotas.append(mascota)
   return jsonify(mascotas)

@app.route('/registrar', methods=["POST"])
def registrar():
   conexion = engine.connect() #establezco la conexion con la base de datos

   """requests.get(f'{BackendLink}/registrar?usuarioid={decode.user_id}&especie={especie}&raza={raza}&sexo={sexo}&detalles={detalles}&zona={zona}&calle={calle}&altura={altura}')"""

   id_usuario = request.args.get('usuarioid', default=None, type=str) 

   especie = request.args.get('especie', default=None, type=str) 
   raza = request.args.get('raza', default=None, type=str)
   sexo = request.args.get('sexo', default=None, type=str)
   detalles = request.args.get('detalles', default=None, type=str) 
   zona = request.args.get('zona', default=None, type=str)
   calle = request.args.get('calle', default=None, type=str)
   altura = request.args.get('altura', default=None, type=str)

   query_contacto = f"SELECT contacto FROM usuarios WHERE usuarioid"

   try: 
      contacto = conexion.execute(text(query_contacto))
      conexion.commit()
      conexion.close()
   except SQLAlchemyError as error:
      return jsonify({'error': str(error.__cause__)})
   
   query = f"INSERT INTO mascotas (usuarioid, especie, sexo, raza, detalles, zona, calle, altura, contacto) VALUES ('{id_usuario}', '{especie}', '{raza}', '{sexo}', '{detalles}', '{zona}', '{calle}', {altura}, '{contacto}')"

   try: 
      conexion.execute(text(query))
      conexion.commit()
      conexion.close()
   except SQLAlchemyError as error:
      return jsonify({'error': str(error.__cause__)})
   return jsonify({'message': 'se ha agregado correctamente' + query})


@app.route('/cargarzona/<zona>', methods=["GET"])
def cargar_zona(zona):
   conexion = engine.connect()
   query_mascotas = f'SELECT * FROM mascotas WHERE zona = {zona};'
   query_centros =  f'SELECT * FROM centros WHERE zona = {zona};'

   try: 
       resultado_mascotas=conexion.execute(text(query_mascotas))
       resultado_centros=conexion.execute(text(query_centros))
       conexion.close()
   except SQLAlchemyError as error:
       return jsonify({'error': str(error.__cause__)})
   
   if resultado_centros.rowcount!= 0 or resultado_mascotas.rowcount!= 0:
      datos={
         'centroTransito': [],
         'mascotasPerdidas': [] 
            }
      for fila in resultado_mascotas:
         datos['mascotasPerdidas'].append({
            'especie':fila.especie,
            'raza':fila.raza,
            'zona':fila.zona,
            'calle':fila.calle,
            'altura':fila.altura
         })
      for fila in resultado_centros:
         datos['centroTransito'].append({
            'nombre':fila.nombre,
            'zona':fila.zona,
            'calle':fila.calle,
            'altura': fila.altura,
            'descripcion':fila.descripcion,
            'contacto':fila.contacto
         })
      return jsonify(datos)
   return jsonify({'mensaje': 'No hay animales ni centros de animales en transito por esta zona'}, 404)
   

if __name__ == '__main__':
  app.run(debug=True, port=PORT)
