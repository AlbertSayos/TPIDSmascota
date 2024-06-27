#!/bin/bash

# Actualizar el índice de paquetes e instalar Python 3.12 si es necesario
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Crear y activar el entorno virtual con pipenv usando Python 3.12
pipenv --python 3.12

# Instalar Flask y las demás dependencias
pipenv install flask
pipenv install requests pip install python-dotenv

# Ejecutar la aplicación dentro del entorno virtual
pipenv run python app.py

