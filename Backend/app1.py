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



### Ver tablas y agregar nuevas instancias ###

@app.route("/usuarios/tabla", methods = ["GET", "POST"])
def usuarios_tabla():
    conexion = establecer_conexion()

    if flask.request.method == "GET":
        query = "SELECT * FROM usuarios;"

        try:
            resultado_query = conexion.execute(sqlalchemy.text(query))
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        if resultado_query.rowcount == 0:
            mensaje = {"mensaje": "No hay ningún usuario en la tabla 'usuarios'."}
            return flask.jsonify(mensaje), 404

        json = auxiliar.crear_json(resultado_query, "usuarios")
        return flask.jsonify(json), 200

    elif flask.request.method == "POST":
        usuario_nuevo = flask.request.get_json()
        columnas = "nombre, contraseña, contacto"
        valores = auxiliar.obtener_valores(columnas, usuario_nuevo)
        query = f"INSERT INTO usuarios ({columnas}) VALUES ({valores});"

        try:
            conexion.execute(sqlalchemy.text(query))
            conexion.commit()
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Usuario creado correctamente."}
        return flask.jsonify(mensaje), 201


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
            conexion.commit()
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Mascota creada correctamente."}
        return flask.jsonify(mensaje), 201


@app.route("/centros/tabla", methods = ["GET", "POST"])
def centros_tabla():
    conexion = establecer_conexion()

    if flask.request.method == "GET":
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
    
    elif flask.request.method == "POST":
        centro_nuevo = flask.request.get_json()
        columnas = "nombre, descripcion, calle, altura, zona"
        valores = auxiliar.obtener_valores(columnas, centro_nuevo)
        query = f"INSERT INTO centros ({columnas}) VALUES ({valores});"

        try:
            conexion.execute(sqlalchemy.text(query))
            conexion.commit()
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Centro creado correctamente."}
        return flask.jsonify(mensaje), 201



### Filtrar información en las tablas ###

@app.route("/usuarios/filtrar", methods = ["POST"])
def usuarios_filtrar():
    conexion = establecer_conexion()
    usuario_caracteristicas = flask.request.get_json()
    condiciones = auxiliar.obtener_condiciones(usuario_caracteristicas)
    query = f"SELECT * FROM usuarios WHERE {condiciones};"

    try:
        resultado_query = conexion.execute(sqlalchemy.text(query))
        conexion.close()
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    if resultado_query.rowcount == 0:
        mensaje = {"mensaje": "No hay ningún usuario que cumpla con las características."}
        return flask.jsonify(mensaje), 404

    json = auxiliar.crear_json(resultado_query, "usuarios")
    return flask.jsonify(json), 200


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


@app.route("/centros/filtrar", methods = ["POST"])
def centros_filtrar():
    conexion = establecer_conexion()
    centro_caracteristicas = flask.request.get_json()
    condiciones = auxiliar.obtener_condiciones(centro_caracteristicas)
    query = f"SELECT * FROM centros WHERE {condiciones};"

    try:
        resultado_query = conexion.execute(sqlalchemy.text(query))
        conexion.close()
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    if resultado_query.rowcount == 0:
        mensaje = {"mensaje": "No hay ningún centro que cumpla con las características."}
        return flask.jsonify(mensaje), 404

    json = auxiliar.crear_json(resultado_query, "centros")
    return flask.jsonify(json), 200



### Actualizar y eliminar instancias ###

@app.route("/usuarios/<usuarioid>", methods = ["PATCH", "DELETE"])
def usuarios_id(usuarioid):
    conexion = establecer_conexion()
    query_verificacion = f"SELECT * FROM usuarios WHERE usuarioid = {usuarioid};"

    try:
        resultado_query_verificacion = conexion.execute(sqlalchemy.text(query_verificacion))
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    if resultado_query_verificacion.rowcount == 0:
        mensaje = {"mensaje": "No hay ningún usuario con dicha id."}
        return flask.jsonify(mensaje), 404


    if flask.request.method == "PATCH":
        usuario_modificaciones = flask.request.get_json()
        columnas_y_valores = auxiliar.obtener_columnas_y_valores(usuario_modificaciones)
        query = f"UPDATE usuarios SET {columnas_y_valores} WHERE usuarioid = {usuarioid};"

        try:
            conexion.execute(sqlalchemy.text(query))
            conexion.commit()
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Usuario modificado correctamente."}
        return flask.jsonify(mensaje), 200

    elif flask.request.method == "DELETE":
        query = f"DELETE FROM usuarios WHERE usuarioid = {usuarioid};"

        try:
            conexion.execute(sqlalchemy.text(query))
            conexion.commit()
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Usuario eliminado correctamente."}
        return flask.jsonify(mensaje), 200


@app.route("/mascotas/<mascotaid>", methods = ["PATCH", "DELETE"])
def mascotas_id(mascotaid):
    conexion = establecer_conexion()
    query_verificacion = f"SELECT * FROM mascotas WHERE mascotaid = {mascotaid};"

    try:
        resultado_query_verificacion = conexion.execute(sqlalchemy.text(query_verificacion))
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    if resultado_query_verificacion.rowcount == 0:
        mensaje = {"mensaje": "No hay ninguna mascota con dicha id."}
        return flask.jsonify(mensaje), 404


    if flask.request.method == "PATCH":
        mascota_modificaciones = flask.request.get_json()
        columnas_y_valores = auxiliar.obtener_columnas_y_valores(mascota_modificaciones)
        query = f"UPDATE mascotas SET {columnas_y_valores} WHERE mascotaid = {mascotaid};"

        try:
            conexion.execute(sqlalchemy.text(query))
            conexion.commit()
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Mascota modificada correctamente."}
        return flask.jsonify(mensaje), 200

    elif flask.request.method == "DELETE":
        query = f"DELETE FROM mascotas WHERE mascotaid = {mascotaid};"

        try:
            conexion.execute(sqlalchemy.text(query))
            conexion.commit()
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Mascota eliminada correctamente."}
        return flask.jsonify(mensaje), 200


@app.route("/centros/<centroid>", methods = ["PATCH", "DELETE"])
def centros_id(centroid):
    conexion = establecer_conexion()
    query_verificacion = f"SELECT * FROM centros WHERE centroid = {centroid};"

    try:
        resultado_query_verificacion = conexion.execute(sqlalchemy.text(query_verificacion))
    except SQLAlchemyError as falla:
        error = {"error": str(falla.__cause__)}
        return flask.jsonify(error), 500

    if resultado_query_verificacion.rowcount == 0:
        mensaje = {"mensaje": "No hay ningún centro con dicha id."}
        return flask.jsonify(mensaje), 404


    if flask.request.method == "PATCH":
        centro_modificaciones = flask.request.get_json()
        columnas_y_valores = auxiliar.obtener_columnas_y_valores(centro_modificaciones)
        query = f"UPDATE centros SET {columnas_y_valores} WHERE centroid = {centroid};"

        try:
            conexion.execute(sqlalchemy.text(query))
            conexion.commit()
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Centro modificado correctamente."}
        return flask.jsonify(mensaje), 200

    elif flask.request.method == "DELETE":
        query = f"DELETE FROM centros WHERE centroid = {centroid};"

        try:
            conexion.execute(sqlalchemy.text(query))
            conexion.commit()
            conexion.close()
        except SQLAlchemyError as falla:
            error = {"error": str(falla.__cause__)}
            return flask.jsonify(error), 500

        mensaje = {"mensaje": "Centro eliminado correctamente."}
        return flask.jsonify(mensaje), 200



### Login ###

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



if __name__ == "__main__":
    app.run(debug = True, port = PORT)