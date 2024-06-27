def crear_json(resultado_query, tabla: str) -> list[dict]:
    """
    Dado el resultado de una query y el nombre de la tabla de donde proviene, devuelve
    un modelo json del resultado.

    Precondiciones:
        - `resultado_query` es el resultado de la ejecución de una query en una base de
        datos MySQL.
        - `tabla` es una cadena que representa una tabla en particular de la base de datos.

    Postcondiciones:
        - La función devuelve una lista de diccionarios, donde cada uno representa una
        instancia de la tabla respectiva; las claves son las columnas, mientras que los
        valores el tipo de dato definido en la base de datos.

    """
    json = []
    if tabla == "usuarios":
        for fila in resultado_query:
            usuario = {}
            usuario["usuarioid"] = fila.usuarioid
            usuario["nombre"] = fila.nombre
            usuario["contraseña"] = fila.contraseña
            usuario["contacto"] = fila.contacto
            json.append(usuario)

    elif tabla == "mascotas":
        for fila in resultado_query:
            mascota = {}
            mascota["mascotaid"] = fila.mascotaid
            mascota["nombre"] = fila.nombre
            mascota["especie"] = fila.especie
            mascota["raza"] = fila.raza
            mascota["sexo"] = fila.sexo
            mascota["descripcion"] = fila.descripcion
            mascota["calle"] = fila.calle
            mascota["altura"] = fila.altura
            mascota["zona"] = fila.zona
            mascota["usuarioid"] = fila.usuarioid
            mascota["contacto"] = fila.contacto
            json.append(mascota)

    elif tabla == "centros":
        for fila in resultado_query:
            centro = {}
            centro["centroid"] = fila.centroid
            centro["nombre"] = fila.nombre
            centro["descripcion"] = fila.descripcion
            centro["calle"] = fila.calle
            centro["altura"] = fila.altura
            centro["zona"] = fila.zona
            json.append(centro)

    return json



def obtener_condiciones(json: dict) -> str:
    """
    Dado un json con datos referentes a las columnas de una de las tablas, devuelve una
    cadena del tipo "clave = 'valor'", separadas cada una por " AND ".

    Precondiciones:
        - `json` es un diccionario cuyas claves son todas o algunas de las columnas de una
        tabla en particular. Asimismo, sus valores respetan el tipo de dato ya definido en
        la base de datos.

    Postcondiciones:
        - La función devuelve una cadena que sirve como parte de diversas queries MySQL.

    """
    condiciones = ""
    columnas_abarcadas = 0
    for columna, valor in json.items():
        columnas_abarcadas += 1

        if columnas_abarcadas != len(json):
            condiciones += f"{columna} = '{valor}' AND "
        else:
            condiciones += f"{columna} = '{valor}'"

    return condiciones



def obtener_columnas_y_valores(json: dict) -> str:
    """
    Dado un json con datos referentes a las columnas de una de las tablas, devuelve una
    cadena del tipo "clave = 'valor'", separadas cada una por ", ".

    Precondiciones:
        - `json` es un diccionario cuyas claves son todas o algunas de las columnas de una
        tabla en particular. Asimismo, sus valores respetan el tipo de dato ya definido en
        la base de datos.

    Postcondiciones:
        - La función devuelve una cadena que sirve como parte de diversas queries MySQL.

    """
    columnas_y_valores = ""
    columnas_abarcadas = 0
    for columna, valor in json.items():
        columnas_abarcadas += 1

        if columnas_abarcadas != len(json):
            columnas_y_valores += f"{columna} = '{valor}', "
        else:
            columnas_y_valores += f"{columna} = '{valor}'"

    return columnas_y_valores



def obtener_valores(columnas: str, json: dict) -> str:
    """
    Dada una cadena con las columnas de una de las tablas y un json con datos referentes a
    cada una de ellas, devuelve una cadena con los valores de este último, ordenados según
    la cadena de columnas.

    Precondiciones:
        - `columnas` es una cadena que contiene los nombres de las columnas de una tabla en
        particular, separadas cada una por ", ".
        - `json` es un diccionario cuyas claves son todas las columnas de una tabla en
        particular. Asimismo, sus valores respetan el tipo de dato ya definido en la base
        de datos.

    Postcondiciones:
        - La función devuelve una cadena que sirve como parte de diversas queries MySQL.

    """
    valores = ""
    lista_columnas = columnas.split(", ")
    for columna in lista_columnas:

        if columna != lista_columnas[len(lista_columnas) - 1]:
            valores += f"'{json[columna]}', "
        else:
            valores += f"'{json[columna]}'"

    return valores