from flask import Flask, jsonify,request
import os
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


PORT = 8081

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('contraseña')
app.config['SECRET_KEY'] = os.getenv('contraseña')
jwt = JWTManager(app)

engine = create_engine('mysql+mysqlconnector://root:tp@localhost/tp')
#reemplazar 'user', 'pass', 'host' y 'DBname' con los datos correspondientes

#**************************************************endpoind de mascotas*************************************************************#
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
       #mascota['estado'] = fila.estado
       mascota['usuarioid'] = fila.usuarioid
       mascotas.append(mascota)
    return jsonify(mascotas)

@app.route('/tablademascotas', methods=['DELETE'])
def eliminar_mascota():
   conexion = engine.connect()
   mascota =request.get_json() #recibe los datos en formato json
   id_mascota = mascota.get('mascotaid')

   query = f'DELETE FROM mascotas WHERE mascotaid = {id_mascota};'

   validar_query = f'SELECT * FROM mascotas WHERE mascotaid = {id_mascota};'

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
      centro['centroid'] = fila.centroid
      centro['nombre'] = fila.nombre
      centro['descripcion'] = fila.descripcion
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

@app.route('/registrarMascota', methods=['POST'])
def registrarMascota():
   conexion = engine.connect() #establezco la conexion con la base de datos
   data = request.get_json()
   
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
   imagen_mascota = request.files.get('fimagen')
   query_contacto = f"SELECT contacto FROM usuarios WHERE usuarioid ={id_usuario};"
   
   try: 
      contacto = conexion.execute(text(query_contacto)).fetchone()
   except SQLAlchemyError as error:
      conexion.close()
      return jsonify({'error': str(error.__cause__)}),500
   
   query = f"INSERT INTO mascotas (especie, raza, sexo, descripcion, zona, calle, altura, contacto,usuarioid) VALUES ('{especie}', '{raza}', '{sexo}', '{detalles}', '{zona}', '{calle}', {altura}, '{contacto[0]}', '{id_usuario})"
   
   try: 
      conexion.execute(text(query))
      conexion.commit()
      mascota_id=conexion.lastrowid
      
      if imagen_mascota:
         nombreArchivo = f"{mascota_id}_mascota.jpg"
         imagen_mascota.save(os.path.join("static","image", nombreArchivo))
      conexion.close()
   except SQLAlchemyError as error:
      conexion.close()
      return jsonify({'error': str(error.__cause__)}),500
   return jsonify({'mensaje': 'La mascota se ha registrado correctamente'}),201
   
   
@app.route('/buscarmascotas', methods=['GET'])
def buscar_mascotas():
   conexion = engine.connect()
   busqueda_mascota=request.get_json()

   especie = request.get('especie') 
   raza = request.get('raza')
   sexo = request.get('sexo')


   query_mascotas= f"SELECT * FROM mascotas WHERE especie={especie} AND raza={raza} AND sexo={sexo};"

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
            #'estado' : fila.estado,
      })
      return jsonify(mascotas_buscadas),200
   return jsonify({'mensaje': 'No existen mascotas con esas caracteristicas'}),404


#**************************************************endpoind de usuarios*************************************************************#
@app.route('/login', methods=['GET'])
def login():
   conexion = engine.connect()
   login= request.get_json()
   usuario = request.get('usuario')
   contraseña = request.get('contraseña')

   query_usuario = f"SELECT * FROM usuarios WHERE nombre = '{usuario}';"
   
   try: 
      resultado=conexion.execute(text(query_usuario)).fetchone()
      if not resultado.nombre:
         conexion.close() 
         return jsonify({'error': 'No se encontraron usuarios'}), 404
      conexion.close()
      if (contraseña == resultado.contraseña):
         token = create_access_token(identity={'username': resultado.nombre,'user_id': resultado.usuarioid})
         try:
            conexion2 = engine.connect()
            querry_token = f"UPDATE usuarios SET token = '{token}' WHERE nombre = '{resultado.nombre}';"
            conexion2.execute(text(querry_token))
            conexion2.commit()
            conexion2.close()
         except Exception as e:
            print("Error:", e)
         return jsonify(token=token), 200
      else:
         return jsonify({"mensaje": "Credenciales inválidas"}), 401
   
   except SQLAlchemyError as error:
       return jsonify({'error': str(error.__cause__)}), 500

@app.route('/registrar', methods=['POST'])
def registrarUsuario():
   
   conexion = engine.connect()
   nuevo_usuario =request.get_json() #recibe los datos en formato json

   nombre = nuevo_usuario.get('nombre')
   contraseña = nuevo_usuario.get('contraseña')
   contacto = nuevo_usuario.get('contacto')

   query_nuevo_usuario= f"INSERT INTO usuarios (nombre, contraseña, contacto) VALUES ('{nombre}', '{contraseña}', '{contacto}');"
   
   try:
      resultado= conexion.execute(text(query_nuevo_usuario))
      conexion.commit()
      conexion.close()
   except SQLAlchemyError as error:
        return jsonify({'error': 'No se pudo registrar el usuario' + str(error.__cause__)}),404
   return jsonify({'mensaje': 'Se ha registrado el usuario con exito'}), 201

@app.route('/mascotaDeUsuario', methods=['GET'])
def mascotaDeUsuario():
   conexion = engine.connect()
   usuario = request.get_json()
   usuario_id= request.get('id')
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
            'estado' : fila.estado
         })
      return jsonify(mascotaDeUsuario),200
   return jsonify (({'mensaje': 'El usuario no existe.'}), 404)

if __name__ == '__main__':
  app.run(debug=True, port=PORT)
