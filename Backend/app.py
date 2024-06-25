import flask
import sqlalchemy
import auxiliar
from sqlalchemy.exc import SQLAlchemyError

PORT = 5000
DB_URL = "mysql+mysqlconnector://root:tp@localhost:3300/tp"

app = flask.Flask(__name__)

def establecer_conexion():
    base_de_datos = sqlalchemy.create_engine(DB_URL)
    conexion = base_de_datos.connect()
    return conexion



### Tabla: usuarios // Agregar usuarios ("POST") ###

@app.route("/usuarios/tabla", methods = ["POST"])
def usuarios_tabla():
    conexion = establecer_conexion()
    usuario_nuevo = flask.request.get_json()
    columnas = "nombre, contraseña, contacto"
    valores = auxiliar.obtener_valores(columnas, usuario_nuevo)
    query = f"INSERT INTO usuarios ({columnas}) VALUES ({valores});"

    try:
        conexion.execute(sqlalchemy.text(query))
        conexion.close()
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    mensaje = {"mensaje": "Usuario creado correctamente."}
    return flask.jsonify(mensaje), 201


### Tabla: usuarios // Iniciar sesión ("POST") ###

@app.route("/usuarios/login", methods = ["POST"])
def usuarios_login():
    conexion = establecer_conexion()
    usuario_login = flask.request.get_json()
    query = f"SELECT usuarioid, contraseña FROM usuarios WHERE nombre = '{usuario_login["nombre"]}';"

    try:
        resultado_query = conexion.execute(sqlalchemy.text(query)).fetchone()
        conexion.close()
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    if resultado_query == None:
        mensaje = {"mensaje": "El usuario no existe."}
        return flask.jsonify(mensaje), 404

    elif resultado_query.contraseña == usuario_login["contraseña"]:
        usuarioid = {"usuarioid": resultado_query.usuarioid}
        return flask.jsonify(usuarioid), 200

    else:
        mensaje = {"mensaje": "La contraseña es incorrecta."}
        return flask.jsonify(mensaje), 400



### Tabla: mascotas // Ver tabla ("GET") - Agregar mascotas ("POST") ###

@app.route("/mascotas/tabla", methods = ["GET", "POST"])
def mascotas_tabla():
    conexion = establecer_conexion()

    if flask.request.method == "GET":
        query = "SELECT * FROM mascotas;"

        try:
            resultado_query = conexion.execute(sqlalchemy.text(query))
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        if resultado_query.rowcount == 0:
            mensaje = {"mensaje": "No hay ninguna mascota en la tabla 'mascotas'."}
            return flask.jsonify(mensaje), 404

        json = auxiliar.crear_json(resultado_query, "mascotas")
        return flask.jsonify(json), 200

    elif flask.request.method == "POST":
        mascota_nueva = flask.request.get_json()
        columnas = "nombre, especie, raza, sexo, descripcion, calle, altura, zona, usuarioid, contacto"
        valores = auxiliar.obtener_valores(columnas, mascota_nueva)
        query = f"INSERT INTO mascotas ({columnas}) VALUES ({valores});"

        try:
            conexion.execute(sqlalchemy.text(query))
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Mascota creada correctamente."}
        return flask.jsonify(mensaje), 201


### Tabla: mascotas // Eliminar mascotas ("DELETE") ###

@app.route("/mascotas/eliminar", methods = ["DELETE"])
def mascotas_eliminar():
    conexion = establecer_conexion()
    mascota_eliminada = flask.request.get_json()
    query_verificacion = f"SELECT * FROM mascotas WHERE mascotaid = {mascota_eliminada["mascotaid"]};"

    try:
        resultado_query_verificacion = conexion.execute(sqlalchemy.text(query_verificacion))
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    if resultado_query_verificacion.rowcount == 0:
        mensaje = {"mensaje": "No hay ninguna mascota con dicha id."}
        return flask.jsonify(mensaje), 404

    query = f"DELETE FROM mascotas WHERE mascotaid = {mascota_eliminada["mascotaid"]};"

    try:
        conexion.execute(sqlalchemy.text(query))
        conexion.close()
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    mensaje = {"mensaje": "Mascota eliminada correctamente."}
    return flask.jsonify(mensaje), 200


### Tabla: mascotas // Filtrar mascotas ("POST") ###

@app.route("/mascotas/filtrar", methods = ["POST"])
def mascotas_filtrar():
    conexion = establecer_conexion()
    mascota_caracteristicas = flask.request.get_json()
    condiciones = auxiliar.obtener_condiciones(mascota_caracteristicas)
    query = f"SELECT * FROM mascotas WHERE {condiciones};"

    try:
        resultado_query = conexion.execute(sqlalchemy.text(query))
        conexion.close()
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    if resultado_query.rowcount == 0:
        mensaje = {"mensaje": "No hay ninguna mascota que cumpla con las características."}
        return flask.jsonify(mensaje), 404

    json = auxiliar.crear_json(resultado_query, "mascotas")
    return flask.jsonify(json), 200



### Tabla: centros // Ver tabla ("GET") ###

@app.route("/centros/tabla", methods = ["GET"])
def centros_tabla():
    conexion = establecer_conexion()
    query = "SELECT * FROM centros;"

    try:
        resultado_query = conexion.execute(sqlalchemy.text(query))
        conexion.close()
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    if resultado_query.rowcount == 0:
        mensaje = {"mensaje": "No hay ningún centro en la tabla 'centros'."}
        return flask.jsonify(mensaje), 404

    json = auxiliar.crear_json(resultado_query, "centros")
    return flask.jsonify(json), 200



if __name__ == "__main__":
    app.run(debug = True, port = PORT)