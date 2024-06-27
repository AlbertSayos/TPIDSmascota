from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import create_engine, text,inspect
from sqlalchemy.exc import SQLAlchemyError


PORT = 8081

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('contraseña')
app.config['SECRET_KEY'] = os.getenv('contraseña')



engine = create_engine('mysql+mysqlconnector://root:tp@localhost:3300/tp')
#reemplazar 'user', 'pass', 'host' y 'DBname' con los datos correspondientes

#**************************************************endpoind de mascotas*************************************************************#
"""
Devuelve un json con informacion de las mascotas: mascotaid,especie,sexo,raza, descripcion, zona, calle, altura,contacto,usuarioid
"""
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
       mascota['mascotaid'] = fila.mascotaid
       mascota['especie'] = fila.especie
       mascota['sexo'] = fila.sexo
       mascota['raza'] = fila.raza
       mascota['descripcion'] = fila.descripcion
       mascota['zona'] =fila.zona
       mascota['calle']=fila.calle
       mascota['altura']=fila.altura
       mascota['contacto'] = fila.contacto
       mascota['estado'] = fila.estado
       mascota['usuarioid'] = fila.usuarioid
       mascotas.append(mascota)
    return jsonify(mascotas)

"""
elimina de la base de datos un registro de una mascota por su id
"""
@app.route('/eliminarmascota', methods=['DELETE'])#
def eliminar_mascota():
   conexion = engine.connect()
   mascota = request.json #recibe los datos en formato json
   id_mascota = mascota.get('mascotaid')

   query = f'DELETE FROM mascotas WHERE mascotaid = {id_mascota};'

   validar_query = f'SELECT * FROM mascotas WHERE mascotaid = {id_mascota};'
   print("validar query " + validar_query)
   print("query " + query)
   try:
      val_resultado= conexion.execute(text(validar_query))

      if val_resultado.rowcount != 0:
         resultado = conexion.execute(text(query))
         conexion.commit()
         conexion.close()
      else:
         conexion.close()
         return jsonify({'mensaje': 'La mascota no existe'}),404
      
   except SQLAlchemyError as error:
      return jsonify({'error': str(error.__cause__)})
   return jsonify ({'mensaje': 'La mascota se ha eliminado con exito'}), 202

"""
Devuelve un json con informacion de las mascotas: centroid,nombre, descripcion, zona, calle, altura,contacto
"""
@app.route('/tabladecentros', methods=["GET"])#
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
      centro['centroid'] = fila.centroid
      centro['nombre'] = fila.nombre
      centro['descripcion'] = fila.descripcion
      centro['zona'] = fila.zona
      centro['calle'] = fila.calle
      centro['altura'] = fila.altura
      centros.append(centro)
   return jsonify(centros)

"""
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
"""


"""
Recibe un json con informacion sobre la mascota: usuarioid,especie,sexo,raza,detalles,zona,calle,altura. hace una peticion POST a 
la base de datos para guadar la informacion
"""
@app.route('/registrarMascota', methods=['POST'])
def registrarMascota():
   print("hola")
   conexion = engine.connect() #establezco la conexion con la base de datos
   #imagen_mascota = request.files.get('fimagen')

   print("hola 2")
   data = request.json
   
   if not data:
      return jsonify({'error': 'No data provided'}), 400
   id_usuario = data.get('usuarioid')
   especie = data.get('especie')
   sexo = data.get('sexo')
   raza = data.get('raza')
   detalles = data.get('detalles')
   zona = data.get('zona')
   calle = data.get('calle')
   altura = data.get('altura')
   estado = data.get('estado')

   query_contacto = f"SELECT contacto FROM usuarios WHERE usuarioid ={id_usuario};"
   
   try: 
      contacto = conexion.execute(text(query_contacto)).fetchone()
   except SQLAlchemyError as error:
      conexion.close()
      return jsonify({'error': str(error.__cause__)}),500

   query = f"INSERT INTO mascotas (especie, raza, sexo, descripcion, zona, calle, altura, contacto,usuarioid, estado) VALUES ('{especie}', '{raza}', '{sexo}', '{detalles}', '{zona}', '{calle}', {altura}, '{contacto[0]}', {id_usuario}, '{estado}')"
   print(query)
   try: 
      conexion.execute(text(query))
      conexion.commit()
      result = conexion.execute(text("SELECT LAST_INSERT_ID()"))
      
      mascota_id = result.fetchone()[0]
      print(mascota_id)
      """
      if imagen_mascota:
         nombreArchivo = f"{mascota_id}_mascota.jpg"
         print("llegue aca")
         imagen_mascota.save(os.path.join("static","image", nombreArchivo))
         """
      conexion.close()
   except SQLAlchemyError as error:
      conexion.close()
      return jsonify({'error': str(error.__cause__)}),500
   return jsonify({'mascota_id': mascota_id}),201

"""
Recibe un json con la informacion de la mascota: mascotaid,especie, raza, sexo. y busca en la tabla mascota que cumplan con esas caracteristicas
"""
@app.route('/buscarmascotas', methods=['POST'])
def buscar_mascotas():
   conexion = engine.connect()
   busqueda_mascota=request.json
   parametros=[]
   id_mascota = busqueda_mascota.get('mascotaid') if 'mascotaid' in busqueda_mascota else ""
   especie = busqueda_mascota.get('especie') if 'especie' in busqueda_mascota else ""
   raza = busqueda_mascota.get('raza') if 'raza' in busqueda_mascota else ""
   sexo = busqueda_mascota.get('sexo') if 'sexo' in busqueda_mascota else ""
   estado = busqueda_mascota.get('estado') if 'estado' in busqueda_mascota else ""

   if id_mascota:
      parametros.append(f"mascotaid = {id_mascota}")
   if especie:
      parametros.append(f"especie = '{especie}'")
   if raza:
      parametros.append(f"raza = '{raza}'")
   if sexo:
      parametros.append(f"sexo = '{sexo}'")
   if estado:
      parametros.append(f"estado = '{estado}'")
   print(parametros)
   if len(parametros) == 0:
      query_mascotas = 'SELECT * FROM mascotas;'
   else: 
      query_mascotas= f"SELECT * FROM mascotas WHERE "+ "AND ".join(parametros) + ";"
   
   try: 
       resultado_mascotas=conexion.execute(text(query_mascotas))
       conexion.close()
   except SQLAlchemyError as error:
       return jsonify({'error': str(error.__cause__)}),500

   if resultado_mascotas.rowcount!=0:
      mascotas_buscadas=[]
      for fila in resultado_mascotas:
         mascotas_buscadas.append({
            'especie': fila.especie,
            'sexo': fila.sexo,
            'raza': fila.raza,
            'descripcion': fila.descripcion,
            'zona' : fila.zona,
            'calle' : fila.calle,
            'altura': fila.altura,
            'contacto' : fila.contacto,
            'mascotaid' : fila.mascotaid,
            'estado' : fila.estado,
      })
      
      return jsonify(mascotas_buscadas),200
   return jsonify({'mensaje': 'No existen mascotas con esas caracteristicas'}),404


#**************************************************endpoind de usuarios*************************************************************#
"""
recibe por un json un numbre de usuario "nombre" y una contraseña "contraseña" y devuelve el id del usuario si es correcto
"""
@app.route('/login', methods=['GET'])
def login():
   conexion = engine.connect()
   
   login= request.json

   usuario = login.get('nombre')
   contraseña = login.get('contraseña')
   query_usuario = f"SELECT * FROM usuarios WHERE nombre = '{usuario}';"
   
   try: 
      resultado=conexion.execute(text(query_usuario)).fetchone()
      if not resultado.nombre:
         conexion.close() 
         return jsonify({'error': 'No se encontraron usuarios'}), 404
      conexion.close()
      if (contraseña == resultado.contraseña):
         return jsonify({"usuarioid": resultado.usuarioid}), 200
      else:
         return jsonify({"mensaje": "Credenciales inválidas"}), 401
   
   except SQLAlchemyError as error:
       return jsonify({'error': str(error.__cause__)}), 500

"""
Recibe por un json un numbre de usuario "nombre",una contraseña "contraseña", y un contacto "contacto"
guarda esa informacion en la base de datos, 201 si se guardo con exito
"""
@app.route('/registrarusuario', methods=['POST'])
def registrarUsuario():
   
   conexion = engine.connect()
   nuevo_usuario =request.json #recibe los datos en formato json

   nombre = nuevo_usuario.get('nombre')
   contraseña = nuevo_usuario.get('contraseña')
   contacto = nuevo_usuario.get('contacto')
   
   query_nombre=f"SELECT * FROM usuarios where nombre='{nombre}'"
   try:
      resultado_nombre = conexion.execute(text(query_nombre)).fetchone()

      if resultado_nombre:
         conexion.close()
         return jsonify({"mensaje": "Nombre de usuario no disponible"}), 409
      
      query_nuevo_usuario= f"INSERT INTO usuarios (nombre, contraseña, contacto) VALUES ('{nombre}', '{contraseña}', '{contacto}');"
      resultado= conexion.execute(text(query_nuevo_usuario))
      conexion.commit()
      conexion.close()   
   except SQLAlchemyError as error:
        return jsonify({'error': 'No se pudo registrar el usuario' + str(error.__cause__)}),404
   return jsonify({'mensaje': 'Se ha registrado el usuario con exito'}), 201


"""
recibe por json el usuarioid y devuelve un json las mascotas que esten asociadas a ese usuarioid
"""
@app.route('/mascotaDeUsuario', methods=['GET'])
def mascotaDeUsuario():
   conexion = engine.connect()
   usuario = request.json
   usuario_id= usuario.get('usuarioid')
   query = f'SELECT * from mascotas WHERE usuarioid = {usuario_id};'

   try:
      resultado= conexion.execute(text(query))
      conexion.close()
   except SQLAlchemyError as error:
      return jsonify({'error': str(error.__cause__)})

   if resultado.rowcount !=0:
      mascotaDeUsuario=[]
      for fila in resultado:
         mascotaDeUsuario.append({
            'especie' : fila.especie,
            'sexo' : fila.sexo,
            'raza' : fila.raza,
            'descripcion': fila.descripcion,
            'zona' : fila.zona,
            'calle' : fila.calle,
            'altura' : fila.altura,
            'contacto' : fila.contacto,
            'mascotaid': fila.mascotaid
            #'estado' : fila.estado
         })
      return jsonify(mascotaDeUsuario),200
   return jsonify [{'mensaje': 'El usuario no tiene mascotas.'}], 404

@app.route('/datosDeUsuario', methods=['GET'])
def datosDeUsuario():
   conexion = engine.connect()
   usuario = request.json
   usuario_id= usuario.get('usuarioid')
   query = f'SELECT * from usuarios WHERE usuarioid = {usuario_id};'
   print(query)
   try:
      resultado= conexion.execute(text(query))
      conexion.close()
   except SQLAlchemyError as error:
      return jsonify({'error': str(error.__cause__)})
   
   if resultado.rowcount !=0:
      datosDeUsuario=[]
      for fila in resultado:
         datosDeUsuario.append({
            'nombre': fila.nombre,
            'contacto': fila.contacto
         })
      return jsonify(datosDeUsuario),200
   return jsonify (({'mensaje': 'El usuario no existe.'}), 404)

@app.route('/tabla_faq', methods=['GET'])
def tabla_faq():
   conexion = engine.connect() #establezco la conexion con la base de datos
   query = 'SELECT * FROM preguntas_respuestas;'

   try:
      resultado=conexion.execute(text(query))
      conexion.close()
   except SQLAlchemyError as error:
      return jsonify({'error': str(error.__cause__)})
    
   preguntas_respuestas = []
   for fila in resultado:
      pregunta_respuesta = {}
      pregunta_respuesta['pregunta'] = fila.pregunta
      pregunta_respuesta['respuesta'] = fila.respuesta
      preguntas_respuestas.append(pregunta_respuesta)
   return jsonify(preguntas_respuestas)




if __name__ == '__main__':
  app.run(debug=True, port=PORT)
