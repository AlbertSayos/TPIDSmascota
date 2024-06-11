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

engine = create_engine('mysql+mysqlconnector://root:@localhost/mascotas')
engineUsuarios = create_engine('mysql+mysqlconnector://root:@localhost/usuarios')
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
   
@app.route('/buscarmascotas', methods=['GET'])
def buscar_mascotas():
   #Uso query parameters. En caso de que el usuario quiera omitir un parametro al buscar una mascota puede hacerlo
   #Ejemplo URL: http://localhost:8081/buscarmascotas?id=1&especie=perro&raza=labrador&sexo=hembra
   id_mascota=request.args.get('id', default=None, type=int) 
   especie = request.args.get('especie', default=None, type=str) 
   raza = request.args.get('raza', default=None, type=str)
   sexo = request.args.get('sexo', default=None, type=str)
   print(especie)
   conexion = engine.connect()
   parametros=[]

   if not id_mascota is None:
      parametros.append(f'id = {id_mascota}')
   if not especie is None:
      parametros.append(f"especie = '{especie}'")
   if not raza is None:
      parametros.append(f"raza = '{raza}'")
   if not sexo is None:
      parametros.append(f"sexo = '{sexo}'")
   
   if len(parametros) == 0:
      query_mascotas = 'SELECT * FROM mascotas;'
   else: 
      query_mascotas= f"SELECT * FROM mascotas WHERE "+ "AND ".join(parametros) + ";"
      
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


@app.route('/registrarMascota', methods=['POST'])
def registrarMascota():
   #Ejemplo URL:  requests.get(f'{BackendLink}/registrar?usuarioid={decode.user_id}&tipo={tipo}&raza={raza}&sexo={sexo}&detalles={detalles}&zona={zona}&calle={calle}&altura={altura}')
   pass

#**************************************************endpoind de usuarios*************************************************************#
@app.route('/login', methods=['GET'])
def login():
   #Ejemplo URL: http://localhost:8081/login?usuario=Marcos&contraseña=contraseña123
   usuario = request.args.get('usuario', default=None, type=str) 
   contraseña = request.args.get('contraseña', default=None, type=str)
   conexion = engineUsuarios.connect()
   querry_usuario = f"SELECT * FROM usuarios WHERE nombre = '{usuario}';"
   print(usuario)
   try: 
      resultado=conexion.execute(text(querry_usuario)).fetchone()
      if not resultado.nombre:
         conexion.close() 
         return jsonify({'error': 'No se encontraron usuarios'}), 404
      conexion.close()
      if (contraseña == resultado.contraseña):
         token = create_access_token(identity={'username': resultado.nombre,'user_id': resultado.usuarioid})
         try:
            conexion2 = engineUsuarios.connect()
            querry_token = f"UPDATE usuarios SET token = '{token}' WHERE nombre = '{resultado.nombre}';"
            conexion2.execute(text(querry_token))
            conexion2.commit()
            conexion2.close()
         except Exception as e:
            print("Error:", e)
         return jsonify(token=token), 200
      else:
         return jsonify({"msg": "Credenciales inválidas"}), 401
   
   except SQLAlchemyError as error:
       return jsonify({'error': str(error.__cause__)}), 500

@app.route('/registrarUsuario', methods=['POST'])
def registrarUsuario():
   #Ejemplo URL: http://localhost:8081/registrarUsuario?nombre=nombre&contraseña=contraseña&contacto=contacto
   pass

@app.route('/mascotaDeUsuario', methods=['GET'])
def mascotaDeUsuario():
   #Ejemplo URL: http://localhost:8081/mascotaDeUsuario?usuarioid=usuarioid
   pass

@app.route('/tablaDeCasas', methods=['GET'])
def tablaDeCasas():
   pass

if __name__ == '__main__':
  app.run(debug=True, port=PORT)
