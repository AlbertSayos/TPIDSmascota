#!/bin/bash

# Actualizar el índice de paquetes e instalar Python 3.12 si es necesario
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev

# Crear y activar el entorno virtual con pipenv usando Python 3.12
pipenv --python 3.10

# Instalar Flask y las demás dependencias
pipenv install flask
pipenv install SQLAlchemy Flask-SQLAlchemy mysql-connector-python PyJWT Flask-JWT-Extended

# Ejecutar la aplicación dentro del entorno virtual
pipenv run python app.py

