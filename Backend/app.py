from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

PORT = 8080

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

@app.route('/tabladecentros', methods=["GET"])
def mostrar_tabla_de_centros():
   conexion = engine.connect() 
   query = "SELECT * FROM centros;"
    
   try:
       resultado = conexion.execute(text(query))
       conexion.close()
   except SQLAlchemyError as error:
       return jsonify({'error': str(error.__cause__)})
   centros = []
   for fila in resultado:
      centro = {}
      centro['id_centro'] = fila.id_centro
      centro['nombre'] = fila.nombre
      centro['datos'] = fila.datos
      centro['zona'] = fila.zona
      centro['calle'] = fila.calle
      centro['altura'] = fila.altura
      centros.append(centro)
   return jsonify(centros)

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
   
@app.route('/buscarmascotas', methods=['GET'])
def buscar_mascotas():
   #Uso query parameters. En caso de que el usuario quiera omitir un parametro al buscar una mascota puede hacerlo
   #Ejemplo URL: http://localhost:8081/buscarmascotas?especie=perro&raza=labrador&sexo=hembra 
   especie = request.args.get('especie', default=None, type=str) 
   raza = request.args.get('raza', default=None, type=str)
   sexo = request.args.get('sexo', default=None, type=str)

   conexion = engine.connect()
   parametros=[]

   if not especie is None:

      parametros.append(f'especie = "{especie}"')
   if not raza is None:
      parametros.append(f'raza = "{raza}"')
   if not sexo is None:
      parametros.append(f'sexo = "{sexo}"')

   if len(parametros) == 0:
      query_mascotas = 'SELECT * FROM mascotas;'
   else: 
      query_mascotas= f'SELECT * FROM mascotas WHERE'+ ' AND'.join(parametros) + ';'

   try: 
       resultado_mascotas=conexion.execute(text(query_mascotas))
       conexion.close()
   except SQLAlchemyError as error:
       return jsonify({'error': str(error.__cause__)})

   mascotas=[]
   for fila in resultado_mascotas:
      mascotas.append({
         'id': fila.id,
         'especie': fila.especie,
         'sexo': fila.sexo,
         'raza': fila.raza,
         'detalles': fila.detalles,
         'zona' : fila.zona,
         'calle' : fila.calle,
         'altura': fila.altura,
         'contacto' : fila.contacto,
         'estado' : fila.estado,
   })

   return jsonify(mascotas)

if __name__ == '__main__':
  app.run(debug=True, port=PORT)
